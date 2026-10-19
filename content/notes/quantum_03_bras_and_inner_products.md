+++
title = "Bras, the dual space and inner products"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

So, we saw the "ket" space. Let's now talk about the **bra** space. This is "dual to" the ket space.

## Dual correspondence

> Every ket in ket space has a bra in bra space.

$$
\boxed{|\alpha\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha|}
$$

Same with eigenkets and eigenbras:

$$
|a\'\rangle, |a\'\'\rangle, \dots \overset{\text{D.C.}}{\longleftrightarrow} \langle a\'|, \langle a\'\'|, \dots
$$

and

$$
|\alpha\rangle + |\beta\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle\alpha| + \langle\beta|
$$

The bra space is some mirror of the ket space.

> **Note:** the bra dual of $c|\alpha\rangle$ is $c^{\ast}\langle\alpha|$

In general,

$$
c_\alpha|\alpha\rangle + c_\beta|\beta\rangle \overset{\text{D.C.}}{\longleftrightarrow} c_\alpha^{\ast}\langle\alpha| + c_\beta^{\ast}\langle\beta|
$$

you must take the complex conjugate of the coefficient.

## Inner product

> **Inner product** $\to$ taken of a bra and a ket.

$$
\langle\beta|\alpha\rangle = \left(\langle\beta|\right)\cdot\left(|\alpha\rangle\right)
$$

(bra $\cdot$ ket). This product in general is a complex no. We always take one vector from bra space $\times$ one vector from ket space.

Two fundamental properties:

1. $\langle\beta|\alpha\rangle = \langle\alpha|\beta\rangle^{\ast}$
2. $\langle\alpha|\alpha\rangle \geq 0$

> $\langle\alpha|\alpha\rangle$ must be a real number (no complex part). Put $\beta = \alpha$ in (1) and you get $\langle\alpha|\alpha\rangle = \langle\alpha|\alpha\rangle^{\ast}$.

## Orthogonality

Two kets $|\alpha\rangle$ and $|\beta\rangle$ are orthogonal iff

$$
\langle\alpha|\beta\rangle = 0
$$

and then (from property 1) $\langle\beta|\alpha\rangle = 0 = \langle\alpha|\beta\rangle$.

## Normalization

The normalized ket $|\tilde\alpha\rangle$ is given by:

$$
|\tilde\alpha\rangle = \left(\frac{1}{\sqrt{\langle\alpha|\alpha\rangle}}\right)|\alpha\rangle
$$

Normalized means

$$
\langle\tilde\alpha|\tilde\alpha\rangle = 1
$$

In general $\sqrt{\langle\alpha|\alpha\rangle}$ is called the **norm** of $|\alpha\rangle$.

Normalization is imp. before using kets for physical states, as $|\alpha\rangle$ and $c|\alpha\rangle$ represent the same state.

---

[← Kets and the Hilbert space](@/notes/quantum_02_kets_and_hilbert_space.md) | Next: [Operators, commutators and outer products →](@/notes/quantum_04_operators.md)
