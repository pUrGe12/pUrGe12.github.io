+++
title = "Operators, commutators and outer products"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Operators

- Observables are represented as operators.

> Obviously not all operators are observables.

An operator acts on a ket from the left:

$$
\hat X\cdot\left(|\alpha\rangle\right) = \hat X|\alpha\rangle
$$

↳ another ket.

Two operators $\hat X$ and $\hat Y$ are equal iff

$$
\hat X|\alpha\rangle = \hat Y|\alpha\rangle
$$

for any **arbitrary ket in the ket space**.

$\hat X$ is a NULL operator if $\hat X|\alpha\rangle = 0$ $\forall |\alpha\rangle$ in ket space.

## Associative and commutative

$$
\hat X + \hat Y = \hat Y + \hat X
$$

and,

$$
\hat X + (\hat Y + \hat Z) = (\hat X + \hat Y) + \hat Z
$$

Most operators are linear (except time reversal, forget that):

$$
\hat X\left(c_\alpha|\alpha\rangle + c_\beta|\beta\rangle\right) = c_\alpha\hat X|\alpha\rangle + c_\beta\hat X|\beta\rangle
$$

## Operators acting on bras

For a bra, the operator acts from the right:

$$
\left(\langle\alpha|\right)\hat X = \langle\alpha|\hat X
$$

↳ another bra.

Note for an operator $\hat X$, the ket $\hat X|\alpha\rangle$ and bra $\langle\alpha|\hat X$ are **NOT** duals. In fact:

$$
\hat X|\alpha\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha|\hat X^\dagger
$$

where

> $\hat X^\dagger$ is the **adjoint** of $\hat X$

An operator $\hat X$ is **Hermitian** if $\hat X = \hat X^\dagger$

$$
\implies \hat X|\alpha\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha|\hat X \quad \text{iff } \hat X \text{ is Hermitian}
$$

## Multiplication of operators

$$
\hat X\hat Y \neq \hat Y\hat X
$$

(order of application matters). However they are **associative**!

$$
\hat X(\hat Y\hat Z) = (\hat X\hat Y)\hat Z = \hat X\hat Y\hat Z
$$

and

$$
\begin{aligned}
\hat X\left(\hat Y\left(|\alpha\rangle\right)\right) &= \hat X\left(\hat Y|\alpha\rangle\right) = \hat X\hat Y|\alpha\rangle \\\\
\left(\left(\langle\alpha|\right)\hat X\right)\hat Y &= \left(\langle\alpha|\hat X\right)\hat Y = \langle\alpha|\hat X\hat Y
\end{aligned}
$$

note:

$$
(\hat X\hat Y)^\dagger = \hat Y^\dagger\hat X^\dagger
$$

as,

$$
\hat X\hat Y|\alpha\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha|\hat Y^\dagger\hat X^\dagger
$$

## Commutator and anti-commutator

Since the order matters, it's useful to have a way of measuring *how much* it matters. The **commutator**:

$$
[\hat X, \hat Y] \equiv \hat X\hat Y - \hat Y\hat X
$$

and the **anti-commutator**:

$$
\lbrace\hat X, \hat Y\rbrace \equiv \hat X\hat Y + \hat Y\hat X
$$

- If $[\hat X, \hat Y] = 0$, the operators commute and the order doesn't matter. Observables like that are called [compatible](@/notes/quantum_09_compatible_observables.md).
- $[\hat X, \hat Y] = -[\hat Y, \hat X]$ while $\lbrace\hat X, \hat Y\rbrace = \lbrace\hat Y, \hat X\rbrace$
- Any product splits into the two: $\hat X\hat Y = \frac{1}{2}[\hat X, \hat Y] + \frac{1}{2}\lbrace\hat X, \hat Y\rbrace$

## Outer product

Can we multiply a bra and a ket? ↳ one way is the inner product $\langle\alpha|\beta\rangle$. The other way around:

