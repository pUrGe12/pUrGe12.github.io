+++
title = "Formula reduction for Polyominoes"
date = 2026-08-23
draft = false

[taxonomies]
categories = ["Math", "Algebra"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

<style>
.poly {
  --cell: 1.2em;
  --poly-line: #3c4043;
  --poly-fill: #ffffff;
  --poly-new: #f2ce3c;
  --poly-gray: #d5d7da;
  --poly-red: #f0908a;
  --poly-green: #8ecf96;
  --poly-cyan: #86ccd6;
  display: inline-grid;
  grid-auto-columns: var(--cell);
  grid-auto-rows: var(--cell);
  vertical-align: middle;
  line-height: 0;
}
.poly i {
  display: block;
  border: 1px solid var(--poly-line);
  background: var(--poly-fill);
  margin: 0 -1px -1px 0;
}
.poly i.new { background: var(--poly-new); }
.poly i.g   { background: var(--poly-gray); }
.poly i.r   { background: var(--poly-red); }
.poly i.gr  { background: var(--poly-green); }
.poly i.cy  { background: var(--poly-cyan); }
.poly.sm    { --cell: 0.85em; vertical-align: -0.4em; }

.dark .poly {
  --poly-line: #8b9099;
  --poly-fill: #26282c;
  --poly-new: #b8952a;
  --poly-gray: #4b4f55;
  --poly-red: #9c5450;
  --poly-green: #4f7f57;
  --poly-cyan: #47818b;
}

.polyeq {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  margin: 1.7em 0;
}
.polyeq .op  { font-size: 1.1em; opacity: 0.7; padding: 0 0.1em; }
.polyeq .gap { width: 1.8em; }
.polyeq .lbl { font-size: 1em; white-space: nowrap; }

.latch { display: inline-flex; align-items: center; gap: 0.15em; }
.latch .pr {
  display: inline-block;
  font-size: 1.5em;
  font-weight: 300;
  line-height: 1;
  opacity: 0.55;
  transform: scaleY(1.45);
}
.latch .lt { font-family: KaTeX_Math, Georgia, serif; font-style: italic; font-size: 0.85em; opacity: 0.85; align-self: flex-end; margin-bottom: 0.35em; }

.slot {
  border: 1px dashed currentColor;
  background: rgba(128, 128, 128, 0.06);
  border-radius: 3px;
  padding: 1.1em 1.2em;
  margin: 1.6em 0;
  text-align: center;
  font-style: italic;
  font-size: 0.94em;
  opacity: 0.65;
}

.tetro-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 0.5em 2.4em;
  margin: 1.8em 0;
}
.tetro { display: flex; align-items: center; gap: 1em; min-height: 5.2em; }
.tetro-pic { flex: 0 0 5.2em; line-height: 0; }
.tetro-eq { flex: 1 1 auto; min-width: 0; overflow-x: auto; overflow-y: hidden; }

@media (max-width: 400px) {
  .tetro-grid { grid-template-columns: 1fr; }
  .tetro-eq { font-size: 0.9em; }
}
</style>

## Introduction

