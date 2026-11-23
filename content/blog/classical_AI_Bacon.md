+++
title = "Classical AI paradigms (BACON) and improvements"
date = 2026-11-08
draft = false

[taxonomies]
categories = ["AI", "Data"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

BACON is an old paradigm, what's called a "classical AI" model in today. It was proposed to find laws based on numerical data by Patrick Langley back in 1977! I was going through a paper by Tyler Josephson of UMBC who mentioned this old tool and I got curious. Turns out that a group in Cambridge with Soumya Banerjee and Jonah Miller who were making a case for the the "classical AI" systems for equation discovery in 2024-25. (I couldn't find their social's with 100% probability so I am not linking them here but do check their work out).

I thought I should check it out because it seemed like an interesting idea and this blog post will talk about exactly that. Note that the original code for Langley has not survived the time translation, it was written in a language called PRISM apparently, so any reference anyone had is from his [textbook](https://www.google.co.in/books/edition/Scientific_Discovery/VPxc-uPB7LEC?hl=en), which is what Jonah Miller used to recreate an implementation of BACON and push it to GitHub. See the code [here](https://github.com/JonahMiller/BACON).

Here I am trying to understand how exactly BACON works and then I'll report on some benchmarks that I ran against PySINDy (a sparse regression paradigm) and the improvements I made over it (I think I'll skip the comparision and talk about the improvements directly since the GitHub repo has all the necessary comparisions anyway). That might go in a new post depending on how big this gets. So, let's get started. I am using Jonah's dissertation file as the reference because I don't want to go and read Langley's book.

## The architecture

There are atleast 6 versions of Bacon that Langley came up with and since no code survived, Jonah's version is the 7th. I am talking about the 7th version which apart from being the only one I `can` talk about, is better than the previous 6 in terms of noise reliability and overall accuracy.

We need to understand how BACON will handle a system of two input datasets $D(X)$ and $D(Y)$ to give out $f(X, Y)$, that is, a function that relates variables $X$ and $Y$ based on their datasets.

> BACON accepts only one dependent variable

The core philosophy of this tool is to find `invariants`. By finding quantities that do not change, in `radical` forms (We'll talk about how those radicals are achieved) it's able to come up with a function $f(X,Y)$ in terms of those variants.

There are two layers to the architecture:

1. Heuristic Layer
2. Managing Layer

The Heuristic Layer has the actual "logic" which decides given two datasets $D(X)$ and $D(Y)$ (with $Y$ being the dependent variable according to convention), whether:

- [x] $Y$ is a constant
- [x] $Y-mX$ is feasible for some $m$
- [x] $XY$ is a new symbol
- [x] $\frac{Y}{X}$ is a new symbol

The important question here is, how does the model decide when something is a "new symbol"? We'll talk about that soon. First, let's talk about tolerances which will affect how we work with noisy data.

### Tolerances in the Heuristics Layer

There are three kinds of tolerances that the approach uses:

1. $\delta$: Tolerance for considering $Y$ as a constant
2. $\epsilon$: Tolerance for assuming $X$ and $Y$ vary lineraly
3. $c_{var}$: Tolerance for having the $Y$ intercept of that linearity be non-zero

To check if $Y$ is a constant, the model computes $M_Y = \sum_{i} y_i / \sum_{i}$, and checks if 

$$
M_Y(1-\delta) < y_i < M_Y(1+\delta) \forall i
$$

and if its true, then $Y$ is defined to be a constant.

To check if $X$ and $Y$ are proportional, it computes the correlation coefficient: 

$$
r = \frac{\sum_i \left((X_i - M_X)(Y_i-M_Y)\right)}{\sqrt(\sum_i (X_i-M_X)^2 \sum_i (Y_i-M_Y)^2)}
$$

If $|r| \approx 1$ then we say that $X$ and $Y$ are linearly proportional. $r>0$ means $X$ and $Y$ increase or decrease together (hence they should be divded in hopes of getting an invariant) and $r<0$ means they are inversely proportional, hence they should be multiplied to potentially get an invariant.

Linear relationship is when $1-|r| < \epsilon$ and to ensure that $X+mY=c$ we need to see if the Y intercept $c$ is zero or not. Which we do via $\left| \frac{c}{mean(D(Y))} \right| < c_{var}$.

### Management Layer

This layer "supplies" the independent variables to the Heuristics layer depending on the invariants that the heuristics layer finds. It goes somewhat like this code below:

1.  input X, Y, d(X), d(Y), hyperparams (δ, ε, c_rel, s_ε, s_δ)
2.  Z, d(Z), State = HL(X, Y)
3.  Z1, d(Z1), State1 = HL(X, Z)
4.  if State1 not in {Prod, Div, Null}:
        return Invariant: Z1, Data: d(Z1), State: State1   # Exit 1
5.  Z2, d(Z2), State2 = HL(Y, Z)
6.  if State2 in {Lin, Const}:
        return Invariant: Z2, Data: d(Z2), State: State2   # Exit 2
7.  if State1 == Null and State2 == Null:
        jmp 12
8.  j = j + 1
9.  if State2 != Null:
        Z, d(Z), State = HL(X, Z2)
10. else:
        Z, d(Z), State = HL(X, Z1)
11. jmp 3
12. ε = s_ε * ε
13. δ = s_δ * δ
14. jmp 1


Okay this might be a mouthful, but in essence what's happening is simple. We take the intial variables and try to find product, fraction or linear rules through the HL. If HL says for example that `xy` is a valid invariant, we STILL want to check if there is a linearity condition too. So, we don't stop there and check for linearity before incrementing our counter. All the "complexity" in the pseudo code comes from that.

If nothing is found, then we update our hyperparams, we relax them a bit and try again from the very beginning. Now there is an iteration counter in between if you want to make sure it doesn't keep running forever, but I omitted that from the pseudocode.

## Bacon 6 and beyond

So, the core idea behind the latest implementation of Bacon is as above, however we don't know if AS ABOVE was exactly what Bacon did (in terms of code, that is). Anyway, `Bacon 6` was the last of the family that Langley wrote and it required a basic understanding of the relationship that you are trying to further cement. So, not really an EXPLORATORY thing with this one.

Miller's method uses a bunch of "layer pickers" which pick an expression from the list of possible expressions. That's an improvement over Bacon we've seen above. So, here, he considers:

1. `popular`: Selects the expression which appears most frequently 
2. `min_mse`: Minimize MSE
3. `gp_ranking`: GP Regression to optimize S/R ratio
4. `user_input`: Similar to bacon 6

He used `popular` and `min_mse` so, that's what I did too. The others took more time to run and had identical results. He does explain why we need multiple methods, but I am already sold.

BTW, the whole hyperparams thing above, was actually a part of the `Bacon 7` paradigm which "must have been" a core of Bacon too but alas.

Anyway, this seems like a good place to stop. I have got an idea on what my hybrid (with [PySindy](https://pysindy.readthedocs.io/en/latest/)) should look like, I'll write about that and then talk about some `BusyBeavers`.

---
