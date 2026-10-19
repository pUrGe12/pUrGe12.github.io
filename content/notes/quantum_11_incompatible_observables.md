+++
title = "Incompatible observables and the general uncertainty relation"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Incompatible observables

↳ No simultaneous eigenkets $\to$ proof by contradiction.

If we did have $[\hat A, \hat B] \neq 0$ and $\hat A, \hat B$ still have simultaneous eigenkets, then

$$
\begin{aligned}
\hat A\hat B|a\',b\'\rangle &= \hat A b\'|a\',b\'\rangle = a\'b\'|a\',b\'\rangle \\\\
&= \hat B\hat A|a\',b\'\rangle
\end{aligned}
$$

$$
\implies \hat A\hat B|a\',b\'\rangle = \hat B\hat A|a\',b\'\rangle
$$

or $\hat A\hat B - \hat B\hat A = 0$ $\to$ which is a contradiction.

> There is a **subspace** in the ket space such that $|a\',b\'\rangle$ holds / makes sense even when $[\hat A, \hat B] \neq 0$.

For example in the $l = 0$ state (s-state), $L_x$ and $L_z$ don't commute, but $l = 0$ is a simultaneous eigenket (all the components give 0 there). More on $l$ in the [angular momentum notes](@/notes/quantum_15_angular_momentum.md).

## Sequential measurements

```text
          ┌─────┐   a'    ┌─────┐   b'    ┌─────┐   c'
   ─────► │  A  │ ──────► │  B  │ ──────► │  C  │ ──────►
          │     │ ──► ■   │     │ ──► ■   │     │ ──► ■
          └─────┘  rest   └─────┘  rest   └─────┘  rest
                 blocked         blocked         blocked
```

What's the prob. of obtaining $|c\'\rangle$?

We need $|a\'\rangle \to |b\'\rangle$ and $|b\'\rangle \to |c\'\rangle$:

$$
|a\'\rangle \to |b\'\rangle \implies |\langle b\'|a\'\rangle|^2, \qquad |b\'\rangle \to |c\'\rangle \implies |\langle c\'|b\'\rangle|^2
$$

$$
\therefore \text{total prob. of } |c\'\rangle = |\langle c\'|b\'\rangle|^2|\langle b\'|a\'\rangle|^2
$$

Now, we had blocked some $|b\'\rangle$ routes. What if we consider them one by one (and add up all the routes)?

