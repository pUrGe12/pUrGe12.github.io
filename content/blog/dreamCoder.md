+++
title = "An analysis of DreamCoder"
date = 2026-04-03
draft = false

[taxonomies]
categories = ["ML" ,"functional-programming"]
tags = ["Automation"]

[extra]
lang = "en"
+++

# DreamCoder

DreamCoder is a seminal (I am guessing) research paper published by MIT scientists on a machine learning algorithm that generates programs to solve tasks in any domain. It does this via taking in a set of **primitives** in that domain (read: a DSL, i.e. **Domain Specific Language**), **learning** to create higher-order abstractions and using a **Neural Network** as a guide to help search for the right program.

In this blog post, I will be deconstructing the paper with every single line as I learnt them and analyze this paper. Why am I doing this? Hopefully that'll be clear soon (I have some vague ideas, I am reading some papers to get a concrete understanding of it, DreamCoder happens to be one of them).

## Introduction

### Aim

- The aim is to create a system that learns to solve problems by writing programs.
- The idea behind learning is something called **program induction**.

> The learning of a new task is searching for a program that solves it or has the intended behaviour.

I thought of the goal of the system as a curve finder. Just like in **curve fitting** where we have a bunch of data points and we need to find a function that fits that perfectly, the goal here is to find a `program` (not just a mathematical function, but a function is within the set of programs), that can produce the desired output in `any domain`.

The word **any** is important because the primitives we pass it detemine the language the system will learn and reason in. (Does it really reason? I'll let you decide that once we progress forward).


### Approach

- Start with a DSL and some primitives.

What does that mean exactly? This means that if you're trying to solve physics problems, your primitives in the DSL will be the **laws of motion** perhaps, the basic equations of **calculus** and similar primitives. These are what the system will `train` on.

- Train it (and the NN that comes along with it) -> We'll see about this soon
- Have a NN that will `guide` the model in its search for a program given a task.

The serach problem is a combinatorial explosion. There are so many ways to arrange primitives, some of them will make sense, some won't, so how do you efficiently search for the right program? That is one of the major hurdles that the paper tries to avoid (we'll see how they do that, and why its good but still not very practical).

- **Learning** happens for both the model that "generates" the program and the NN that guides it.

Notice I used the word generate here. Because later we'll read about a learning phase called **abstraction** which will generate libraries out of useful + previously seen primitives to use in later tasks. In practice therefore, the model which tries to **search** for a program, CAN also be said to be generating the said program. In spirit ofcourse, its not a `generation model` per se.

Now the paper mentions two more ideas which they have utilizied to solve this problem:

1. **Bayesian multitask program learning** (I couldn't understand why use this, from it’s name)
2. **Neurally-guided program synthesis** (I can understand why this, because the NN literally is supposed to help in program generation for program induction)

Now these are two separate research paper so I am did read them yet. But since the authors also didn't explain any more on these, I think its implicit in their arguments.


### The wake-sleep algorithm

**Learning** happens as part of the wake-sleep algorithm (specifically in the sleep phase). Each iteration of training is a `wake-phase` of trying to **solve a task**, and 2 `sleep phases` for learning to **solve new-tasks**.

Let me clarify some notation for you:


- [x] `X` -> domin of the tasks (say physics or web)
- [x] `x` -> single task from the domain X
- [x] `px` -> A program that solves x
- [x] `L` -> Library of tasks which form a "prior" distribution of programs likely to solve x in X
- [x] `P[p|L]` -> The generative model defined as giving a program from the given library
- [x] `Q(p|x)` -> The posterior distribution output by the NN given the task x.

The NN gives out a "posterior distribution" over programs likely to solve the task. A posterior distribution is probability distribution that takes into context both the `prior` and the `liklihood`.

In bayesian statistics, the **posterior** is the final step in the three-part process of updating your belief in with new evidence.

- The **Prior Distribution** (Before): This is your initial belief about something before you see any new data.
- The **Likelihood** (The Evidence): This is the new data or evidence you just observed.
- The **Posterior Distribution** (After): This is your updated belief after combining your Prior with the new Evidence.

Mathematically, it looks like this:

$$
\text{Posterior} \propto \text{Prior} \times \text{Likelihood}
$$

(hopefully the above is rendered properly)

