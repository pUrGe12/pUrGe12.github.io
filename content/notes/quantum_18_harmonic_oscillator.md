+++
title = "The simple harmonic oscillator"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## The setup

$\to$ Any potential well can be approximated as a SHO (near its minimum, $V(x) \approx V(x_0) + \frac{1}{2}V\'\'(x_0)(x - x_0)^2$). We'll see this later as well.

```text
   ┃
   ┃                   ┌─────┐
   ┃──/\/\/\/\/\/\/\/──│  m  │ ──► x
   ┃         k         └─────┘
   ┃
```

For the SHO:

$$
\boxed{\hat H = \frac{\hat p^2}{2m} + \frac{m\omega^2\hat x^2}{2}}, \qquad \omega = \sqrt{\frac{k}{m}}
$$

$\to$ $\omega$ is the angular freq. of the classical oscillator.

> $\hat x$ and $\hat p$ are Hermitian.

## Annihilation and creation operators

We now define two new operators:

$$
\boxed{a = \sqrt{\frac{m\omega}{2\hbar}}\left(\hat x + \frac{i\hat p}{m\omega}\right)}, \qquad \boxed{a^\dagger = \sqrt{\frac{m\omega}{2\hbar}}\left(\hat x - \frac{i\hat p}{m\omega}\right)}
$$

$\to$ the **annihilation operator** and the **creation operator**. We can quickly see that

$$
\boxed{[a, a^\dagger] = 1}
$$

since only the cross terms survive:

$$
[a, a^\dagger] = \frac{m\omega}{2\hbar}\left(-\frac{i}{m\omega}[\hat x, \hat p] + \frac{i}{m\omega}[\hat p, \hat x]\right) = \frac{m\omega}{2\hbar}\cdot\left(-\frac{2i}{m\omega}\right)(i\hbar) = 1
$$

## The number operator

We also define

$$
\boxed{N = a^\dagger a}
$$

$\to$ the **number operator**.

$$
a^\dagger a = \frac{m\omega}{2\hbar}\left(\hat x^2 + \frac{\hat p^2}{m^2\omega^2}\right) + \frac{i}{2\hbar}[\hat x, \hat p]
$$

(the cross terms don't cancel, as $\hat x\hat p \neq \hat p\hat x$). With $[\hat x, \hat p] = i\hbar$,

$$
\boxed{a^\dagger a = \frac{\hat H}{\hbar\omega} - \frac{1}{2}} \implies N = \frac{\hat H}{\hbar\omega} - \frac{1}{2}
$$

or

$$
\boxed{\hat H = \hbar\omega\left(N + \frac{1}{2}\right)}
$$

We also denote an energy eigenket of $N$ by its eigenvalue $n$:

$$
\boxed{N|n\rangle = n|n\rangle}
$$

$\to$ why? Because $\hat H$ is just a function of $N$, so they share eigenkets. Now,

$$
\hat H|n\rangle = \hbar\omega\left(N + \frac{1}{2}\right)|n\rangle = \hbar\omega\left(n + \frac{1}{2}\right)|n\rangle
$$

$$
\implies \boxed{E_n = \left(n + \frac{1}{2}\right)\hbar\omega}
$$

$\to$ the energy eigenvalues.

## Ladder relations

We can show that

$$
[N, a] = [a^\dagger a, a] = a^\dagger[a, a] + [a^\dagger, a]a = -a
$$

and

$$
[N, a^\dagger] = a^\dagger
$$

$$
\implies \boxed{Na^\dagger|n\rangle = \left([N, a^\dagger] + a^\dagger N\right)|n\rangle = (n + 1)a^\dagger|n\rangle}
$$

and

$$
\boxed{Na|n\rangle = (n - 1)a|n\rangle}
$$

Sit with this.

These relations imply that $a^\dagger|n\rangle$ ($a|n\rangle$) is also an eigenket of $N$, with the eigenvalue increased (or decreased) by one. Same story as the [angular momentum ladders](@/notes/quantum_15_angular_momentum.md#ladder-operators).

We can say

$$
\boxed{a|n\rangle = c|n - 1\rangle}
$$

because we denote the normalized eigenket corresponding to the eigenvalue $n - 1$ as $|n - 1\rangle$:

$$
N|n - 1\rangle = (n - 1)|n - 1\rangle
$$

For a quantum harmonic oscillator, the energy spectrum (and the spectrum of $n$) is non-degenerate $\implies$ there is only one unique quantum state, up to a scalar constant, for each eigenvalue.

> Since both $a|n\rangle$ and $|n - 1\rangle$ have the same eigenvalue $(n - 1)$, they must be the same state up to a constant.

To find $c$:

$$
a|n\rangle = c|n - 1\rangle \implies \langle n|a^\dagger = c^{\ast}\langle n - 1|
$$

$$
\implies \langle n|a^\dagger a|n\rangle = |c|^2
$$

(assuming $|n - 1\rangle$ is normalized). And $a^\dagger a = N$, with $N|n\rangle = n|n\rangle$:

$$
\implies \langle n|n|n\rangle = |c|^2 \implies \boxed{n = |c|^2}
$$

(assuming $|n\rangle$ is normalized). Taking $c$ to be real and positive, we obtain

$$
\boxed{a|n\rangle = \sqrt n|n - 1\rangle}
$$

Similarly (using $aa^\dagger = N + 1$),

$$
\boxed{a^\dagger|n\rangle = \sqrt{n + 1}|n + 1\rangle}
$$

## n is a non-negative integer

If we keep applying the annihilation operator here,

$$
\begin{aligned}
a^2|n\rangle &= \sqrt{n(n - 1)}|n - 2\rangle \\\\
a^3|n\rangle &= \sqrt{n(n - 1)(n - 2)}|n - 3\rangle
\end{aligned}
$$

$\to$ the sequence will terminate if $n$ is an integer.

We also have the positivity requirement for the norm of $a|n\rangle$:

$$
n = \langle n|N|n\rangle = \left(\langle n|a^\dagger\right)\left(a|n\rangle\right) \geq 0
$$

> $\therefore$ $n$ can never be negative. So, the sequence must terminate with $n = 0$, and $n$ is a non-negative integer.

(If $n$ wasn't an integer, applying $a$ enough times would land us on a state with negative $n$, which can't exist.)

So, the smallest value of $n$ is zero, and the ground state energy becomes

$$
\boxed{E_0 = \frac{1}{2}\hbar\omega}
$$

## Building every state from the ground state

Now, we can successively apply creation to the ground state:

$$
\begin{aligned}
a^\dagger|0\rangle &= |1\rangle \\\\
a^\dagger|1\rangle &= \sqrt 2|2\rangle \implies |2\rangle = \frac{a^\dagger|1\rangle}{\sqrt 2} = \frac{(a^\dagger)^2}{\sqrt 2}|0\rangle \\\\
a^\dagger|2\rangle &= \sqrt 3|3\rangle \implies |3\rangle = \frac{(a^\dagger)^3}{\sqrt{2\cdot 3}}|0\rangle
\end{aligned}
$$

$$
\implies \boxed{|n\rangle = \frac{(a^\dagger)^n}{\sqrt{n!}}|0\rangle}
$$

$\to$ the $n$-th state.

Now we have simultaneous eigenkets of $N$ and $\hat H$, with energy eigenvalues

$$
\boxed{E_n = \left(n + \frac{1}{2}\right)\hbar\omega, \qquad n \in \lbrace 0, 1, 2, \dots\rbrace}
$$

## Matrix elements

So, from $a|n\rangle = \sqrt n|n - 1\rangle$ and $a^\dagger|n\rangle = \sqrt{n + 1}|n + 1\rangle$ (and orthogonality):

$$
\boxed{\langle n\'|a|n\rangle = \sqrt n\delta_{n\',n-1}, \qquad \langle n\'|a^\dagger|n\rangle = \sqrt{n + 1}\delta_{n\',n+1}}
$$

For example,

$$
a \doteq \begin{pmatrix}
0 & 1 & 0 & 0 & \cdots \\\\
0 & 0 & \sqrt 2 & 0 & \cdots \\\\
0 & 0 & 0 & \sqrt 3 & \cdots \\\\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}
$$

Rewriting $\hat x$ and $\hat p$ with $a$ and $a^\dagger$ (just invert the definitions),

$$
\hat x = \sqrt{\frac{\hbar}{2m\omega}}\left(a + a^\dagger\right), \qquad \hat p = i\sqrt{\frac{m\hbar\omega}{2}}\left(-a + a^\dagger\right)
$$

we get the matrix elements for $\hat x$ and $\hat p$:

$$
\boxed{
\begin{aligned}
\langle n\'|\hat x|n\rangle &= \sqrt{\frac{\hbar}{2m\omega}}\left(\sqrt n\delta_{n\',n-1} + \sqrt{n + 1}\delta_{n\',n+1}\right) \\\\
\langle n\'|\hat p|n\rangle &= i\sqrt{\frac{m\hbar\omega}{2}}\left(-\sqrt n\delta_{n\',n-1} + \sqrt{n + 1}\delta_{n\',n+1}\right)
\end{aligned}
}
$$

$\to$ literally just replace $a$ and $a^\dagger$ with their matrix elements and factor out the constants.

Only $N$ and $\hat H$ are diagonal in the $|n\rangle$ basis. $a$ and $a^\dagger$ each live on a single line just off the diagonal, and $\hat x$ and $\hat p$ (mixes of both) live on both of those lines.

## The ground state wave function

Can we obtain the energy eigenfunctions in position space?

So, we know

$$
a|0\rangle = 0
$$

$\to$ the ground state. And $a = \sqrt{\frac{m\omega}{2\hbar}}\left(\hat x + \frac{i\hat p}{m\omega}\right)$

$$
\implies \left(\hat x + \frac{i\hat p}{m\omega}\right)|0\rangle = 0
$$

$\to$ project this onto position space with $\langle x\'|$:

$$
\implies \langle x\'|\left(\hat x + \frac{i\hat p}{m\omega}\right)|0\rangle = 0 \implies \langle x\'|\hat x|0\rangle + \frac{i}{m\omega}\langle x\'|\hat p|0\rangle = 0
$$

The first term is $x\'\langle x\'|0\rangle$ (from the eigenvalue equation), and the second one we know from the [wave functions notes](@/notes/quantum_14_wave_functions.md#momentum-in-the-position-basis): $\langle x\'|\hat p|\alpha\rangle = -i\hbar\frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle$.

$$
\implies x\'\langle x\'|0\rangle + \frac{i}{m\omega}\left(-i\hbar\frac{\partial}{\partial x\'}\langle x\'|0\rangle\right) = 0
$$

$$
\implies \boxed{\frac{\hbar}{m\omega}\frac{\partial}{\partial x\'}\langle x\'|0\rangle + x\'\langle x\'|0\rangle = 0}
$$

$\to$ that's the equation. Let

$$
x_0 = \sqrt{\frac{\hbar}{m\omega}}
$$

$\to$ this is the length scale of the problem / oscillations.

$$
\implies \boxed{\left(x\' + x_0^2\frac{\partial}{\partial x\'}\right)\langle x\'|0\rangle = 0}
$$

Now, we know $\langle x\'|0\rangle = \psi_0(x\')$

$$
\implies \int\frac{d\psi_0}{\psi_0} = -\int\frac{x\'}{x_0^2}dx\'
$$

$\to$ solve it:

$$
\ln\psi_0 = -\frac{x\'^2}{2x_0^2} + \text{const} \implies \psi_0(x\') = A\exp\left(-\frac{1}{2}\left(\frac{x\'}{x_0}\right)^2\right)
$$

and normalizing, $\int|\psi_0|^2dx\' = A^2\sqrt\pi x_0 = 1$, so $A = \frac{1}{\pi^{1/4}\sqrt{x_0}}$:

$$
\boxed{\langle x\'|0\rangle = \frac{1}{\pi^{1/4}\sqrt{x_0}}\exp\left(-\frac{1}{2}\left(\frac{x\'}{x_0}\right)^2\right)}
$$

This is a **Gaussian** wave function for the ground state: the [Gaussian wave packet](@/notes/quantum_14_wave_functions.md#gaussian-wave-packets) with $k = 0$ and $d = x_0$, so the ground state is a minimum uncertainty state.

The highest prob. is at the centre, and not at the edges like classical systems. We can find the excited states as well, which is the [next notes](@/notes/quantum_19_harmonic_oscillator_wave_functions.md).

---

[← Energy eigenkets and spin precession](@/notes/quantum_17_energy_eigenkets.md) | Next: [Harmonic oscillator wave functions →](@/notes/quantum_19_harmonic_oscillator_wave_functions.md)