$$
\sum_{b\'}|\langle c\'|b\'\rangle|^2|\langle b\'|a\'\rangle|^2 = \sum_{b\'}\langle c\'|b\'\rangle\langle b\'|a\'\rangle\langle a\'|b\'\rangle\langle b\'|c\'\rangle
$$

But if we remove the $B$ filter entirely, the prob. becomes $|\langle c\'|a\'\rangle|^2$:

$$
|\langle c\'|a\'\rangle|^2 = \left|\sum_{b\'}\langle c\'|b\'\rangle\langle b\'|a\'\rangle\right|^2
$$

(same imagined $|b\'\rangle$, we just inserted closure).

> **Note the two are different!** So going through all routes $\neq$ as if not going through it at all.

In both cases the pure $|a\'\rangle$ beam can be regarded as

$$
|a\'\rangle = \sum_{b\'}|b\'\rangle\langle b\'|a\'\rangle
$$

(not an eigenvalue equation). This is what we do in the second case, as $\langle c\'|a\'\rangle = \sum_{b\'}\langle c\'|b\'\rangle\langle b\'|a\'\rangle$. By actually recording the $|\langle b\'|a\'\rangle|^2$ prob. values, we change things!!

When are these expressions equal? When $[\hat A, \hat B] = 0$ or $[\hat B, \hat C] = 0$, in absence of degeneracy.

> $\therefore$ for incompatible measurements only does "looking" f\*ck it up.

## The general uncertainty relation

We did the dispersion in the [uncertainty notes](@/notes/quantum_10_uncertainty_relation.md). The general uncertainty relation (insane) is:

$$
\boxed{\langle(\Delta A)^2\rangle\langle(\Delta B)^2\rangle \geq \frac{1}{4}\left|\langle[\hat A, \hat B]\rangle\right|^2}
$$

Why? 3 lemmas:

1. Cauchy-Schwarz
2. $\langle A\rangle$ is real if $\hat A$ is Hermitian
3. if $\hat A = -\hat A^\dagger$ (anti-Hermitian), the expectation value is purely imaginary.

For 2 and 3, use $\langle\beta|\hat X|\alpha\rangle = \langle\alpha|\hat X^\dagger|\beta\rangle^{\ast}$ from the [operators notes](@/notes/quantum_04_operators.md#sandwiching-an-operator):

$$
\hat A = \hat A^\dagger \implies \langle\alpha|\hat A|\alpha\rangle = \langle\alpha|\hat A|\alpha\rangle^{\ast} \implies \text{real}
$$

$$
\hat A = -\hat A^\dagger \implies \langle\alpha|\hat A|\alpha\rangle = -\langle\alpha|\hat A|\alpha\rangle^{\ast} \implies \text{purely imaginary}
$$

Cauchy-Schwarz is:

$$
\langle\alpha|\alpha\rangle\langle\beta|\beta\rangle \geq |\langle\alpha|\beta\rangle|^2
$$

(same as $|\vec a|^2|\vec b|^2 \geq |\vec a\cdot\vec b|^2$ for ordinary vectors). Can intuitively think of it as measuring $\langle\alpha|\alpha\rangle$, then measuring a $|b\'\rangle$ beam after $B$ and taking the product. Both are "large" values prob. wise, and $|\langle\alpha|\beta\rangle|^2$ will always be a smaller or at max equal prob.

Now we use Cauchy-Schwarz **and** the following definitions:

$$
|\alpha\rangle = \Delta A|\ \rangle, \qquad |\beta\rangle = \Delta B|\ \rangle
$$

where $|\ \rangle$ is any ket.

$$
\implies \langle(\Delta A)^2\rangle\langle(\Delta B)^2\rangle \geq |\langle\Delta A\Delta B\rangle|^2
$$

Why? Since $\Delta A$ is Hermitian,

$$
\langle\alpha|\alpha\rangle = \langle\ |\Delta A^\dagger\Delta A|\ \rangle = \langle\ |(\Delta A)^2|\ \rangle = \langle(\Delta A)^2\rangle
$$

↳ the definition of expectation value. The same goes for $\langle\beta|\beta\rangle$, and $\langle\alpha|\beta\rangle = \langle\Delta A\Delta B\rangle$.

Now to evaluate $|\langle\Delta A\Delta B\rangle|^2$ we use the fact (from the [commutator notes](@/notes/quantum_04_operators.md#commutator-and-anti-commutator)):

$$
\Delta A\Delta B = \frac{1}{2}[\Delta A, \Delta B] + \frac{1}{2}\lbrace\Delta A, \Delta B\rbrace
$$

- The commutator $[\Delta A, \Delta B] = [A, B]$, since $\langle A\rangle$ and $\langle B\rangle$ are just numbers.
- $[A, B]$ is anti-Hermitian: $[A, B]^\dagger = (AB - BA)^\dagger = BA - AB = -[A, B]$
- $\lbrace\Delta A, \Delta B\rbrace$ is Hermitian (due to the positive sign).

$$
\implies \langle\Delta A\Delta B\rangle = \underbrace{\frac{1}{2}\langle[A, B]\rangle}\_{\text{purely imaginary}} + \underbrace{\frac{1}{2}\langle\lbrace\Delta A, \Delta B\rbrace\rangle}\_{\text{purely real}}
$$

$$
|\langle\Delta A\Delta B\rangle|^2 = \frac{1}{4}|\langle[A, B]\rangle|^2 + \frac{1}{4}|\langle\lbrace\Delta A, \Delta B\rbrace\rangle|^2
$$

↳ sum of squares, hence. Throwing away the second (non-negative) term can only make the right side smaller, and this proves the inequality we saw.

---

[← The uncertainty relation](@/notes/quantum_10_uncertainty_relation.md) | Next: [Change of basis and the transformation matrix →](@/notes/quantum_12_change_of_basis.md)
