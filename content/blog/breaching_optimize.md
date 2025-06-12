+++
title = "Gradient Inversion attacks with the breaching library"
date = 2025-06-02
draft = false

[taxonomies]
categories = ["AI-security"]
tags = ["AI-Security", "blog"]

[extra]
lang = "en"
+++

The [`breaching`](https://github.com/JonasGeiping/breaching) library created by Jonas Geiping is for gradient inversion attacks. In this blog, I will be explaining how we managed to achieve an accuracy of 65% (the way we calculate this is a little different and will be explained later) in gradient inversions for the [Genomics PPFL red teaming](https://pages.nist.gov/genomics_ppfl/index.html) competition (Note that this is before the leaderboards were updated, if something happens after that, well, I will update this), by hypermodification of the breaching library to fit our dataset and increase accuracy.

I have seperate blogs on [Differential Privacy](https://purge12.github.io/blog/differential-privacy) (DP) which you can go through if you want to understand the challenges in reconstructing data through leaked gradients for that, but that is not a necessity.

# The setting

We were testing our tactics on a federated learning setting where we had access to 4 clients (client_0 to 4), and with each client there are 3 rounds of learning where each client submits their data to the server after a training round, recieves the aggregated weights and trains again.

In our case, along with the weights in each round we had been provided with the leaked gradients after the stochastic gradient descent for the last 5 data records. The data itself has over 100,000 features which makes it susceptible to PCA (we didn't apply that in this case because we thought it won't necessary and that wouldn't make sense because for reconstruction, the more data we have the better). 

So, we have 3 different privacy settings:

1. Normal CNN --> no privacy
2. DP enchanced CNN (with epsilon = 5) --> more privacy, less useful 
3. DP ehchanced CNN (with epsilon = 200) --> less privacy, more useful

To measure the accuracy of our attack model, we had also been provided with the inverted gradients for the client_2 for each round and for each privacy setting. The accuracy calculation will be described later.

# Breaching library

The main code for inverting gradients looks something like this (this is the part we code):

```py
attacker = breaching.attacks.prepare_attack(
    task_model, loss_fn, cfg_attack, setup)
reconstructed_user_data, stats = attacker.reconstruct(server_payload,
                                                      shared_data, {},
                                                      dryrun=False)
```

The `prepare_attack` function is made available to all the modules inside the library throught the `__init__.py` file. Inside, we can note the following description:

```py
def prepare_attack(model, loss, cfg_attack, setup=dict(dtype=torch.float, device=torch.device("cpu"))):
    if cfg_attack.attack_type == "optimization":
        attacker = OptimizationBasedAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "multiscale":
        attacker = MultiScaleOptimizationAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "analytic":
        attacker = AnalyticAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "april-analytic":
        attacker = AprilAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "imprint-readout":
        attacker = ImprintAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "decepticon-readout":
        attacker = DecepticonAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "recursive":
        attacker = RecursiveAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "joint-optimization":
        attacker = OptimizationJointAttacker(model, loss, cfg_attack, setup)
    elif cfg_attack.attack_type == "permutation-optimization":
        attacker = OptimizationPermutationAttacker(model, loss, cfg_attack, setup)
    else:
        raise ValueError(f"Invalid type of attack {cfg_attack.attack_type} given.")

    return attacker
```

Basically, there are a lot of cool things we can try, the basic one that I have used is the `optimization` and the truth is, that's the only one which works. The others have different uses which I will describe later in the blog.

So, it calls the `OptimizationBasedAttacker` class and that has a method called `reconstruct` which is what we used in the code shared above. Before we dive into the reconstruct method, we should checkout the `__init__` because that is what holds the `regularizers` and `augmentations` implementation.

```py
def __init__(self, model, loss_fn, cfg_attack, setup=dict(dtype=torch.float, device=torch.device("cpu"))):
    super().__init__(model, loss_fn, cfg_attack, setup)
    objective_fn = objective_lookup.get(self.cfg.objective.type)
    if objective_fn is None:
        raise ValueError(f"Unknown objective type {self.cfg.objective.type} given.")
    else:
        self.objective = objective_fn(**self.cfg.objective)
    self.regularizers = []
    try:
        for key in self.cfg.regularization.keys():
            if self.cfg.regularization[key].scale > 0:
                self.regularizers += [regularizer_lookup[key](self.setup, **self.cfg.regularization[key])]
    except AttributeError:
        pass  # No regularizers selected.

    try:
        self.augmentations = []
        for key in self.cfg.augmentations.keys():
            self.augmentations += [augmentation_lookup[key](**self.cfg.augmentations[key])]
        self.augmentations = torch.nn.Sequential(*self.augmentations).to(**setup)
    except AttributeError:
        self.augmentations = torch.nn.Sequential()  # No augmentations selected.
```

So, here we can see that it gets the `key` values from `self.cfg` and based on the scale there, it adds regularizers. The first thing to understand is how self.cfg comes into picture. Like what exactly is it? This comes from this definition of `Hydra`:

```py
def get_attack_config(attack="invertinggradients", overrides=[]):
    """Return default hydra config for a given attack."""
    with hydra.initialize(config_path="config/attack"):
        cfg = hydra.compose(config_name=attack, overrides=overrides)
    return cfg
```

This is basically what `self.cfg` also means, its a packed version of this YAML file, which by default is called `invertinggradients.yaml`. This works for me because this is literally what I am trying to do. So, inside this yaml are these configuration params, (note that I have already edited these to fit my idea, it will orignally be different):

```yaml
defaults:
  - _default_optimization_attack
  - _self_
type: invertinggradients

objective:
  type: angular
  scale: 1.0 # need to have a much smaller scale like 0.0001 for euclidean objectives

restarts:
  num_trials: 1
  scoring: "euclidean"

optim:
  optimizer: adam
  signed: "hard"
  step_size: 0.025
  boxed: True
  max_iterations: 70
  step_size_decay: step-lr
  langevin_noise: 0.0

  callback: 1000

regularization:
  orthogonality:
    scale: 0.1
``` 

So, `self.cfg` gives us access to all of this. I will explain these changes later, first let us explore what the `reconstruct` code looks like:

```py
def reconstruct(self, server_payload, shared_data, server_secrets=None, initial_data=None, dryrun=False):
    rec_models, labels, stats = self.prepare_attack(server_payload, shared_data)
    scores = torch.zeros(self.cfg.restarts.num_trials)
    candidate_solutions = []
    try:
        for trial in range(self.cfg.restarts.num_trials):
            candidate_solutions += [
                self._run_trial(rec_models, shared_data, labels, stats, trial, initial_data, dryrun)
            ]
            scores[trial] = self._score_trial(candidate_solutions[trial], labels, rec_models, shared_data)
    except KeyboardInterrupt:
        print("Trial procedure manually interruped.")
        pass
    optimal_solution = self._select_optimal_reconstruction(candidate_solutions, scores, stats)
    reconstructed_data = dict(data=optimal_solution, labels=labels)
    ...
```

Basically, it checks the number of trials it should run, then for that many times it passes it to `_run_trials` method. I won't add the code here. But the general idea behind that is it first initializes all the regularizers. In my case, I have defined that to be `orthogonal` and the default was `TotalVariation`. 

The reason we can't use `TotalVariation` here is because of this function defined inside that class.

```py
def forward(self, tensor, *args, **kwargs):
        """Use a convolution-based approach."""
        if self.double_opponents:
            tensor = torch.cat(
                [
                    tensor,
                    tensor[:, 0:1, :, :] - tensor[:, 1:2, :, :],
                    tensor[:, 0:1, :, :] - tensor[:, 2:3, :, :],
                    tensor[:, 1:2, :, :] - tensor[:, 2:3, :, :],
                ],
                dim=1,
            )
        diffs = torch.nn.functional.conv2d(
            tensor, self.weight, None, stride=1, padding=1, dilation=1, groups=self.groups
        )
        squares = (diffs.abs() + self.eps).pow(self.inner_exp)
        squared_sums = (squares[:, 0::2] + squares[:, 1::2]).pow(self.outer_exp)
        return squared_sums.mean() * self.scale
```

This is using the `torch.nn.functional.conv2d` function which requires the `tensor` to be 4D but ours ain't. Thus in the sample code they had given, they were bypassing this deliberately. This is achievied by setting the `scale` value there to 0, 

```py
self.regularizers = []
        try:
            for key in self.cfg.regularization.keys():
                if self.cfg.regularization[key].scale > 0:
                    self.regularizers += [regularizer_lookup[key](self.setup, **self.cfg.regularization[key])]
```

Hence, it never knew that the `TotalVariation` was set. So, I changed the scale to 0.1 and changed the regularizer to `orthogonal`which works for our data. 

### What exactly are regularizers?

Regularization is simply the process of penalizing the model when it tries to overfit. The idea is that, we have a `scale` value and we multiply that to a `regularization term` to prevent the loss being minimized exactly (yeah its a lil weird). 

I was thinking that regularization will be especially helpful here, because we have about 100k features but very less rows, so the chances of overfitting are very high. This would mean that, it will never be able to achieve a high accuracy for testing data, which it has never seen before.

The reason I went with `orthogonal` is two-folds:

1. It was easily available and worked without tweaking the function
2. It made sense


I think I don't have to explain the first part, I was able to simply set this regularizer in the YAML file and boom, it works. But the second part requires more attention. The idea is that `orthogonal` regularization penalizes **non-orthogonality** of gradients (its for weights or gradients). The reason this works is because in FL, the orthogonality of gradients provides less aligned gradient information, or less redundant gradient information. This makes gradient inversion harder.

Additionally, we are denoising the data. I mean, I can say a bunch of things here, but I could say the same about some other method if that worked. or I could equally critize this method if it didn't work.

I think the data was such that this gave the best results. I am not `really` sure what and why this worked in this case.

---

Finally, how we figured out the best hyperparams for training the model in our case and what is the theory behind the reconstruction in the first place.

# Measuring accuracy

Talk about the code

```py
def check_similarity(groundtruth, reconstructed, class_labels):
        # For each reconstructed row, find the best match in the answers file
    for i, (r_row, r_label) in enumerate(zip(reconstructed, class_labels)):
        # Find the best match in the answers file
        for j, (g_row, label) in enumerate(zip(groundtruth, class_labels)):
            # Find the best match from those answers file rows that has
            # the same label as the reconstructed row
            if label == r_label:
                # Compare the reconstructed row with the answer row
                correct = g_row == r_row
                # Compute total values matched in the reconstructed row
                correct_sum_onehot = np.sum(correct)
                # Get accuracy of the reconstructed row against the answer row
                accuracy = correct_sum_onehot / len(g_row)
                # Store the index of the answer row and accuracy
                # against the reconstructed row.
                if len(accuracies) < i + 1:
                    accuracies.append((j, accuracy))
                # If the accuracy is better than the previous best match,
                # update the accuracy
                elif accuracy > accuracies[i][1]:
                    accuracies[i] = (j, accuracy)

    # Print the best match for each reconstructed row`
    for i, ((j, accuracy), label) in enumerate(zip(accuracies, labels)):
        print(f'Reconstructed row {i} with label {label} best matched with answer row {j} with accuracy {accuracy:.4f}')
```