In the last [blog](https://purge12.github.io/blog/shape_algebra_1/), I discussed about some fundamental rules for the shape algebra. I closed with a remark on how we're able to not construct shapes like these:

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/1"></i><i class="g" style="grid-area:1/2"></i><i class="g" style="grid-area:1/3"></i><i class="g" style="grid-area:2/1"></i><i class="g" style="grid-area:2/3"></i><i class="g" style="grid-area:3/1"></i><i class="g" style="grid-area:4/1"></i><i class="g" style="grid-area:4/3"></i><i class="g" style="grid-area:5/1"></i><i class="g" style="grid-area:5/2"></i><i class="g" style="grid-area:5/3"></i></span></div>

In this blog, I'll explore a way of solving this first, then I'll write some generalized notation so that we can talk about the length of the formula as a "feature" of the algebra and ponder over it.

## Introducing Subtraction

The rules are the exact same as adding a block, except that when we write $-1_C$ we'll be removing the first block it hits. So, to give you a few examples:

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i></span><span class="op">&minus;</span><span class="latch"><span class="pr">(</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="pr">)</span><sub class="lt">C</sub></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i></span></div>

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:4/1"></i><i style="grid-area:4/2"></i><i style="grid-area:4/3"></i></span><span class="op">&minus;</span><span class="latch"><span class="pr">(</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="pr">)</span><sub class="lt">C</sub></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:4/1"></i><i style="grid-area:4/2"></i></span></div>

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:4/1"></i><i style="grid-area:4/2"></i><i style="grid-area:4/3"></i></span><span class="pr">)</span><sub class="lt">C</sub></span><span class="op">&minus;</span><span class="latch"><span class="pr">(</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="pr">)</span><sub class="lt">C</sub></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:4/2"></i><i style="grid-area:4/3"></i></span></div>

Hopefully these examples make it clear.

All other rules stay the same. With this in place, I had to use all the existing rules to carve out the shape above, and here's how it looks like:

$$
\left(\left(\left(\left(\left(\left(\left(\left(\left(\left(\left(\left(A_R^3+1_C\right)_C+1_C\right)^M_C+1_C\right)_C\right)_P+1_C\right)_C+1_C\right)+1_C\right)+1_C\right)+1_C\right)^M_C-1_R\right)_P-1_R\right)_C+1_R\right)_C+1_R
$$

To make that clearer:

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i></span><span class="op">$\xrightarrow{1_C\cdot2}$</span><span class="poly"><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i><i class="new" style="grid-area:1/3"></i><i class="new" style="grid-area:2/3"></i></span><span class="op">$\xrightarrow{M_C}$</span><span class="poly"><i class="new" style="grid-area:1/1"></i><i class="new" style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i></span><span class="op">$\xrightarrow{1_C}$</span><span class="poly"><i class="new" style="grid-area:1/1"></i><i class="new" style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i><i class="new" style="grid-area:2/3"></i></span><span class="op">$\xrightarrow{P}$</span><span class="poly"><i class="r" style="grid-area:1/1"></i><i class="r" style="grid-area:2/1"></i><i class="r" style="grid-area:3/1"></i><i class="r" style="grid-area:3/2"></i><i class="r" style="grid-area:3/3"></i><i class="r" style="grid-area:2/3"></i></span><span class="op">$\xrightarrow{1_C}$</span><span class="poly"><i class="new" style="grid-area:1/1"></i><i class="r" style="grid-area:2/1"></i><i class="r" style="grid-area:3/1"></i><i class="r" style="grid-area:4/1"></i><i class="r" style="grid-area:4/2"></i><i class="r" style="grid-area:4/3"></i><i class="r" style="grid-area:3/3"></i></span><span class="op">$\xrightarrow{1_C}$</span><span class="poly"><i class="new" style="grid-area:1/1"></i><i class="new" style="grid-area:2/1"></i><i class="r" style="grid-area:3/1"></i><i class="r" style="grid-area:4/1"></i><i class="r" style="grid-area:5/1"></i><i class="r" style="grid-area:5/2"></i><i class="r" style="grid-area:5/3"></i><i class="r" style="grid-area:4/3"></i></span><span class="op">$\xrightarrow{1_C\cdot3}$</span><span class="poly"><i class="new" style="grid-area:1/1"></i><i class="new" style="grid-area:2/1"></i><i class="r" style="grid-area:3/1"></i><i class="r" style="grid-area:4/1"></i><i class="r" style="grid-area:5/1"></i><i class="r" style="grid-area:5/2"></i><i class="r" style="grid-area:5/3"></i><i class="r" style="grid-area:4/3"></i><i class="new" style="grid-area:3/3"></i><i class="new" style="grid-area:2/3"></i><i class="new" style="grid-area:1/3"></i></span><span class="op">$\xrightarrow{M_C}$</span><span class="poly"><i class="new" style="grid-area:1/3"></i><i class="new" style="grid-area:2/3"></i><i class="r" style="grid-area:3/3"></i><i class="r" style="grid-area:4/3"></i><i class="r" style="grid-area:5/3"></i><i class="r" style="grid-area:5/2"></i><i class="r" style="grid-area:5/1"></i><i class="r" style="grid-area:4/1"></i><i class="new" style="grid-area:3/1"></i><i class="new" style="grid-area:2/1"></i><i class="new" style="grid-area:1/1"></i></span><span class="op">$\xrightarrow{-1_R}$</span><span class="poly"><i class="new" style="grid-area:1/3"></i><i class="new" style="grid-area:2/3"></i><i class="r" style="grid-area:4/3"></i><i class="r" style="grid-area:5/3"></i><i class="r" style="grid-area:5/2"></i><i class="r" style="grid-area:5/1"></i><i class="r" style="grid-area:4/1"></i><i class="new" style="grid-area:3/1"></i><i class="new" style="grid-area:2/1"></i><i class="new" style="grid-area:1/1"></i></span><span class="op">$\xrightarrow{P}$</span><span class="poly"><i class="cy" style="grid-area:1/3"></i><i class="cy" style="grid-area:2/3"></i><i class="cy" style="grid-area:4/3"></i><i class="cy" style="grid-area:5/3"></i><i class="cy" style="grid-area:5/2"></i><i class="cy" style="grid-area:5/1"></i><i class="cy" style="grid-area:4/1"></i><i class="cy" style="grid-area:3/1"></i><i class="cy" style="grid-area:2/1"></i><i class="cy" style="grid-area:1/1"></i></span><span class="op">$\xrightarrow{-1_R}$</span><span class="poly"><i class="cy" style="grid-area:2/3"></i><i class="cy" style="grid-area:4/3"></i><i class="cy" style="grid-area:5/3"></i><i class="cy" style="grid-area:5/2"></i><i class="cy" style="grid-area:5/1"></i><i class="cy" style="grid-area:4/1"></i><i class="cy" style="grid-area:3/1"></i><i class="cy" style="grid-area:2/1"></i><i class="cy" style="grid-area:1/1"></i></span><span class="op">$\xrightarrow{1_R}$</span><span class="poly"><i style="grid-area:1/2"></i><i class="cy" style="grid-area:2/3"></i><i class="cy" style="grid-area:4/3"></i><i class="cy" style="grid-area:5/3"></i><i class="cy" style="grid-area:5/2"></i><i class="cy" style="grid-area:5/1"></i><i class="cy" style="grid-area:4/1"></i><i class="cy" style="grid-area:3/1"></i><i class="cy" style="grid-area:2/1"></i><i class="cy" style="grid-area:1/1"></i></span><span class="op">$\xrightarrow{1_R}$</span><span class="poly"><i style="grid-area:1/3"></i><i style="grid-area:1/2"></i><i class="cy" style="grid-area:2/3"></i><i class="cy" style="grid-area:4/3"></i><i class="cy" style="grid-area:5/3"></i><i class="cy" style="grid-area:5/2"></i><i class="cy" style="grid-area:5/1"></i><i class="cy" style="grid-area:4/1"></i><i class="cy" style="grid-area:3/1"></i><i class="cy" style="grid-area:2/1"></i><i class="cy" style="grid-area:1/1"></i></span></div>

The only trick here was to leverage the pinned image. Because when we subtract, we can then subtract off exactly the middle element, which would be impossible to do so without a rule like this.

## Notation and reduction

You would have realized that there are a lot of unncessary brackets and plus signs. I mean addition is understood, so we can get rid of those and assume addition by default. We can also get rid of the brackets because its one block at a time always going to the right.

So, a formula can be written in a simplified manner:

$$
\left(\left(A_C^4 + 1_R\right)+1_R\right) \implies A_C^{4}(1_R \cdot 2)
$$

Basic translations:

1. $1_R$ + $1_R$ ... $n$ times = $(1_R \cdot n)$ 
2. 


There are some caveates to this. For example in case of rule 1, we only do this when the latch never changes! So, if we had latched onto a column before adding multiple things, we'll write:

$$
C1_R(1_R \cdot 3)
$$

and not

$$
C(1_R \cdot 4)
$$

This is because right after latching, the first $1_X$ will go to the largest X, but the subsequent ones will fall back to the defaults. Hence, we're trying to make this relationship discrete.

## Reduction formulas

Now let's talk about some reduction formulas. The goal of the reduction formula is that if we see the LHS anywhere in the equation, we should be able to substitute them for the RHS and leave the entire equation unchanged. This means, we need to care about the latches as well.

$$
M_{X}M_{X} = \text{empty}
$$

$$
A_X^{j+k} = A_X^j(1_X \cdot k) \forall j,k \in N
$$

$$
M_{X}M_{Y} = M_{Y}M_{X} \forall X \neq Y
$$

So with these, we can reduce an obviously wrong formula into the simplest form:

$$
A_C^{2}1_C1_{R}M_{R}M_{C}M_{C}M_{R} \to A_C^{3}1_R
$$

In the following relation, I had to latch onto `X` in the RHS because the LHS was latched to X. If we don't do that, then we'll mess up the next element's placement.

$$
A_X^{j}(1_Y \cdot (j-1))M_Y = A_Y^{j}(1_X \cdot (j-1))M_XX
$$

In fact it is this observation that led me to adding subtraction in the rules and discovering the new formula for the unspeakable shape.

## Coverage

So, I was able to run some scripts to prove that we're able to reach all the shapes upto N = 11 atleast. After that the required computations go very high so I didn't run those checks. I'll keep updating this, but I assume there shouldn't be a problem with coverage now with all the rules we have in place.

## Theorems and observations

We can define some basic theorems:

**If we're starting from base $A_X^j$, for a figure with N blocks, if the number of "steps" needed is S then**

$$
S \geq (N-j)
$$

This is kinda trivial to see tbh. You will need N-j new blocks to build the shape, so definetly the number of steps will exceed that since we'll be counting M, P and X in the steps as well.

What you're not prepared for is this emperical fact I discovered by running more scripts. I did the following:

1. For each value of N from 5 to 10, we'll take every possible fixed polyominoes and try to find an algebra that fits it.
2. For each algebra that we find, we'll count the number of steps. We'll find ALL possible algebra until we have exhausted the possible branches (the approach is obviously not a naive search, I'll talk about the code later) and move on.
3. We'll count how many shapes fit in "i" number of "steps" and plot that.

If we count the percentage of shapes achieved for different $N$ values against the number of steps, we get this nice looking graph:

{{ figure(src="assets/shape_algebra_2_percentage.png", alt="Percentage of shapes covered against steps", caption="Percentage of total fixed shapes covered against steps (minimum)") }}

> Note that fixes shapes means we're not counting rotations and reflections as the same thing for any shape. Each operation results in a distinct shape.

Clearly the graph is shifting to the right, with the peak decreasing ever so slightly. The thing I want you to focus on right now is the correspondance between the $N$ value and the number of steps at which it peaks. They're the same! That's a pretty coincidence to have isn't it. It also means that for a given $N$ value, atleast emperically, more than 30% of the shapes can be generated in a minimum of $N$ steps.

Maybe there is a proof for that, I am yet to do that.

Here's another image I want to direct your attention to. This one is plotting the average number of steps (minimum) across all shapes for a given N, against N.

{{ figure(src="assets/shape_algebra_2_linear_growth.png", alt="Average minimum steps plotted against N values", caption="Average minimum steps plotted against N values") }}

This is a clear result because look at that beautiful linear growth! We roughly get 

$$
\text{mean} \approx 1.2n − 1.75
$$

So, each new value of N, requires on average 1.2 times more steps. 