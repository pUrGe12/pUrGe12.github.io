+++
title = "Gradient Inversion attacks"
date = 2025-06-08
draft = false

[taxonomies]
categories = ["AI-security"]
tags = ["AI-Security", "blog"]

[extra]
lang = "en"
+++

## Introduction

This is a red teaming tactic against Federated learning, and it basically means "given the updated model weights and gradients, can you reconstruct what the data was?". I think this is pretty cool because from the papers I read on this, it is possible to super accurately reconstructed images trained on CNNs! The idea here is to see if Differential Privacy is going to be of any help in protecting from a gradient inversion attack.

In this blog I will talk mainly about what this attack is and why this happens. I have explained using the breaching library to execute the attack and achieve high accuracies in [this blog](https://purge12.github.io/blob/breaching-optimize). Additionally, you can find some insights on differential privacy in [this one](https://purge12.github.io/blog/differential-privacy).

## Background

The idea is as follows:

1. We have been given leaked gradients for the last 5 records for all rounds in a Federated learning setup.
2. There are 3 rounds in total (0 to 2) 

--- Finish this ---