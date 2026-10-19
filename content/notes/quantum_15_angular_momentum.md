+++
title = "Angular momentum"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

The plan: general angular momentum states $\to$ the eigenvalues and eigenkets of $\vec J^2$ and $J_z$ $\to$ matrix elements. Before that, let's talk about the definition of angular momentum.

## Angular momentum as the generator of rotations

- Classical $\to$ generator of rotations
- Quantum $\to$ a helper for the generation of rotations

In classical mechanics, $\vec J = \vec x\times\vec p$ $\to$ but in quantum we have ideas like **spin** angular momentum, which is unrelated to $\vec x$ or $\vec p$! So we define angular momentum through rotations instead:

$$
\boxed{\mathcal D(\hat n, d\phi) = 1 - i\left(\frac{\vec J\cdot\hat n}{\hbar}\right)d\phi}
$$

> This operator is the generator of infinitesimal rotations (about the axis $\hat n$, by an angle $d\phi$), and $\vec J$ is the angular momentum.

For finite rotations (about $\hat z$, say):

$$
\boxed{\mathcal D_z(\phi) = \exp\left(-\frac{iJ_z\phi}{\hbar}\right)}
$$

Notice the similarity to [finite translations](@/notes/quantum_13_translations_and_momentum.md#finite-translations), $\mathcal J(\Delta x\'\hat x) = \exp\left(-\frac{ip_x\Delta x\'}{\hbar}\right)$.

Applying the same ideas we used for $\mathcal J(\Delta x)$ to $\mathcal D_z(\phi)$ (expand $1 + x + \frac{x^2}{2}$ to 2nd order, ignore $\phi^3$), we get

$$
\boxed{[J_x, J_y] = i\hbar J_z, \qquad [J_i, J_j] = i\hbar\varepsilon_{ijk}J_k}
$$

$\to$ because rotations do not commute (rotate a book by $90^\circ$ about $\hat x$ then $\hat y$, vs $\hat y$ then $\hat x$).

Quick sketch of where it comes from: classical rotation matrices satisfy, to 2nd order in a small angle $\varepsilon$, $R_x(\varepsilon)R_y(\varepsilon) - R_y(\varepsilon)R_x(\varepsilon) = R_z(\varepsilon^2) - 1$. We demand the same of the $\mathcal D$s:

$$
\mathcal D_x(\varepsilon)\mathcal D_y(\varepsilon) - \mathcal D_y(\varepsilon)\mathcal D_x(\varepsilon) = \mathcal D_z(\varepsilon^2) - 1
$$

With $\mathcal D_i(\varepsilon) \approx 1 - \frac{iJ_i\varepsilon}{\hbar} - \frac{J_i^2\varepsilon^2}{2\hbar^2}$, the left side is $-\frac{\varepsilon^2}{\hbar^2}[J_x, J_y]$ and the right side is $-\frac{iJ_z\varepsilon^2}{\hbar}$, so $[J_x, J_y] = i\hbar J_z$. (Compare with translations, where the same game gave $[p_x, p_y] = 0$.)

## J squared

So, we have

$$
\vec J^2 = J_xJ_x + J_yJ_y + J_zJ_z
$$

(note $[J_i, J_i] = 0$ since $\varepsilon_{iik} = 0$) and

$$
\boxed{[\vec J^2, J_i] = 0}
$$

For $J_z$, using $[AB, C] = A[B, C] + [A, C]B$:

$$
\begin{aligned}
[J_xJ_x + J_yJ_y + J_zJ_z, J_z] &= J_x[J_x, J_z] + [J_x, J_z]J_x + J_y[J_y, J_z] + [J_y, J_z]J_y \\\\
&= J_x(-i\hbar J_y) + (-i\hbar J_y)J_x + J_y(i\hbar J_x) + (i\hbar J_x)J_y \\\\
&= 0
\end{aligned}
$$

Since $\vec J^2$ and $J_z$ (or any $J_i$) commute, they must have [simultaneous eigenkets](@/notes/quantum_09_compatible_observables.md):

$$
\vec J^2|a, b\rangle = a|a, b\rangle, \qquad J_z|a, b\rangle = b|a, b\rangle
$$

($b$ is the eigenvalue of $J_z$).

## Ladder operators

To find the allowed values of $a$ and $b$, we'll work with

$$
\boxed{J_\pm \equiv J_x \pm iJ_y}
$$

$\to$ these new non-Hermitian operators are called **ladder operators**. They satisfy

$$
[J_+, J_-] = 2\hbar J_z
$$

since

$$
\begin{aligned}
[J_x + iJ_y, J_x - iJ_y] &= [J_x, J_x] - i[J_x, J_y] + i[J_y, J_x] + [J_y, J_y] \\\\
&= -2i[J_x, J_y] = -2i(i\hbar J_z) = 2\hbar J_z
\end{aligned}
$$

and,

$$
\boxed{[J_z, J_\pm] = \pm\hbar J_\pm}
$$

(as $[J_z, J_x \pm iJ_y] = i\hbar J_y \pm i(-i\hbar J_x) = \pm\hbar(J_x \pm iJ_y)$), and

$$
[\vec J^2, J_\pm] = 0
$$

$\to$ a consequence of $[\vec J^2, J_k] = 0$.

Let's see how $J_z$ acts on $J_\pm|a, b\rangle$:

$$
J_z\left(J_\pm|a, b\rangle\right) = \left([J_z, J_\pm] + J_\pm J_z\right)|a, b\rangle = (b \pm \hbar)\left(J_\pm|a, b\rangle\right)
$$

So, $J_\pm|a, b\rangle$ is an eigenket of $J_z$. We can see that the eigenvalue goes up or down by one ladder unit, $\hbar$.

Note that

$$
\vec J^2\left(J_\pm|a, b\rangle\right) = J_\pm\vec J^2|a, b\rangle = a\left(J_\pm|a, b\rangle\right)
$$

(since they commute) $\to$ no change in the eigenvalue.

$$
\implies \boxed{J_\pm|a, b\rangle = c_\pm|a, b \pm \hbar\rangle}
$$

Why only $b$? Because $J_\pm$ commutes with $\vec J^2$ but not with $J_z$.

## Eigenvalues of J squared and Jz

Apply $J_+$ $n$ times to a simultaneous eigenket of $\vec J^2$ and $J_z$. Then the $J_z$ eigenvalue increases by $n\hbar$, and the $\vec J^2$ eigenvalue is unchanged.

But for $|a, b\rangle$ there is an upper limit to the $|b|$ eigenvalue:

$$
\boxed{a \geq b^2}
$$

so, you can't keep applying $J_\pm$ indefinitely. Why? Because

$$
\vec J^2 - J_z^2 = \frac{1}{2}\left(J_+J_- + J_-J_+\right) = \frac{1}{2}\left(J_+J_+^\dagger + J_+^\dagger J_+\right)
$$

since $J_- = J_+^\dagger$. Using the dual correspondence,

$$
J_+|a, b\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle a, b|J_+^\dagger, \qquad J_+^\dagger|a, b\rangle \overset{\text{D.C.}}{\longleftrightarrow} \langle a, b|J_+
$$

so $\langle a, b|J_+^\dagger J_+|a, b\rangle$ is the squared norm of $J_+|a, b\rangle$ (and the same for the other one). $J_+J_+^\dagger$ and $J_+^\dagger J_+$ must have non-negative expectation values. Thus,

$$
\langle a, b|\vec J^2 - J_z^2|a, b\rangle = a - b^2 \geq 0 \implies a \geq b^2
$$

Anyways, this means there must be a $b_{\text{max}}$:

$$
J_+|a, b_{\text{max}}\rangle = 0
$$

but this means

$$
J_-J_+|a, b_{\text{max}}\rangle = 0
$$

However,

$$
\begin{aligned}
J_-J_+ &= (J_x - iJ_y)(J_x + iJ_y) \\\\
&= J_x^2 + J_y^2 + i[J_x, J_y] \\\\
&= \vec J^2 - J_z^2 - \hbar J_z
\end{aligned}
$$

(from $[J_i, J_j]$, and $\vec J^2 = J_x^2 + J_y^2 + J_z^2$).

$$
\implies (\vec J^2 - J_z^2 - \hbar J_z)|a, b_{\text{max}}\rangle = 0
$$

This is possible iff

$$
a - b_{\text{max}}^2 - \hbar b_{\text{max}} = 0
$$

as $\vec J^2$ gives $a$ and $J_z$ gives $b_{\text{max}}$ on $|a, b_{\text{max}}\rangle$.

$$
\implies a = b_{\text{max}}(b_{\text{max}} + \hbar) \qquad (1)
$$

And similarly, we argue that $J_-|a, b_{\text{min}}\rangle = 0 \implies J_+J_-|a, b_{\text{min}}\rangle = 0$, with $J_+J_- = \vec J^2 - J_z^2 + \hbar J_z$

$$
\implies a = b_{\text{min}}(b_{\text{min}} - \hbar) \qquad (2)
$$

From (1) and (2), we get

$$
\boxed{b_{\text{max}} = -b_{\text{min}}}
$$

(the other root, $b_{\text{max}} = b_{\text{min}} - \hbar$, is impossible since $b_{\text{max}} \geq b_{\text{min}}$).

$\therefore$ the allowed values of $b$:

$$
-b_{\text{max}} \leq b \leq b_{\text{max}}
$$

And since we can apply $J_+$ to $|a, b_{\text{min}}\rangle$ and get to $|a, b_{\text{max}}\rangle$ after $n$ times:

$$
b_{\text{max}} = b_{\text{min}} + n\hbar \implies 2b_{\text{max}} = n\hbar \implies \boxed{b_{\text{max}} = \frac{n\hbar}{2}}
$$

## The j, m labels

We define

$$
j = \frac{b_{\text{max}}}{\hbar} \implies j = \frac{n}{2}
$$

(an integer or a half-integer). Since $b$ is the eigenvalue of $J_z$, its max value is $j\hbar$

$$
\implies \boxed{a = \hbar^2j(j + 1)}
$$

$\to$ the eigenvalue of $\vec J^2$.

Define $m$ such that $b \equiv m\hbar$.

- If $j$ is an integer, all $m$ values are integers.
- If $j$ is a half-integer, all $m$ values are half-integers.

$$
m = -j, -j + 1, \dots, j - 1, j
$$

$\to$ $2j + 1$ states.

Earlier we had $\vec J^2|a, b\rangle = a|a, b\rangle$ and $J_z|a, b\rangle = b|a, b\rangle$. Now we can denote $|a, b\rangle$ with $|j, m\rangle$ to get

$$
\boxed{
\begin{aligned}
\vec J^2|j, m\rangle &= \hbar^2j(j + 1)|j, m\rangle \\\\
J_z|j, m\rangle &= m\hbar|j, m\rangle
\end{aligned}
}
$$

## The ladder coefficients

We still owe the $c_\pm$ in $J_\pm|j, m\rangle = c_\pm|j, m \pm 1\rangle$ (the [H atom notes](@/notes/quantum_20_hydrogen_atom_angular.md) use it). Same trick as before, the squared norm of $J_+|j, m\rangle$:

$$
|c_+|^2 = \langle j, m|J_+^\dagger J_+|j, m\rangle = \langle j, m|\vec J^2 - J_z^2 - \hbar J_z|j, m\rangle = \hbar^2\left(j(j + 1) - m^2 - m\right)
$$

Taking it real and positive, and doing the same with $J_+J_-$ for $c_-$:

$$
\boxed{J_\pm|j, m\rangle = \hbar\sqrt{(j \mp m)(j \pm m + 1)}|j, m \pm 1\rangle}
$$

Sanity check with spin $\frac{1}{2}$ ($j = \frac{1}{2}$, $m = -\frac{1}{2}$): $J_+|-\rangle = \hbar\sqrt{1\cdot 1}|+\rangle = \hbar|+\rangle$, the same as $S_+$ from the [spin ½ notes](@/notes/quantum_07_spin_half_matrices.md#raising-and-lowering-operators).

---

[← Wave functions in position and momentum space](@/notes/quantum_14_wave_functions.md) | Next: [Time evolution →](@/notes/quantum_16_time_evolution.md)
