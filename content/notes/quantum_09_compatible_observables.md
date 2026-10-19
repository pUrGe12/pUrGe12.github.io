+++
title = "Compatible observables and simultaneous eigenkets"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Compatible observables

$\hat A$ and $\hat B$ are **compatible** when they commute:

$$
[\hat A, \hat B] = 0
$$

and **incompatible** when $[\hat A, \hat B] \neq 0$.

Assume that the ket space is spanned by the eigenkets of $\hat A$.

$$
\implies |\alpha\rangle = \sum_{a\'}\langle a\'|\alpha\rangle|a\'\rangle
$$

We can also say that the same ket space is spanned by the eigenkets of $\hat B$.

How is $|a\'\rangle$ related to $|b\'\rangle$ when $[\hat A, \hat B] = 0$?

## Degeneracy

> If two or more linearly independent eigenkets of $\hat A$ have the same eigenvalue, those eigenvalues are **degenerate**.

$\implies |a\'\rangle \to$ not sufficient (to label a state). $\langle a\'\'|a\'\rangle = 0$ iff they are non-degenerate.

If the dim. of the ket space > no. of distinct eigenvalues of $\hat A$, we're cooked! How can $\sum_{a\'}c_{a\'}|a\'\rangle$ be true?

Ignore them (for now).

## Theorem

> **Theorem:** Suppose $[\hat A, \hat B] = 0$ and the eigenvalues of $\hat A$ are non-degenerate. Then the matrix elements $\langle a\'\'|\hat B|a\'\rangle$ are all diagonal. And the matrix elements of $\hat A$ are already diagonal if the basis kets are $\lbrace|a\'\rangle\rbrace$.

$$
\begin{aligned}
\langle a\'\'|[\hat A, \hat B]|a\'\rangle &= \langle a\'\'|\hat A\hat B - \hat B\hat A|a\'\rangle \\\\
&= a\'\'\langle a\'\'|\hat B|a\'\rangle - \langle a\'\'|\hat B|a\'\rangle a\' \\\\
&= (a\'\' - a\')\langle a\'\'|\hat B|a\'\rangle
\end{aligned}
$$

(assuming $a\'\'$ is real, which it is since $\hat A$ is Hermitian). The left side is $0$ since the commutator is $0$:

$$
(a\'\' - a\')\langle a\'\'|\hat B|a\'\rangle = 0
$$

$\therefore a\' = a\'\'$ or $\langle a\'\'|\hat B|a\'\rangle = 0$

- $a\' = a\'\'$ for two different kets would mean degeneracy $\implies$ **not true**.
- so $\langle a\'\'|\hat B|a\'\rangle = 0$ **must be true**.

Note that the way we write the matrix is $\langle a\'\'|\hat B|a\'\rangle$, with $a\'\'$ the row and $a\'$ the column.

$\therefore$ for every row $\neq$ column, element $= 0$, and the diagonal elements are $\delta_{a\'a\'\'}\langle a\'|\hat B|a\'\rangle$.

$\therefore$ We can represent the matrix $\hat B$ with the same set of base kets as $\hat A$: $\lbrace|a\'\rangle\rbrace$

$$
\implies \hat B = \sum_{a\'\'}|a\'\'\rangle\langle a\'\'|\hat B|a\'\'\rangle\langle a\'\'|
$$

If $\hat B$ acts on $|a\'\rangle$:

$$
\hat B|a\'\rangle = |a\'\rangle\langle a\'|\hat B|a\'\rangle
$$

(survives only for that eigenket). But this is the eigenvalue equation of $\hat B$, with eigenvalue $\langle a\'|\hat B|a\'\rangle$

> $\implies |a\'\rangle$ is an eigenket of both $\hat B$ and $\hat A$.

$\therefore$ we can use $|a\',b\'\rangle$ to denote this

> **Compatible operators have simultaneous eigenkets.**

$$
\begin{aligned}
\hat A|a\',b\'\rangle &= a\'|a\',b\'\rangle \\\\
\hat B|a\',b\'\rangle &= b\'|a\',b\'\rangle
\end{aligned}
$$

(different eigenvalues). Or, we can use a collective index $|K\'\rangle = |a\',b\'\rangle$.

## Maximal set of commuting observables

Suppose we have a maximal set of commuting observables

$$
[\hat A, \hat B] = [\hat B, \hat C] = \dots = 0
$$

The eigenvalues of the individual $\hat A, \hat B$ etc. may have degeneracies, but if we specify a combination $(a\', b\', c\', \dots)$ then the simultaneous eigenket of $\hat A, \hat B, \hat C, \dots$ is unique.

$$
|K\'\rangle = |a\', b\', c\', \dots\rangle
$$

They're orthonormal:

$$
\langle K\'\'|K\'\rangle = \delta_{K\'K\'\'} = \delta_{a\'a\'\'}\delta_{b\'b\'\'}\dots
$$

and closure:

$$
\sum_{K\'}|K\'\rangle\langle K\'| = 1 = \sum_{a\'}\sum_{b\'}\dots|a\',b\',\dots\rangle\langle a\',b\',\dots|
$$

## Measuring compatible observables

What about measurements of $\hat A$ and $\hat B$ when $[\hat A, \hat B] = 0$?

$$
|\alpha\rangle \xrightarrow{\hat A} |a\',b\'\rangle \xrightarrow{\hat B} |a\',b\'\rangle \xrightarrow{\hat A} |a\',b\'\rangle
$$

when the eigenvalues are non-degenerate. Measuring one doesn't mess up the other.

When there is degeneracy, the system (an arbitrary state ket) after the first $\hat A$ is

$$
\sum_i c_{a\'}^{(i)}|a\', b^{(i)}\rangle
$$

---

[← Measurements, probabilities and the S-G experiment](@/notes/quantum_08_measurements_and_sg.md) | Next: [The uncertainty relation →](@/notes/quantum_10_uncertainty_relation.md)
