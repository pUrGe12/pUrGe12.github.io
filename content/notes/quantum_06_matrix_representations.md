+++
title = "Matrix representations"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Operators as matrices

Using closure (inserting the identity) twice:

$$
\hat X = \hat X\cdot\sum_{a\'}|a\'\rangle\langle a\'| = \sum_{a\'}\hat X|a\'\rangle\langle a\'|
$$

$$
= \sum_{a\'\'}|a\'\'\rangle\langle a\'\'|\cdot\sum_{a\'}\hat X|a\'\rangle\langle a\'|
$$

Any arbitrary operator:

$$
\boxed{\hat X = \sum_{a\'\'}\sum_{a\'}|a\'\'\rangle\langle a\'\'|\hat X|a\'\rangle\langle a\'|}
$$

If $N$ is the dim. of the ket space, there are $N^2$ no.s of the form $\langle a\'\'|\hat X|a\'\rangle$ $\implies$ we can arrange all $N^2$ no.s in an $N \times N$ matrix. In $\langle a\'\'|\hat X|a\'\rangle$, $a\'\'$ is the **row** and $a\'$ is the **column**:

$$
\hat X \doteq \begin{pmatrix}
\langle a^{(1)}|\hat X|a^{(1)}\rangle & \langle a^{(1)}|\hat X|a^{(2)}\rangle & \cdots \\\\
\langle a^{(2)}|\hat X|a^{(1)}\rangle & \langle a^{(2)}|\hat X|a^{(2)}\rangle & \cdots \\\\
\vdots & \vdots & \ddots
\end{pmatrix}
$$

where $|a^{(i)}\rangle$ denotes the eigenket of $\hat A$ (Hermitian), and $\doteq$ means "is represented by".

Note that:

$$
\langle a\'\'|\hat X|a\'\rangle = \langle a\'|\hat X^\dagger|a\'\'\rangle^{\ast}
$$

↳ Hermitian adjoint.

## Multiplying operators

The arrangement of the $X$ matrix is deliberate, to follow a row $\times$ column multiplication.

$$
\langle a\'|\hat X|a\'\'\rangle = \left(\langle a\'|\hat X\right)\cdot|a\'\'\rangle = \langle a\'|\left(\hat X|a\'\'\rangle\right) \in \mathbb{C}
$$

Say, $\hat Z = \hat X\hat Y$

$$
\begin{aligned}
\langle a\'\'|\hat Z|a\'\rangle &= \langle a\'\'|\hat X\hat Y|a\'\rangle \\\\
&= \langle a\'\'|\hat X\left(\sum_{a\'\'\'}|a\'\'\'\rangle\langle a\'\'\'|\right)\hat Y|a\'\rangle
\end{aligned}
$$

$$
\langle a\'\'|\hat Z|a\'\rangle = \sum_{a\'\'\'}\langle a\'\'|\hat X|a\'\'\'\rangle\langle a\'\'\'|\hat Y|a\'\rangle
$$

which is (matrix) $= \sum$ (matrix) $\cdot$ (matrix), exactly matrix multiplication.

## Kets as column vectors

How can we represent $|\gamma\rangle = \hat X|\alpha\rangle$ using base kets?

Recall that $|\gamma\rangle = \sum_{a\'}c_{a\'}|a\'\rangle$ and $c_{a\'} = \langle a\'|\gamma\rangle$.

$\therefore$ finding the expansion coefficients first,

$$
\begin{aligned}
\langle a\'|\gamma\rangle &= \langle a\'|\hat X|\alpha\rangle \\\\
&= \langle a\'|\hat X\left(\sum_{a\'\'}|a\'\'\rangle\langle a\'\'|\right)|\alpha\rangle \\\\
&= \sum_{a\'\'}\underbrace{\langle a\'|\hat X|a\'\'\rangle}\_{\text{matrix}}\cdot\underbrace{\langle a\'\'|\alpha\rangle}\_{\text{const. numbers}}
\end{aligned}
$$

To realize this, we can find the expansion coefficient $c_{a\'}$ for $|\alpha\rangle$ as $\langle a\'|\alpha\rangle$, and hence

$$
|\alpha\rangle = \sum_{a\'}\langle a\'|\alpha\rangle|a\'\rangle \doteq \begin{pmatrix} \langle a^{(1)}|\alpha\rangle \\\\ \langle a^{(2)}|\alpha\rangle \\\\ \vdots \end{pmatrix}
$$

Similarly,

$$
|\gamma\rangle \doteq \begin{pmatrix} \langle a^{(1)}|\gamma\rangle \\\\ \langle a^{(2)}|\gamma\rangle \\\\ \vdots \end{pmatrix}
$$

Now we have:

$$
\begin{pmatrix} \langle a^{(1)}|\gamma\rangle \\\\ \langle a^{(2)}|\gamma\rangle \\\\ \vdots \end{pmatrix} = \underbrace{\begin{pmatrix}
\langle a^{(1)}|\hat X|a^{(1)}\rangle & \langle a^{(1)}|\hat X|a^{(2)}\rangle & \cdots \\\\
\langle a^{(2)}|\hat X|a^{(1)}\rangle & \langle a^{(2)}|\hat X|a^{(2)}\rangle & \cdots \\\\
\vdots & \vdots & \ddots
\end{pmatrix}}\_{\text{operator matrix}} \begin{pmatrix} \langle a^{(1)}|\alpha\rangle \\\\ \langle a^{(2)}|\alpha\rangle \\\\ \vdots \end{pmatrix}
$$

That's so cool.

## Bras as row vectors

We can do the same stuff for bras: $\langle\gamma| = \langle\alpha|\hat X$

1. find $c_{a\'}$
2. represent all as matrices.

We can write a general bra as:

$$
\langle\gamma| = \sum_{a\'}c_{a\'}\langle a\'| \implies \langle\gamma|a\'\rangle = c_{a\'}
$$

$$
\implies \langle\gamma| = \sum_{a\'}\langle\gamma|a\'\rangle\langle a\'| = \sum_{a\'}\langle\alpha|\hat X|a\'\rangle\langle a\'|
$$

or, inserting the identity $\sum_{a\'}\Lambda_{a\'}$:

$$
\begin{aligned}
\langle\gamma|a\'\'\rangle &= \langle\alpha|\hat X|a\'\'\rangle \\\\
&= \langle\alpha|\left(\sum_{a\'}|a\'\rangle\langle a\'|\right)\hat X|a\'\'\rangle \\\\
&= \sum_{a\'}\langle\alpha|a\'\rangle\langle a\'|\hat X|a\'\'\rangle
\end{aligned}
$$

These are the coefficients $c_{a\'\'}$. Hence we can write the coefficients of a bra in a **row**:

$$
\boxed{
\begin{aligned}
\langle\gamma| &\doteq \begin{pmatrix} \langle\gamma|a^{(1)}\rangle & \langle\gamma|a^{(2)}\rangle & \langle\gamma|a^{(3)}\rangle & \cdots \end{pmatrix} \\\\
&= \begin{pmatrix} \langle a^{(1)}|\gamma\rangle^{\ast} & \langle a^{(2)}|\gamma\rangle^{\ast} & \cdots \end{pmatrix}
\end{aligned}
}
$$

Hence the inner product $\langle\beta|\alpha\rangle$ can be thought of as a row vector ($\langle\beta|$ bra) times a column vector ($|\alpha\rangle$ ket).

$$
\begin{aligned}
\langle\beta|\alpha\rangle &= \sum_{a\'}\langle\beta|a\'\rangle\langle a\'|\alpha\rangle \equiv \langle\beta|\left(\sum_{a\'}\Lambda_{a\'}\right)|\alpha\rangle \\\\
&= \begin{pmatrix} \langle a^{(1)}|\beta\rangle^{\ast} & \langle a^{(2)}|\beta\rangle^{\ast} & \cdots \end{pmatrix} \begin{pmatrix} \langle a^{(1)}|\alpha\rangle \\\\ \langle a^{(2)}|\alpha\rangle \\\\ \vdots \end{pmatrix} \in \mathbb{C}
\end{aligned}
$$

A complex no.

And the outer product can then be:

$$
|\beta\rangle\langle\alpha| \doteq \begin{pmatrix}
\langle a^{(1)}|\beta\rangle\langle a^{(1)}|\alpha\rangle^{\ast} & \langle a^{(1)}|\beta\rangle\langle a^{(2)}|\alpha\rangle^{\ast} & \cdots \\\\
\langle a^{(2)}|\beta\rangle\langle a^{(1)}|\alpha\rangle^{\ast} & \langle a^{(2)}|\beta\rangle\langle a^{(2)}|\alpha\rangle^{\ast} & \cdots \\\\
\vdots & \vdots & \ddots
\end{pmatrix}
$$

$\to$ a matrix.

> So what we've done is essentially that we are saying each bra or ket can be broken down into a sum of basis vectors, found the right coefficients and slapped them in for linear algebra!

## Observables in their own eigenbasis

For an observable (Hermitian) $\hat A$, its matrix representation becomes very simply its eigenvalue or 0, if its eigenkets are the base kets.

$$
\hat A = \sum_{a\'\'}\sum_{a\'}|a\'\'\rangle\underbrace{\langle a\'\'|\hat A|a\'\rangle}\_{\text{matrix}}\langle a\'|
$$

If the basis vectors are the $|a\'\rangle$, then the matrix is **diagonal**:

$$
\langle a\'\'|\hat A|a\'\rangle = \langle a\'|\hat A|a\'\rangle\delta_{a\'a\'\'}
$$

$$
\boxed{\langle a\'\'|\hat A|a\'\rangle = a\'\delta_{a\'a\'\'}}
$$

(a diagonal square matrix)

$$
\implies \hat A = \sum_{a\'\'}\sum_{a\'}|a\'\'\rangle a\'\delta_{a\'a\'\'}\langle a\'|
$$

Dead easy.

$$
\boxed{\hat A = \sum_{a\'}a\'|a\'\rangle\langle a\'| = \sum_{a\'}a\'\Lambda_{a\'}}
$$

note: $\Lambda_{a\'} = |a\'\rangle\langle a\'|$

---

[← Eigenkets, base kets and the identity operator](@/notes/quantum_05_eigenkets_and_base_kets.md) | Next: [Matrix representations for spin ½ systems →](@/notes/quantum_07_spin_half_matrices.md)
