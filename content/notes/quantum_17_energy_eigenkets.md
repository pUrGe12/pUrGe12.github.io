+++
title = "Energy eigenkets and spin precession"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Energy eigenkets

Okay, say we have an operator $\hat A$ s.t. $[\hat A, \hat H] = 0$, and $|a\'\rangle$ is the base ket of $\hat A$ and its eigenket too. Then, the eigenkets of $\hat A$ are also eigenkets of $\hat H$ ([simultaneous](@/notes/quantum_09_compatible_observables.md)), and these eigenkets are called **"energy eigenkets"**:

$$
\hat H|a\'\rangle = E_{a\'}|a\'\rangle
$$

Recall that we can [write any operator](@/notes/quantum_06_matrix_representations.md) as

$$
\hat B = \sum_{a\'\'}\sum_{a\'}|a\'\'\rangle\langle a\'\'|\hat B|a\'\rangle\langle a\'|
$$

We do this for $\exp\left(-\frac{i\hat Ht}{\hbar}\right)$ (taking $t_0 = 0$):

$$
\exp\left(-\frac{i\hat Ht}{\hbar}\right) = \sum_{a\'\'}\sum_{a\'}|a\'\'\rangle\langle a\'\'|\exp\left(-\frac{i\hat Ht}{\hbar}\right)|a\'\rangle\langle a\'|
$$

Now, how is

$$
\exp\left(-\frac{i\hat Ht}{\hbar}\right)|a\'\rangle = \exp\left(-\frac{iE_{a\'}t}{\hbar}\right)|a\'\rangle
$$

??

This is cause we know $\hat H|a\'\rangle = E_{a\'}|a\'\rangle$. Any Taylor-expandable function of $\hat H$ acting on $|a\'\rangle$ just replaces $\hat H$ with $E_{a\'}$:

$$
\exp\left(-\frac{i\hat Ht}{\hbar}\right)|a\'\rangle = \sum_n\frac{1}{n!}\left(-\frac{it}{\hbar}\right)^n\hat H^n|a\'\rangle = \sum_n\frac{1}{n!}\left(-\frac{it}{\hbar}\right)^nE_{a\'}^n|a\'\rangle
$$

So the sandwiched part is $\exp\left(-\frac{iE_{a\'}t}{\hbar}\right)\delta_{a\'\'a\'}$, and the double sum collapses:

$$
\boxed{\exp\left(-\frac{i\hat Ht}{\hbar}\right) = \sum_{a\'}|a\'\rangle\exp\left(-\frac{iE_{a\'}t}{\hbar}\right)\langle a\'|}
$$

## How the expansion coefficients evolve

This is useful. For example, suppose

$$
|\alpha, t_0 = 0\rangle = \sum_{a\'}|a\'\rangle\langle a\'|\alpha\rangle = \sum_{a\'}c_{a\'}|a\'\rangle
$$

then

$$
\begin{aligned}
|\alpha, t_0 = 0; t\rangle &= \exp\left(-\frac{i\hat Ht}{\hbar}\right)|\alpha, t_0 = 0\rangle \\\\
&= \sum_{a\'}|a\'\rangle\langle a\'|\alpha\rangle\exp\left(-\frac{iE_{a\'}t}{\hbar}\right)
\end{aligned}
$$

$\implies c_{a\'}(t = 0) \to c_{a\'}(t)$, the expansion coefficients change as

$$
\boxed{c_{a\'}(t) = c_{a\'}(t = 0)\exp\left(-\frac{iE_{a\'}t}{\hbar}\right)}
$$

Only the phase changes, so $|c_{a\'}(t)| = |c_{a\'}(0)|$. That's the "if $[\hat H, \hat A] = 0$ then they're equal" from the [time evolution notes](@/notes/quantum_16_time_evolution.md#the-time-evolution-operator-is-unitary).

A special case, when $|\alpha\rangle = |a\'\rangle$:

$$
\boxed{|a\', t_0 = 0; t\rangle = |a\', t = 0\rangle\exp\left(-\frac{iE_{a\'}t}{\hbar}\right)}
$$

> If a state is a simultaneous eigenket of $\hat A$ and $\hat H$, it remains so, at all times.

because $\exp\left(-\frac{iE_{a\'}t}{\hbar}\right)$ is only doing phase modulation.

## Example: spin ½ in a magnetic field

The Hamiltonian of a spin $\frac{1}{2}$ system, with magnetic moment $\mu = \frac{e\hbar}{2mc}$, in an external field $\vec B$:

$$
\boxed{\hat H = -\left(\frac{e}{mc}\right)\vec S\cdot\vec B}
$$

($e < 0$ for the electron). We let $\vec B$ be static and uniform in $\hat z$. Evaluating the dot:

$$
\boxed{\hat H = -\frac{eB}{mc}\hat S_z}
$$

Clearly $[\hat H, \hat S_z] = 0$, since there's just a constant multiplier. So they have simultaneous energy eigenkets ($|\pm\rangle$), with energy eigenvalues

$$
\boxed{E_\pm = \mp\frac{e\hbar B}{2mc}}
$$

as $\hat S_z|\pm\rangle = \pm\frac{\hbar}{2}|\pm\rangle$. We define $\omega$ as

$$
\boxed{\omega = \frac{|e|B}{mc}}
$$

and then $\hat H = \omega\hat S_z$, so $\hat H|\pm\rangle = \pm\frac{\hbar\omega}{2}|\pm\rangle$.

### Time development

Now if we consider the time development, it's captured in

$$
\mathcal U(t, 0) = \exp\left(-\frac{i\omega\hat S_zt}{\hbar}\right)
$$

Suppose at $t = 0$, the system is

$$
|\alpha\rangle = c_+|+\rangle + c_-|-\rangle
$$

Apply the time evolution to it:

$$
\begin{aligned}
|\alpha, t_0 = 0; t\rangle &= \exp\left(-\frac{i\omega\hat S_zt}{\hbar}\right)\left(c_+|+\rangle + c_-|-\rangle\right) \\\\
&= c_+\exp\left(-\frac{i\omega t}{2}\right)|+\rangle + c_-\exp\left(\frac{i\omega t}{2}\right)|-\rangle
\end{aligned}
$$

If $|\alpha\rangle$ at $t = 0$ was $|+\rangle$ ($c_+ = 1$, $c_- = 0$), then we see that

$$
\boxed{|\alpha, 0; t\rangle = \exp\left(-\frac{i\omega t}{2}\right)|+\rangle}
$$

$\to$ it forever stays spin up.

If $|\alpha\rangle$ was in the $S_x+$ state,

$$
|\alpha, 0\rangle = \frac{1}{\sqrt 2}|+\rangle + \frac{1}{\sqrt 2}|-\rangle
$$

then we can work out the probabilities...

$$
\begin{aligned}
|\langle S_x;\pm|\alpha, t_0 = 0; t\rangle|^2 &= \left|\underbrace{\left[\frac{1}{\sqrt 2}\langle+| \pm \frac{1}{\sqrt 2}\langle-|\right]}\_{\langle S_x;\pm|}\cdot\underbrace{\left[\frac{1}{\sqrt 2}e^{-i\omega t/2}|+\rangle + \frac{1}{\sqrt 2}e^{i\omega t/2}|-\rangle\right]}\_{|\alpha, t_0 = 0; t\rangle}\right|^2 \\\\
&= \left|\frac{1}{2}e^{-i\omega t/2} \pm \frac{1}{2}e^{i\omega t/2}\right|^2
\end{aligned}
$$

$$
\boxed{
|\langle S_x;+|\alpha, t_0 = 0; t\rangle|^2 = \cos^2\frac{\omega t}{2}, \qquad |\langle S_x;-|\alpha, t_0 = 0; t\rangle|^2 = \sin^2\frac{\omega t}{2}
}
$$

(as $\frac{1}{2}(e^{-i\theta} + e^{i\theta}) = \cos\theta$ and $\frac{1}{2}(e^{-i\theta} - e^{i\theta}) = -i\sin\theta$).

$\to$ This means the spin can flip directions after some time!!

### Spin precession

And we can write $\langle\hat S_x\rangle$ using

$$
\langle A\rangle = \sum_{a\'}a\'|\langle a\'|\alpha\rangle|^2
$$

(measured value $\times$ the prob. of finding it):

$$
\langle\hat S_x\rangle = \frac{\hbar}{2}\cos^2\frac{\omega t}{2} + \left(-\frac{\hbar}{2}\right)\sin^2\frac{\omega t}{2}
$$

$$
\boxed{\langle\hat S_x\rangle = \frac{\hbar}{2}\cos\omega t}
$$

and

$$
\boxed{\langle\hat S_y\rangle = \frac{\hbar}{2}\sin\omega t, \qquad \langle\hat S_z\rangle = 0}
$$

↳ we expect $\hat S_z$ to not change at all (it commutes with $\hat H$). It'll be $\pm\frac{\hbar}{2}$, with the same probabilities, always.

So the spin's expectation value rotates in the $xy$-plane with angular frequency $\omega$: **spin precession**.

---

[← Time evolution and the Schrödinger equation](@/notes/quantum_16_time_evolution.md) | Next: [The simple harmonic oscillator →](@/notes/quantum_18_harmonic_oscillator.md)
