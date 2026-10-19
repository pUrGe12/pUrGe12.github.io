+++
title = "The uncertainty relation"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Dispersion

Given $\hat A$, define

$$
\Delta A \equiv A - \langle A\rangle
$$

where $\langle A\rangle$ is the expectation value $\langle\alpha|\hat A|\alpha\rangle$. (And for a constant $c$: $\langle c\rangle = c\langle\alpha|\alpha\rangle = c$ if $|\alpha\rangle$ is normalized.)

The expectation of $(\Delta A)^2$:

$$
\langle(\Delta A)^2\rangle = \left\langle A^2 + \langle A\rangle^2 - 2A\langle A\rangle\right\rangle
$$

Note that $\langle A\rangle$ is a number, hence $A\langle A\rangle = \langle A\rangle A$.

$$
\begin{aligned}
\implies \langle(\Delta A)^2\rangle &= \langle A^2\rangle + \left\langle\langle A\rangle^2\right\rangle - \left\langle 2A\langle A\rangle\right\rangle \\\\
&= \langle A^2\rangle + \langle A\rangle^2 - 2\langle A\rangle\cdot\langle A\rangle
\end{aligned}
$$

$$
\boxed{\langle(\Delta A)^2\rangle = \langle A^2\rangle - \langle A\rangle^2}
$$

$\to$ **dispersion** (the variance / mean-square deviation).

## Dispersion of Sz in the S-G experiment

Let the state ket be

$$
|\alpha\rangle = |S_x;+\rangle = \frac{1}{\sqrt{2}}\left(|+\rangle + |-\rangle\right)
$$

and $\hat A = \hat S_z$.

$$
\langle\hat S_z\rangle = \langle\alpha|\hat S_z|\alpha\rangle = \left(\langle S_x;+|\right)\left(\hat S_z|S_x;+\rangle\right)
$$

First, $S_z$ in terms of the base kets:

$$
S_z = S_z\cdot I = S_z\cdot\sum_{a\'}|a\'\rangle\langle a\'|
$$

$$
\implies S_z = \sum_{a\'\'}\sum_{a\'}|a\'\'\rangle\langle a\'\'|S_z|a\'\rangle\langle a\'|
$$

For 2-states, $S_z = \sum_{a\'}a\'|a\'\rangle\langle a\'|$ if the basis vectors are eigenkets. We don't need 2 insertions:

$$
\implies S_z = \sum_{a\'}S_z|a\'\rangle\langle a\'| = \sum_{a\'}a\'|a\'\rangle\langle a\'|
$$

$$
\boxed{S_z = \frac{\hbar}{2}\left(|+\rangle\langle+| - |-\rangle\langle-|\right)}
$$

Done.

Now with that, the variance / mean-square deviation is $\langle A^2\rangle - \langle A\rangle^2$.

Eg. dispersion of $S_z$ for a spin $\frac{1}{2}$ system $= \langle S_z^2\rangle - \langle S_z\rangle^2$.

For $|\alpha\rangle = |S_x;+\rangle$:

$$
\langle S_z\rangle = \langle S_x;+|\hat S_z|S_x;+\rangle = 0
$$

(since $\hat S_z|S_x;+\rangle = \frac{\hbar}{2}\cdot\frac{1}{\sqrt{2}}\left(|+\rangle - |-\rangle\right) = \frac{\hbar}{2}|S_x;-\rangle$, which is orthogonal to $|S_x;+\rangle$)

$$
S_z^2 = S_z\cdot S_z = \frac{\hbar^2}{4}\left(|+\rangle\langle+| - |-\rangle\langle-|\right)\left(|+\rangle\langle+| - |-\rangle\langle-|\right)
$$

$$
S_z^2 = \frac{\hbar^2}{4}\underbrace{\left(|+\rangle\langle+| + |-\rangle\langle-|\right)}\_{\text{closure}} = \frac{\hbar^2}{4}I
$$

$$
\therefore \langle S_z^2\rangle = \frac{\hbar^2}{4}
$$

$\implies$ the dispersion of $S_z$:

$$
\boxed{\langle(\Delta S_z)^2\rangle = \frac{\hbar^2}{4} - 0 = \frac{\hbar^2}{4}}
$$

$\implies$ the state in x ($S_x$) has an undefined $\pm S_z$.

If instead the state was $|S_z;+\rangle$, then the dispersion would be 0 $\implies$ no spread in $S_z$. We know it exactly.

---

[← Compatible observables and simultaneous eigenkets](@/notes/quantum_09_compatible_observables.md) | Next: [Incompatible observables and the general uncertainty relation →](@/notes/quantum_11_incompatible_observables.md)