$$
\left(|\beta\rangle\right)\cdot\left(\langle\alpha|\right) = |\beta\rangle\langle\alpha|
$$

> This is called the **outer product**.

> An outer product of a bra and ket is an **operator** $\to$ fundamentally diff. from $\langle\alpha|\beta\rangle \in \mathbb{C}$.

Now, we said that $|\beta\rangle\langle\alpha|$ is an operator. If this acts on a ket:

$$
\left(|\beta\rangle\langle\alpha|\right)\cdot|\gamma\rangle = |\beta\rangle\langle\alpha|\gamma\rangle
$$

(through associativity) and since $\langle\alpha|\gamma\rangle \in \mathbb{C}$, it's another ket.

That is why $|\beta\rangle\langle\alpha|$ is an operator. Also notice

> how the state changes to $|\beta\rangle$ with a "new" constant $\langle\alpha|\gamma\rangle$ from $|\gamma\rangle$.

### Adjoint of an outer product

$$
\hat X|\alpha\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha|\hat X^\dagger
$$

$$
\begin{aligned}
\implies \left(|\beta\rangle\langle\alpha|\right)|\gamma\rangle &\overset{\text{D.C.}}{\longleftrightarrow} \langle\gamma|\left(|\beta\rangle\langle\alpha|\right)^\dagger \\\\
&= \langle\gamma|\left(|\alpha\rangle\langle\beta|\right)
\end{aligned}
$$

Why?

$$
\begin{aligned}
|\beta\rangle\langle\alpha|\gamma\rangle &\overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha|\gamma\rangle^{\ast}\langle\beta| \\\\
&= \langle\gamma|\left(|\alpha\rangle\langle\beta|\right)
\end{aligned}
$$

as $\langle\alpha|\gamma\rangle = \langle\gamma|\alpha\rangle^{\ast}$.

Hence proved that if $\hat X = |\beta\rangle\langle\alpha|$ then $\hat X^\dagger = |\alpha\rangle\langle\beta|$.

## Illegal products

> **Illegal products**

- $|\alpha\rangle\cdot|\beta\rangle$ $\to$ **illegal** iff $|\alpha\rangle$ and $|\beta\rangle$ belong to the same vector space.
- $|\alpha\rangle\otimes|\beta\rangle$ or $|\alpha\rangle|\beta\rangle$ $\to$ **legal** iff $|\alpha\rangle$ and $|\beta\rangle$ are kets from diff. vector spaces.

Eg. $|\alpha\rangle$ is from the vector space for $e^-$ spin and $|\beta\rangle$ is from the $e^-$ orbital angular momentum. Or for two diff. particles and so on.

## Sandwiching an operator

Also note:

$$
\underbrace{\left(\langle\beta|\right)}\_{\text{bra}}\cdot\underbrace{\left(\hat X|\alpha\rangle\right)}\_{\text{ket}} = \underbrace{\left(\langle\beta|\hat X\right)}\_{\text{bra}}\underbrace{\left(|\alpha\rangle\right)}\_{\text{ket}} = \langle\beta|\hat X|\alpha\rangle
$$

since $\hat X$ can be first operated on the bra or the ket, and we'll end up with a complex no.

Note:

$$
\langle\beta|\cdot\left(\hat X|\alpha\rangle\right) = \left[\left(\langle\alpha|\hat X^\dagger\right)\cdot|\beta\rangle\right]^{\ast}
$$

$$
\boxed{\langle\beta|\hat X|\alpha\rangle = \langle\alpha|\hat X^\dagger|\beta\rangle^{\ast}}
$$

If $\hat X$ is Hermitian, $\hat X = \hat X^\dagger$

$$
\implies \langle\beta|\hat X|\alpha\rangle = \langle\alpha|\hat X|\beta\rangle^{\ast}
$$

---

[← Bras, the dual space and inner products](@/notes/quantum_03_bras_and_inner_products.md) | Next: [Eigenkets, base kets and the identity operator →](@/notes/quantum_05_eigenkets_and_base_kets.md)
