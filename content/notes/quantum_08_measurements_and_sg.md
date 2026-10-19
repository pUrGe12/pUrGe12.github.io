+++
title = "Measurements, probabilities and the S-G experiment"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Measurements

> "A measurement always causes the system to jump into an eigenstate of the dynamical variable that is being measured"
>
> P.A.M. Dirac

Before measurement:

$$
|\alpha\rangle = \sum_{a\'}c_{a\'}|a\'\rangle = \sum_{a\'}\left(\langle a\'|\alpha\rangle\right)|a\'\rangle
$$

After measurement:

$$
|\alpha\rangle \xrightarrow{\text{measurement}} |a\'\rangle
$$

$\to$ some eigenstate, one of the many.

> **Measurement usually changes the state**

$\to$ unless of course, the state is already in one of the eigenstates of the observable:

$$
|a\'\rangle \xrightarrow{\text{measurement}} |a\'\rangle
$$

> When a measurement causes $|\alpha\rangle$ to become $|a\'\rangle$, it is said that $\hat A$ (Hermitian) is measured to be $a\'$ (the eigenvalue).

## Probability

Which eigenket will $|\alpha\rangle$ collapse to?

$$
\boxed{\text{Prob. for } a\' = |\langle a\'|\alpha\rangle|^2}
$$

↳ if $|\alpha\rangle$ is normalized.

To find $P(a\')$ empirically, we need to perform measurements on a **pure ensemble** of $|\alpha\rangle$ states.

Note that if $P(a\') = 1$ then $P(a\'\')$ or $P(a\'\'\') = 0$ with certainty. That is, if a state collapses to $|a\'\rangle$ then it cannot collapse further to $|a\'\'\rangle$ or $|a\'\'\'\rangle$, as $\langle a\'\'|a\'\rangle = 0$ $\forall a\' \neq a\'\'$.

We know $|\langle a\'|\alpha\rangle|^2 \geq 0$ and $\sum_{a\'}|\langle a\'|\alpha\rangle|^2 = 1$ from [earlier](@/notes/quantum_05_eigenkets_and_base_kets.md#the-identity-operator).

## Expectation value

$$
\langle\hat A\rangle = \langle\alpha|\hat A|\alpha\rangle
$$

$\to$ the expectation value of an operator w.r.t. state $|\alpha\rangle$.

For example: $\langle\hat S_z\rangle \in \left[-\frac{\hbar}{2}, \frac{\hbar}{2}\right]$ ↳ expectation is a range, but $S_z = \pm\frac{\hbar}{2}$ ↳ eigenvalues are discrete.

## Filtration

Filtration $\to$ choose only one eigenket of $\hat A$, say $|a\'\rangle$, and block the others.

Mathematically:

$$
\Lambda_{a\'}|\alpha\rangle = |a\'\rangle\langle a\'|\alpha\rangle
$$

This is like saying, "choose only $|a\'\rangle$".

## Sequential S-G experiments

> Let's talk about the results of the sequential S-G experiments.

```text
                  ┌──────────┐   Sz+
   Sx+  ────────► │    SG    │ ────────►
                  │  z-axis  │ ────────►
                  └──────────┘   Sz-
```

$$
P(S_z+) = P(S_z-) = \frac{1}{2}
$$

since it splits into equal intensities.

$$
P(|a\'\rangle) = |\langle a\'|\alpha\rangle|^2
$$

$\to$ Remember.

In our case $|\alpha\rangle = |S_x;+\rangle$ $\to$ the initial state. (We're denoting the $S_z+$ and $S_z-$ states as $|+\rangle$ and $|-\rangle$ only.)

$$
P(|+\rangle) = P(|S_z;+\rangle) = \frac{1}{2} = P(|-\rangle)
$$

$$
\boxed{|\langle+|S_x;+\rangle| = |\langle-|S_x;+\rangle| = \frac{1}{\sqrt{2}}}
$$

So, what does $|\alpha\rangle$ or $|S_x;+\rangle$ look like before measurement?

$$
\boxed{|S_x;+\rangle = \frac{1}{\sqrt{2}}|+\rangle + \frac{1}{\sqrt{2}}e^{i\delta_1}|-\rangle}
$$

with $\delta_1$ as real. Why like this? $\delta_1 \to$ "phase" for the vector. Some angle. Helpful in differentiation.

What about $|S_x;-\rangle$ then? We know it must be orthogonal to $|S_x;+\rangle \implies \langle S_x;-|S_x;+\rangle = 0$

$$
\boxed{|S_x;-\rangle = \frac{1}{\sqrt{2}}|+\rangle - \frac{1}{\sqrt{2}}e^{i\delta_1}|-\rangle}
$$

Why? Find

$$
\langle S_x;-| = \frac{1}{\sqrt{2}}\langle+| - \frac{1}{\sqrt{2}}e^{-i\delta_1}\langle-|
$$

and

$$
\langle S_x;-|S_x;+\rangle = \frac{1}{2}\langle+|+\rangle - \frac{1}{2}\langle-|-\rangle = 0
$$

(cross terms die). Hence, they are indeed orthogonal.

We choose the coefficient of $|+\rangle$ to be positive by convention.

## Building Sx and Sy

Now, we know

$$
\boxed{\hat A = \sum_{a\'}a\'|a\'\rangle\langle a\'| = \sum_{a\'}a\'\Lambda_{a\'}}
$$

In our case:

$$
\hat S_x = \frac{\hbar}{2}\left(|S_x;+\rangle\langle S_x;+| - |S_x;-\rangle\langle S_x;-|\right)
$$

cause now we know the ket $|S_x\rangle$ exactly,

$$
\boxed{\hat S_x = \frac{\hbar}{2}\left[e^{-i\delta_1}\left(|+\rangle\langle-|\right) + e^{i\delta_1}\left(|-\rangle\langle+|\right)\right]}
$$

To tell if it's Hermitian ($\hat S_x = \hat S_x^\dagger$), use

$$
\left(|a\rangle\langle b|\right)^\dagger = |b\rangle\langle a|, \qquad (cA)^\dagger = c^{\ast}A^\dagger, \qquad (A+B)^\dagger = A^\dagger + B^\dagger
$$

We can compute

$$
\hat S_x^\dagger = \frac{\hbar}{2}\left(e^{i\delta_1}|-\rangle\langle+| + e^{-i\delta_1}|+\rangle\langle-|\right) = \hat S_x
$$

$\therefore$

> $\hat S_x$ is indeed Hermitian.

Similarly, we can find

$$
|S_y;\pm\rangle = \frac{1}{\sqrt{2}}|+\rangle \pm \frac{1}{\sqrt{2}}e^{i\delta_2}|-\rangle
$$

and

$$
\hat S_y = \frac{\hbar}{2}\left[e^{-i\delta_2}\left(|+\rangle\langle-|\right) + e^{i\delta_2}\left(|-\rangle\langle+|\right)\right]
$$

## Finding the phases

But what are $\delta_1$ and $\delta_2$? $\to$ Can we find them?

If we have

```text
                  ┌──────────┐   Sy+
   Sx±  ────────► │    SG    │ ────────►
                  │  y-axis  │ ────────►
                  └──────────┘   Sy-
```

$$
\implies |\langle S_y;\pm|S_x;\pm\rangle| = \frac{1}{\sqrt{2}}
$$

Same as before. (This also hints at the invariance of the system under rotation.)

But,

$$
|S_y;+\rangle = \frac{1}{\sqrt{2}}|+\rangle + \frac{e^{i\delta_2}}{\sqrt{2}}|-\rangle, \qquad |S_y;-\rangle = \frac{1}{\sqrt{2}}|+\rangle - \frac{e^{i\delta_2}}{\sqrt{2}}|-\rangle
$$

and

$$
|S_x;+\rangle = \frac{1}{\sqrt{2}}|+\rangle + \frac{e^{i\delta_1}}{\sqrt{2}}|-\rangle, \qquad \langle S_y;+| = \frac{1}{\sqrt{2}}\langle+| + \frac{e^{-i\delta_2}}{\sqrt{2}}\langle-|
$$

$$
\implies |\langle S_y;+|S_x;+\rangle| = \left|\frac{1}{2} + \frac{1}{2}e^{i(\delta_1-\delta_2)}\right| = \frac{1}{\sqrt{2}}
$$

$$
\implies \frac{1}{2}\left|1 + e^{i(\delta_1-\delta_2)}\right| = \frac{1}{\sqrt{2}}
$$

only possible when

$$
\boxed{\delta_2 - \delta_1 = \pm\frac{\pi}{2}}
$$

Since the coefficients of $\hat S_x$ and $\hat S_y$ are $e^{i\delta}$, their matrix elements are not all real!!

$\to$ Convenient to take the $S_x$ matrix to be real and set $\delta_1 = 0$.

$$
\implies |S_x;+\rangle = \frac{1}{\sqrt{2}}|+\rangle + \frac{1}{\sqrt{2}}|-\rangle \quad\text{and}\quad |S_y;+\rangle = \frac{1}{\sqrt{2}}|+\rangle + \frac{e^{i\pi/2}}{\sqrt{2}}|-\rangle
$$

where $|+\rangle$ and $|-\rangle$ are shorthand for $|S_z;+\rangle$ and $|S_z;-\rangle$, which form our basis vectors.

Note that with $\delta_1 = 0$, $\delta_2 = \pm\frac{\pi}{2}$ is still ambiguous. Choose $\frac{\pi}{2}$, we'll see why later.

$$
\boxed{
\begin{aligned}
|S_x;\pm\rangle &= \frac{1}{\sqrt{2}}|+\rangle \pm \frac{1}{\sqrt{2}}|-\rangle \\\\
|S_y;\pm\rangle &= \frac{1}{\sqrt{2}}|+\rangle \pm \frac{i}{\sqrt{2}}|-\rangle
\end{aligned}
}
$$

Which is the same guess we made from polarized light in the [Stern-Gerlach notes](@/notes/quantum_01_stern_gerlach.md#analogies-from-polarized-light) (the $S_x$ one up to an overall sign, which doesn't change the state).

## Spin flipping operators

And the two non-Hermitian operators of spin flipping:

$$
\boxed{S_\pm = S_x \pm iS_y}
$$

$$
S_+ = \hbar|+\rangle\langle-|, \qquad S_- = \hbar|-\rangle\langle+|
$$

Quick check: with $\delta_1 = 0$ and $\delta_2 = \frac{\pi}{2}$ (so $e^{\mp i\pi/2} = \mp i$),

$$
\hat S_x = \frac{\hbar}{2}\left(|+\rangle\langle-| + |-\rangle\langle+|\right), \qquad \hat S_y = \frac{\hbar}{2}\left(-i|+\rangle\langle-| + i|-\rangle\langle+|\right)
$$

$$
\implies S_x + iS_y = \frac{\hbar}{2}\left(|+\rangle\langle-| + |-\rangle\langle+| + |+\rangle\langle-| - |-\rangle\langle+|\right) = \hbar|+\rangle\langle-| = S_+
$$

and the same way $S_x - iS_y = \hbar|-\rangle\langle+| = S_-$. These are the increment / decrement operators from the [spin ½ notes](@/notes/quantum_07_spin_half_matrices.md#raising-and-lowering-operators): they raise (or lower) the spin component by $\hbar$. They're not Hermitian since $S_+^\dagger = S_-$.

---

[← Matrix representations for spin ½ systems](@/notes/quantum_07_spin_half_matrices.md) | Next: [Compatible observables and simultaneous eigenkets →](@/notes/quantum_09_compatible_observables.md)
