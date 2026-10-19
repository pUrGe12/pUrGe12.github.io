+++
title = "Change of basis and the transformation matrix"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Change of basis

Take two incompatible operators $\hat A, \hat B$ $\implies [\hat A, \hat B] \neq 0$.

The entire ket space, as we know, can be spanned by eigenkets and their linear combinations. In this case, it can be $\lbrace|a\'\rangle\rbrace$ or $\lbrace|b\'\rangle\rbrace$.

What transformation takes us from $\lbrace|a\'\rangle\rbrace$ to $\lbrace|b\'\rangle\rbrace$?

Changing the set of base kets ($\lbrace|a\'\rangle\rbrace$ to $\lbrace|b\'\rangle\rbrace$ for eg.) is a **change of basis**. We want to figure out some transformation operator to connect these two.

We define a **"unitary" operator** $U$ as:

$$
U = \sum_k |b^{(k)}\rangle\langle a^{(k)}|
$$

Then applying $U$ to $|a^{(l)}\rangle$ gives:

$$
U|a^{(l)}\rangle = \sum_k |b^{(k)}\rangle\langle a^{(k)}|a^{(l)}\rangle
$$

Now since the $\lbrace|a\'\rangle\rbrace$ are orthonormal, only $k = l$ survives:

$$
U|a^{(l)}\rangle = |b^{(l)}\rangle\underbrace{\langle a^{(l)}|a^{(l)}\rangle}\_{1}
$$

$$
\boxed{U|a^{(l)}\rangle = |b^{(l)}\rangle}
$$

$\to$ that's the transform.

Further, using the [adjoint of an outer product](@/notes/quantum_04_operators.md#adjoint-of-an-outer-product), $U^\dagger = \sum_l |a^{(l)}\rangle\langle b^{(l)}|$:

$$
U^\dagger U = \sum_l\sum_k |a^{(l)}\rangle\langle b^{(l)}|b^{(k)}\rangle\langle a^{(k)}|
$$

and since $\lbrace|b\'\rangle\rbrace$ is orthonormal,

$$
\boxed{U^\dagger U = \sum_k |a^{(k)}\rangle\langle a^{(k)}|}
$$

and we know from before that this is the [identity](@/notes/quantum_05_eigenkets_and_base_kets.md#the-identity-operator)

$$
\implies \boxed{U^\dagger U = 1}
$$

## Transformation matrix

Let's look at the matrix representation of $U$ in the $\lbrace|a\'\rangle\rbrace$ basis. This basis is now the **"old"** basis, and $\lbrace|b\'\rangle\rbrace$ is now the **"new"** basis.

$$
\langle a^{(k)}|U|a^{(l)}\rangle = \langle a^{(k)}|b^{(l)}\rangle
$$

$\therefore$ the matrix elements of $U$ are made of the inner products of old basis bras and new basis kets.

Now consider rotating the axes, $(\hat x, \hat y, \hat z)$ to $(\hat x\', \hat y\', \hat z\')$:

$$
R^{(3)} = \begin{pmatrix}
\hat x\cdot\hat x\' & \hat x\cdot\hat y\' & \hat x\cdot\hat z\' \\\\
\hat y\cdot\hat x\' & \hat y\cdot\hat y\' & \hat y\cdot\hat z\' \\\\
\hat z\cdot\hat x\' & \hat z\cdot\hat y\' & \hat z\cdot\hat z\'
\end{pmatrix}
$$

Same idea: old basis vectors dotted with the new ones.

So, the square matrix made of $\langle a^{(k)}|U|a^{(l)}\rangle$ is the **transformation matrix** from $\lbrace|a\'\rangle\rbrace$ to $\lbrace|b\'\rangle\rbrace$.

### Coefficients in the new basis

Consider

$$
|\alpha\rangle = \sum_{a\'}|a\'\rangle\langle a\'|\alpha\rangle
$$

(in the old basis). To get the expansion coefficients in the new basis, hit it with $\langle b^{(k)}|$:

$$
\begin{aligned}
\langle b^{(k)}|\alpha\rangle &= \sum_l \langle b^{(k)}|a^{(l)}\rangle\langle a^{(l)}|\alpha\rangle \\\\
&= \sum_l \langle a^{(k)}|U^\dagger|a^{(l)}\rangle\langle a^{(l)}|\alpha\rangle
\end{aligned}
$$

since $\langle b^{(k)}| = \langle a^{(k)}|U^\dagger$ (the dual of $U|a^{(k)}\rangle = |b^{(k)}\rangle$).

That's applying the transformation matrix to the coefficients in the old basis!

$$
\boxed{(\text{new}) = U^\dagger(\text{old})}
$$

## Trace

$$
\text{tr}(X) = \sum_{a\'}\langle a\'|X|a\'\rangle
$$

$\to$ the sum of its diagonal elements.

> The trace of an operator is independent of its base kets.

$$
\begin{aligned}
\sum_{a\'}\langle a\'|X|a\'\rangle &= \sum_{a\'}\sum_{b\'}\sum_{b\'\'}\langle a\'|b\'\rangle\langle b\'|X|b\'\'\rangle\langle b\'\'|a\'\rangle \\\\
&= \sum_{b\'}\sum_{b\'\'}\langle b\'\'|b\'\rangle\langle b\'|X|b\'\'\rangle \\\\
&= \sum_{b\'}\langle b\'|X|b\'\rangle
\end{aligned}
$$

(closure over $a\'$ for the second line, orthonormality of the $|b\'\rangle$ for the third).

We can also prove the following:

$$
\text{tr}(XY) = \text{tr}(YX), \qquad \text{tr}(U^\dagger XU) = \text{tr}(X)
$$

$$
\text{tr}(|a\'\rangle\langle a\'\'|) = \delta_{a\'a\'\'}, \qquad \text{tr}(|b\'\rangle\langle a\'|) = \langle a\'|b\'\rangle
$$

The first one is just inserting closure in the middle,

$$
\text{tr}(XY) = \sum_{a\'}\sum_{a\'\'}\langle a\'|X|a\'\'\rangle\langle a\'\'|Y|a\'\rangle = \sum_{a\'\'}\langle a\'\'|YX|a\'\'\rangle = \text{tr}(YX)
$$

and the second one follows from it: $\text{tr}(U^\dagger XU) = \text{tr}(XUU^\dagger) = \text{tr}(X)$.

## Diagonalization

Assume we know $\langle a\'\'|B|a\'\rangle$ $\to$ the matrix elements of $\hat B$ in the old basis. How do we find its eigenvalues and eigenkets now? Find a unitary matrix ($U^\dagger U = 1$) that diagonalizes $\hat B$.

We want $b\'$ and $|b\'\rangle$ from

$$
\hat B|b\'\rangle = b\'|b\'\rangle
$$

First we rewrite this for matrices (insert closure and hit with $\langle a\'\'|$):

$$
\sum_{a\'}\langle a\'\'|B|a\'\rangle\langle a\'|b\'\rangle = b\'\langle a\'\'|b\'\rangle
$$

$$
\begin{pmatrix}
B_{11} & B_{12} & B_{13} & \cdots \\\\
B_{21} & B_{22} & B_{23} & \cdots \\\\
\vdots & \vdots & \vdots & \ddots
\end{pmatrix}
\begin{pmatrix} C_1^{(l)} \\\\ C_2^{(l)} \\\\ \vdots \end{pmatrix}
= b^{(l)}\begin{pmatrix} C_1^{(l)} \\\\ C_2^{(l)} \\\\ \vdots \end{pmatrix}
$$

with

$$
B_{ij} = \langle a^{(i)}|B|a^{(j)}\rangle, \qquad C_k^{(l)} = \langle a^{(k)}|b^{(l)}\rangle
$$

This is the matrix rep. Non-trivial solutions for $C_k^{(l)}$ are possible iff

$$
\boxed{\det(B - \lambda I) = 0}
$$

$\to$ solving this gives the eigenvalues $b^{(l)}$. Knowing $b^{(l)}$, we can find $C_k^{(l)}$.

For this to work, $B$ must be Hermitian ($B = B^\dagger$).

Notice that $C_k^{(l)} = \langle a^{(k)}|b^{(l)}\rangle$ are exactly the transformation matrix elements $\langle a^{(k)}|U|a^{(l)}\rangle$. So finding the eigenvectors **is** finding $U$.

But what does diagonalizing a matrix mean?

$$
A \to PDP^{-1}
$$

$\to$ this is diag., where $P \to$ eigenvectors (as columns) and $D \to$ eigenvalues (on the diagonal).

## Unitary equivalent observables

> **Theorem:** Consider two sets of orthonormal bases $\lbrace|a\'\rangle\rbrace$ and $\lbrace|b\'\rangle\rbrace$, with $\hat U$ telling us the transform. With this we may construct a "unitary transform" of $\hat A$ as $UAU^{-1}$. Then $\hat A$ and $UAU^{-1}$ are said to be **unitary equivalent observables**.

The eigenvalue equation for $\hat A$:

$$
\hat A|a^{(l)}\rangle = a^{(l)}|a^{(l)}\rangle
$$

$$
\implies UAU^{-1}U|a^{(l)}\rangle = a^{(l)}U|a^{(l)}\rangle
$$

But wtf is $U^{-1}$? $\to$ Turns out that for unitary operators, $U^\dagger = U^{-1}$.

$$
\implies (UAU^\dagger)|b^{(l)}\rangle = a^{(l)}|b^{(l)}\rangle
$$

$\implies |b^{(l)}\rangle$ is the eigenket of $UAU^\dagger$, and the $a^{(l)}$ are the eigenvalues of $UAU^\dagger$ (the same as $\hat A$'s).

And we know by definition

$$
\hat B|b^{(l)}\rangle = b^{(l)}|b^{(l)}\rangle
$$

$\implies \hat B$ and $UAU^\dagger$ are simultaneously diagonalizable.

But is $UAU^{-1}$ (or $UAU^\dagger$) $= \hat B$? For physical cases, yes. Always? No.

---

[← Incompatible observables and the general uncertainty relation](@/notes/quantum_11_incompatible_observables.md) | Next: [Translations and momentum →](@/notes/quantum_13_translations_and_momentum.md)
