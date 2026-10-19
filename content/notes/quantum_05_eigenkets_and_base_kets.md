+++
title = "Eigenkets, base kets and the identity operator"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Eigenkets of observable operators

Let $\hat A$ be a Hermitian operator ($\hat A = \hat A^\dagger$). Hermitian operators turn out to be observables!!

> **Theorem:** Eigenvalues of a Hermitian operator are real. Eigenkets of $\hat A$ corresponding to diff. eigenvalues are orthogonal.

Start with the eigenvalue equations:

$$
\hat A|a\'\rangle = a\'|a\'\rangle \quad (1) \qquad \text{and} \qquad \hat A|a\'\'\rangle = a\'\'|a\'\'\rangle
$$

Taking the dual correspondence of the second one (and using $\hat A^\dagger = \hat A$):

$$
\langle a\'\'|\hat A = a\'\'^{\ast}\langle a\'\'| \quad (2)
$$

Now hit (1) with $\langle a\'\'|$ from the left and (2) with $|a\'\rangle$ from the right:

$$
\begin{aligned}
\langle a\'\'|\cdot(1): &\quad \langle a\'\'|\hat A|a\'\rangle = a\'\langle a\'\'|a\'\rangle \\\\
(2)\cdot|a\'\rangle: &\quad \langle a\'\'|\hat A|a\'\rangle = a\'\'^{\ast}\langle a\'\'|a\'\rangle
\end{aligned}
$$

Subtracting:

$$
0 = \left(a\' - a\'\'^{\ast}\right)\langle a\'\'|a\'\rangle
$$

- If $a\'\'$ and $a\'$ are the same (and the ket is not NULL) $\implies$ we know $\langle a\'|a\'\rangle > 0$ $\implies a\' = a\'^{\ast}$ $\therefore$

> $a\'$ must be **real**

- If $a\'$ and $a\'\'$ are not the same, then $a\' - a\'\'^{\ast}$ cannot be 0 $\implies$ $\langle a\'\'|a\'\rangle = 0$ $(a\' \neq a\'\')$, which proves the orthogonality.

We expect observables to have real eigenvalues. The theorem proves that for Hermitians.

It is conventional to normalize $|a\'\rangle$ so that $|a\'\rangle, |a\'\'\rangle, \dots$ form an **orthonormal** set (orthogonal + normal):

$$
\langle a\'\'|a\'\rangle = \delta_{a\'\'a\'}, \qquad \delta_{a\'a\'\'} = \begin{cases} 1 & a\' = a\'\' \\\\ 0 & a\' \neq a\'\' \end{cases}
$$

## Eigenkets as base kets

Recall that we said any ket $|\alpha\rangle$ can be formed by $|a\'\rangle, |a\'\'\rangle, \dots$ and so on (henceforth represented as $\lbrace|a\'\rangle\rbrace$), or

$$
|\alpha\rangle = \sum_{a\'} c_{a\'}|a\'\rangle
$$

Let's dive deeper into these basis vectors.

- We know that the normalized eigenkets of $\hat A$ (Hermitian) form a complete orthonormal set.

$$
|\alpha\rangle = \sum_{a\'} c_{a\'}|a\'\rangle
$$

where $|a\'\rangle$ is an eigenket of $\hat A$ (Hermitian).

$$
\implies \langle a\'\'|\alpha\rangle = \sum_{a\'} c_{a\'}\langle a\'\'|a\'\rangle
$$

Since $\langle a\'\'|a\'\rangle = \delta_{a\'\'a\'}$, we get $\langle a\'\'|\alpha\rangle = c_{a\'}$ when $a\' = a\'\'$

$$
\boxed{\langle a\'|\alpha\rangle = c_{a\'}}
$$

(So the expansion from the [kets notes](@/notes/quantum_02_kets_and_hilbert_space.md) *is* unique, the coefficients are fixed by this.)

$$
\implies |\alpha\rangle = \sum_{a\'}\langle a\'|\alpha\rangle|a\'\rangle = \sum_{a\'}|a\'\rangle\langle a\'|\alpha\rangle
$$

From associativity:

$$
|\alpha\rangle = \left(\sum_{a\'}|a\'\rangle\langle a\'|\right)|\alpha\rangle
$$

## The identity operator

This has to hold for any $|\alpha\rangle$, so

$$
\boxed{\sum_{a\'}|a\'\rangle\langle a\'| = 1}
$$

$\to$ must be true. This is an **identity operator**, and the relation is called **"closure"**.

Eg.

$$
\begin{aligned}
\langle\alpha|\alpha\rangle &= \langle\alpha|\cdot\left(\sum_{a\'}|a\'\rangle\langle a\'|\right)\cdot|\alpha\rangle \\\\
&= \sum_{a\'}\langle\alpha|a\'\rangle\langle a\'|\alpha\rangle \\\\
&= \sum_{a\'}|\langle\alpha|a\'\rangle|^2 = \sum_{a\'}|\langle a\'|\alpha\rangle|^2
\end{aligned}
$$

$\to$ Real no. But $\langle a\'|\alpha\rangle = c_{a\'}$

$$
\implies \sum_{a\'}|c_{a\'}|^2 = \sum_{a\'}|\langle a\'|\alpha\rangle|^2 = \langle\alpha|\alpha\rangle = 1
$$

if $\langle\alpha|\alpha\rangle = 1$ $\implies$ if $|\alpha\rangle$ is normalized.

## Meaning of the outer product

Coming back to $|a\'\rangle\langle a\'|$ $\to$ the outer product of two eigenkets of a Hermitian operator $\to$ must also be an operator.

$$
\left(|a\'\rangle\langle a\'|\right)|\alpha\rangle = |a\'\rangle\cdot\langle a\'|\alpha\rangle = c_{a\'}|a\'\rangle
$$

> $|a\'\rangle\langle a\'|$ selects that portion of $|\alpha\rangle$ parallel to $|a\'\rangle$

$\implies |a\'\rangle\langle a\'|$ is called the **projection operator** along base ket $|a\'\rangle$.

$$
\boxed{\Lambda_{a\'} \equiv |a\'\rangle\langle a\'|}
$$

Outer products like these get used to select or flip spin (eg. $|+\rangle\langle-|$ flips a down spin to up).

And we have,

$$
\sum_{a\'}\Lambda_{a\'} = 1
$$

$\to$ Identity.

Think of it as saying,

> if you take a ket $|\alpha\rangle$ and take its projections in $\lbrace|a\'\rangle\rbrace$, then adding all those projections will give back $|\alpha\rangle$.

---

[← Operators, commutators and outer products](@/notes/quantum_04_operators.md) | Next: [Matrix representations →](@/notes/quantum_06_matrix_representations.md)
