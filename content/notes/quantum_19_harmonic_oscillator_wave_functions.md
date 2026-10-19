+++
title = "Harmonic oscillator wave functions and time dependence"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

We have the [ground state](@/notes/quantum_18_harmonic_oscillator.md#the-ground-state-wave-function) $\psi_0(x\') = \langle x\'|0\rangle$. Now we build everything else from it with $a^\dagger$.

## The first excited state

Now we can build the first excited state $|1\rangle$ with $|0\rangle$:

$$
a^\dagger|0\rangle = |1\rangle \implies \sqrt{\frac{m\omega}{2\hbar}}\left(\hat x - \frac{i\hat p}{m\omega}\right)|0\rangle = |1\rangle
$$

In the position projection, with $\langle x\'|$:

$$
\implies \sqrt{\frac{m\omega}{2\hbar}}\left(\langle x\'|\hat x|0\rangle - \frac{i}{m\omega}\langle x\'|\hat p|0\rangle\right) = \langle x\'|1\rangle
$$

$$
\implies \sqrt{\frac{m\omega}{2\hbar}}\left(x\'\psi_0 - \frac{i}{m\omega}\left(-i\hbar\frac{\partial}{\partial x\'}\langle x\'|0\rangle\right)\right) = \langle x\'|1\rangle
$$

$$
\implies \psi_1(x\') = \sqrt{\frac{m\omega}{2\hbar}}\left(x\'\psi_0 - \frac{\hbar}{m\omega}\frac{\partial\psi_0}{\partial x\'}\right)
$$

With $x_0^2 = \frac{\hbar}{m\omega}$ (so $\sqrt{\frac{m\omega}{2\hbar}} = \frac{1}{\sqrt 2x_0}$),

$$
\psi_1 = \frac{1}{\sqrt 2x_0}\left(x\'\psi_0 - x_0^2\frac{\partial\psi_0}{\partial x\'}\right)
$$

$$
\boxed{\psi_1(x\') = \frac{1}{\sqrt 2x_0}\left(x\' - x_0^2\frac{\partial}{\partial x\'}\right)\psi_0(x\')}
$$

Doing the derivative ($\frac{\partial\psi_0}{\partial x\'} = -\frac{x\'}{x_0^2}\psi_0$) gives $\psi_1 = \frac{\sqrt 2x\'}{x_0}\psi_0$: an odd function with one node in the middle.

## The general case

Since $|n\rangle = \frac{(a^\dagger)^n}{\sqrt{n!}}|0\rangle$, and every $a^\dagger$ turns into $\frac{1}{\sqrt 2x_0}\left(x\' - x_0^2\frac{\partial}{\partial x\'}\right)$ in the position basis, we can similarly write out $\psi_n$ as

$$
\psi_n(x\') = \frac{1}{\sqrt{n!}}\left(\frac{1}{\sqrt 2x_0}\right)^n\left(x\' - x_0^2\frac{\partial}{\partial x\'}\right)^n\psi_0(x\')
$$

↳ and if we expand / substitute for $\psi_0 = \langle x\'|0\rangle$:

$$
\boxed{\psi_n(x\') = \frac{1}{\pi^{1/4}\sqrt{2^nn!}}\left(\frac{1}{x_0^{n+1/2}}\right)\left(x\' - x_0^2\frac{\partial}{\partial x\'}\right)^n\exp\left(-\frac{1}{2}\left(\frac{x\'}{x_0}\right)^2\right)}
$$

The polynomials that pop out of $\left(x\' - x_0^2\frac{\partial}{\partial x\'}\right)^n$ acting on the Gaussian are the **Hermite polynomials**, $\psi_n \propto H_n\left(\frac{x\'}{x_0}\right)e^{-x\'^2/2x_0^2}$. More on those in [this post](@/blog/rediscovering_hermite_polynomials.md).

## Expectation values of x squared and p squared

We may also want to look at the expectation values of $x^2$ and $p^2$. From $\hat x = \sqrt{\frac{\hbar}{2m\omega}}(a + a^\dagger)$,

$$
\hat x^2 = \left[\sqrt{\frac{\hbar}{2m\omega}}(a + a^\dagger)\right]^2 = \frac{\hbar}{2m\omega}\left(a^2 + a^{\dagger 2} + a^\dagger a + aa^\dagger\right)
$$

In the ground state, only the last term has a non-vanishing expectation value ($a|0\rangle = 0$ kills $a^2$ and $a^\dagger a$, and $\langle 0|a^{\dagger 2}|0\rangle = 0$), with $\langle 0|aa^\dagger|0\rangle = 1$:

$$
\langle x^2\rangle = \frac{\hbar}{2m\omega}, \qquad \langle p^2\rangle = \frac{\hbar m\omega}{2}
$$

Recall,

$$
\begin{aligned}
\text{KE:} &\quad \left\langle\frac{p^2}{2m}\right\rangle = \frac{\hbar\omega}{4} = \frac{\langle H\rangle}{2} \\\\
\text{PE:} &\quad \left\langle\frac{m\omega^2x^2}{2}\right\rangle = \frac{\hbar\omega}{4} = \frac{\langle H\rangle}{2}
\end{aligned}
$$

$\to$ expected from the **virial theorem**.

And we also note $\langle x\rangle = \langle p\rangle = 0$, from

$$
\begin{aligned}
\langle n\'|\hat x|n\rangle &= \sqrt{\frac{\hbar}{2m\omega}}\left(\sqrt n\delta_{n\',n-1} + \sqrt{n + 1}\delta_{n\',n+1}\right) \\\\
\langle n\'|\hat p|n\rangle &= i\sqrt{\frac{m\hbar\omega}{2}}\left(-\sqrt n\delta_{n\',n-1} + \sqrt{n + 1}\delta_{n\',n+1}\right)
\end{aligned}
$$

(the diagonal $n\' = n$ elements vanish) ↳ this holds for all $n$.

So (normally it's $\langle x^2\rangle - \langle x\rangle^2$, but $\langle x\rangle = 0$ here)

$$
\langle(\Delta x)^2\rangle = \langle x^2\rangle = \frac{\hbar}{2m\omega}, \qquad \langle(\Delta p)^2\rangle = \langle p^2\rangle = \frac{\hbar m\omega}{2}
$$

$$
\implies \langle(\Delta x)^2\rangle\langle(\Delta p)^2\rangle = \frac{\hbar^2}{4}
$$

$\to$ for the ground state. The minimum, as promised by the Gaussian.

### For any n

And if we go to higher excited states,

$$
\hat x^2 = \frac{\hbar}{2m\omega}\left(a^2 + a^{\dagger 2} + \underbrace{a^\dagger a}\_{N} + aa^\dagger\right)
$$

- $a^2$ and $a^{\dagger 2}$ always give 0 expectation value:

$$
\begin{aligned}
\langle n|a^2|n\rangle &= \sqrt{n(n - 1)}\langle n|n - 2\rangle = 0 \\\\
\langle n|a^{\dagger 2}|n\rangle &= \sqrt{(n + 1)(n + 2)}\langle n|n + 2\rangle = 0
\end{aligned}
$$

↳ always 0 due to orthogonality.

- $a^\dagger a = N$: $\langle n|N|n\rangle = n$ (which is 0 when $n = 0$).

- For $aa^\dagger$:

$$
\langle n|aa^\dagger|n\rangle = \langle n|a\sqrt{n + 1}|n + 1\rangle = \sqrt{n + 1}\langle n|a|n + 1\rangle = (n + 1)\langle n|n\rangle = n + 1
$$

$$
\therefore \langle aa^\dagger\rangle = n + 1
$$

Hence, in general,

$$
\boxed{\langle x^2\rangle = \frac{\hbar}{2m\omega}(2n + 1)}
$$

And $\hat p^2 = -\frac{m\hbar\omega}{2}\left(a^2 + a^{\dagger 2} - aa^\dagger - a^\dagger a\right)$, so the same reasoning gives

$$
\boxed{\langle p^2\rangle = \frac{m\hbar\omega}{2}(2n + 1)}
$$

$$
\implies \langle(\Delta x)^2\rangle\langle(\Delta p)^2\rangle = \frac{m\hbar\omega}{2}\cdot\frac{\hbar}{2m\omega}(2n + 1)^2
$$

$$
\boxed{\langle(\Delta x)^2\rangle\langle(\Delta p)^2\rangle = \frac{\hbar^2}{4}(2n + 1)^2 = \hbar^2\left(n + \frac{1}{2}\right)^2}
$$

↳ general for any $n$.

## From quantum to classical

The ground state has its highest prob. at the centre, and not at the edges like classical systems. As $n \to \infty$, $\langle x\'|n\rangle$ wiggles faster and faster inside the potential, and the probability starts to look more like the classical one.

Classically, a particle oscillating with amplitude $A$ spends more time where it moves slowly, i.e. near the turning points. The time it spends in $dx$ is $\propto \frac{dx}{|v|}$, which gives

$$
P_{\text{cl}}(x) = \frac{1}{\pi\sqrt{A^2 - x^2}}, \qquad A = x_0\sqrt{2n + 1}
$$

where $A$ comes from matching the energy, $\frac{1}{2}m\omega^2A^2 = \left(n + \frac{1}{2}\right)\hbar\omega$. Hover (or focus and use the arrow keys) to read off the values:

{{ qho_classical_limit() }}

At $n = 0$ they look nothing alike: the quantum particle sits in the middle, the classical one at the edges, and the quantum one even leaks past the turning points (classically forbidden). At $n = 30$ the quantum density averages out to the classical curve. That's the **correspondence principle**: at large quantum numbers (macroscopic energies) we get classical probabilities back.

## Time dependence of the SHO

We know (these are the equations of motion for the operators, and they look exactly like the classical ones)

$$
\frac{d\hat p}{dt} = -m\omega^2\hat x, \qquad \frac{d\hat x}{dt} = \frac{\hat p}{m}
$$

With $a = \sqrt{\frac{m\omega}{2\hbar}}\left(\hat x + \frac{i\hat p}{m\omega}\right)$,

$$
\frac{da}{dt} = \sqrt{\frac{m\omega}{2\hbar}}\left(\frac{\hat p}{m} - i\omega\hat x\right) = -i\omega\sqrt{\frac{m\omega}{2\hbar}}\left(\hat x + \frac{i\hat p}{m\omega}\right)
$$

$$
\implies \boxed{\frac{da}{dt} = -i\omega a}, \qquad \boxed{\frac{da^\dagger}{dt} = i\omega a^\dagger}
$$

$$
\implies a(t) = a(0)\exp(-i\omega t), \qquad a^\dagger(t) = a^\dagger(0)\exp(i\omega t)
$$

$$
\begin{aligned}
\implies \hat x(t) + \frac{i\hat p(t)}{m\omega} &= \left(\hat x(0) + \frac{i\hat p(0)}{m\omega}\right)\exp(-i\omega t) \\\\
\hat x(t) - \frac{i\hat p(t)}{m\omega} &= \left(\hat x(0) - \frac{i\hat p(0)}{m\omega}\right)\exp(i\omega t)
\end{aligned}
$$

Adding and subtracting the two:

$$
\boxed{
\begin{aligned}
\hat x(t) &= \hat x(0)\cos\omega t + \frac{\hat p(0)}{m\omega}\sin\omega t \\\\
\hat p(t) &= -m\omega\hat x(0)\sin\omega t + \hat p(0)\cos\omega t
\end{aligned}
}
$$

Damn. $\therefore$ the $\hat x$ and $\hat p$ operators oscillate, exactly like the classical oscillator!

---

[← The simple harmonic oscillator](@/notes/quantum_18_harmonic_oscillator.md) | Next: [The hydrogen atom: angular part →](@/notes/quantum_20_hydrogen_atom_angular.md)
