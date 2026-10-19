+++
title = "Kets and the Hilbert space"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## The Hilbert space

Looking at that $i$ in $|S_y;\pm\rangle$ from the [Stern-Gerlach notes](@/notes/quantum_01_stern_gerlach.md), the **Hilbert space** must be a complex vector space.

## Kets

- A physical state is represented by a state vector $\to$ called a **"ket"**: $|\alpha\rangle$
- It contains complete info about the state.

We can add two kets:

$$
|\alpha\rangle + |\beta\rangle = |\gamma\rangle
$$

or constant multiply:

$$
c|\alpha\rangle = |\alpha\rangle c, \qquad c \in \mathbb{C}
$$

Physics says $|\alpha\rangle$ and $c|\alpha\rangle$ ($c \neq 0$) represent the same physical state $\implies$ only the "direction" in this vector space is of any significance.

## Observables and eigenkets

> An observable is an operator $\to \hat A$. The operator acts on a ket from the left.

$$
\hat A\cdot\left(|\alpha\rangle\right) = \hat A|\alpha\rangle
$$

In some special cases, for some "eigenkets", we have

$$
\hat A|a\'\rangle = a\'|a\'\rangle, \qquad \hat A|a\'\'\rangle = a\'\'|a\'\'\rangle
$$

where $|a\'\rangle, |a\'\'\rangle$ are all eigenkets, and $a\', a\'\'$ are just numbers $\in \mathbb{C}$ (the eigenvalue of the ket).

> The physical state corresponding to an eigenket is called an **eigenstate**.

Eg.

$$
\begin{aligned}
\hat S_z|S_z;+\rangle &= \frac{\hbar}{2}|S_z;+\rangle \\\\
\hat S_z|S_z;-\rangle &= -\frac{\hbar}{2}|S_z;-\rangle
\end{aligned}
$$

here, $|S_z;\pm\rangle$ are eigenkets of the operator $\hat S_z$. And,

$$
\hat S_x|S_x;\pm\rangle = \pm\frac{\hbar}{2}|S_x;\pm\rangle
$$

↳ same eigenvalues, different states.

## Dimensionality

The dimensionality of the vector space is determined by the no. of alternatives in SG type experiments $\implies$ experiments to measure all measurables. How many alternatives? (For the spin in the SG experiment, two: $S_z = \pm\hbar/2$.)

We are concerned with an $N$-dim. vector space spanned by $N$ eigenkets of observable $\hat A$. Then any arbitrary ket $|\alpha\rangle$ can be written as:

$$
|\alpha\rangle = \sum_{a\'} c_{a\'}|a\'\rangle
$$

with $a\', a\'\', \dots, a^{(N)}$ and $c_{a\'}$ is a $\mathbb{C}$ number.

Is this unique? Will see.

---

[← The Stern-Gerlach experiment](@/notes/quantum_01_stern_gerlach.md) | Next: [Bras, the dual space and inner products →](@/notes/quantum_03_bras_and_inner_products.md)
