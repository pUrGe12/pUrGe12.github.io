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

Basically, there are a lot of cool things we can try, the basic one that I have used is the `optimization` and the truth is, that's the one which works. The others have different uses which I will describe later in the blog.

So, it calls the `OptimizationBasedAttacker` class and that has a method called `reconstruct` which is what we used in the code shared above.

---

Then I noticed was the the `invertinggradients.yaml` file which has some hyperparams that we can tune off. 

---

Talk about adding the regularizer and why that worked. Talk about the different types and what makes the one we use, better.

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