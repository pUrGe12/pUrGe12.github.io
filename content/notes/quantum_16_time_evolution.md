+++
title = "Time evolution and the Schrödinger equation"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Time is a parameter

Time $\to$ just a parameter, **not** an operator / observable.

Eg. Einstein's photon box experiment: he tried to challenge $\Delta E\Delta t \geq \frac{\hbar}{2}$ by building a time operator. Pauli also showed that there cannot exist a self-adjoint (Hermitian) time operator $\hat T$ s.t. $[\hat H, \hat T] = i\hbar$.

So $\Delta t$ is not the uncertainty of a time operator. It's a proxy:

$$
\Delta t \equiv \frac{\Delta A}{\left|\frac{d\langle A\rangle}{dt}\right|}
$$

$\to$ by observing how physical dynamical operators change w.r.t. the parameter $t$ (the time it takes $\langle A\rangle$ to move by one $\Delta A$). This is the **Mandelstam-Tamm** version.

## How does a state ket change in time?

Say at $t = t_0$ it is $|\alpha\rangle$. At $t > t_0$ we don't expect the state to remain $|\alpha\rangle$, so we denote it as

$$
|\alpha, t_0; t\rangle
$$

(we write $\alpha, t_0$ to remind us that it used to be $\alpha$ at $t_0$). We know, by definition,

$$
\boxed{\lim_{t\to t_0}|\alpha, t_0; t\rangle = |\alpha\rangle}
$$

or, we'll use a short hand: $|\alpha, t_0; t_0\rangle = |\alpha, t_0\rangle$.

Now we need a **time evolution operator**, something to bring in the changes in time from $t_0$ to $t$. We'll call it $\mathcal U(t, t_0)$. The defining equation:

$$
\boxed{|\alpha, t_0; t\rangle = \mathcal U(t, t_0)|\alpha, t_0\rangle}
$$

## The time evolution operator is unitary

We know that

$$
|\alpha, t_0\rangle = \sum_{a\'}c_{a\'}(t_0)|a\'\rangle
$$

and at a later time

$$
|\alpha, t_0; t\rangle = \sum_{a\'}c_{a\'}(t)|a\'\rangle
$$

In general we expect

$$
|c_{a\'}(t)| \neq |c_{a\'}(t_0)|
$$

(but if $[\hat H, \hat A] = 0$, then they're equal! We'll see why in the [energy eigenkets notes](@/notes/quantum_17_energy_eigenkets.md).)

However, since $\sum_{a\'}|c_{a\'}(t_0)|^2$ talks of the total prob., the sum must stay equal (and 1):

$$
\implies \sum_{a\'}|c_{a\'}(t_0)|^2 = \sum_{a\'}|c_{a\'}(t)|^2
$$

Stated another way, if the state ket is normalized, then it's forever normalized:

$$
\langle\alpha, t_0|\alpha, t_0\rangle = 1 \implies \langle\alpha, t_0; t|\alpha, t_0; t\rangle = 1
$$

and from $|\alpha, t_0; t\rangle = \mathcal U|\alpha, t_0\rangle$ $\implies \langle\alpha, t_0; t| = \langle\alpha, t_0|\mathcal U^\dagger$

$$
\implies \boxed{\mathcal U^\dagger\mathcal U = 1}
$$

$\implies$ the time evolution operator is **unitary**.

> Note how probability conservation in time led to normalization, which led to the unitary condition.

## Composition

We need $\mathcal U$ to have another feature, **composition**:

$$
\mathcal U(t_2, t_0) = \mathcal U(t_2, t_1)\mathcal U(t_1, t_0), \qquad t_2 > t_1 > t_0
$$

And we also define the infinitesimal $\mathcal U(t_0 + dt, t_0)$:

$$
|\alpha, t_0; t_0 + dt\rangle = \mathcal U(t_0 + dt, t_0)|\alpha, t_0\rangle
$$

As $dt \to 0$, the small $\mathcal U(t_0 + dt, t_0)$ must go to the identity.

We assert (with no proof) that all of this is met by

$$
\boxed{\mathcal U(t_0 + dt, t_0) = 1 - i\Omega dt}
$$

where $\Omega$ is a Hermitian operator, $\Omega^\dagger = \Omega$. Why? We'll see. It satisfies the composition property

$$
\mathcal U(t_0 + dt_1 + dt_2, t_0) = \mathcal U(t_0 + dt_1 + dt_2, t_0 + dt_1)\mathcal U(t_0 + dt_1, t_0)
$$

since $(1 - i\Omega dt_2)(1 - i\Omega dt_1) = 1 - i\Omega(dt_1 + dt_2)$ to first order. And we can also check that $\mathcal U^\dagger\mathcal U = 1$ if we ignore the $(dt)^2$ terms:

$$
(1 + i\Omega dt)(1 - i\Omega dt) = 1 + \Omega^2dt^2 \approx 1
$$

So, it's not the perfect estimate... but it's right to first order, which is all we need.

## The Hamiltonian as the generator of time translations

The operator $\Omega$ has dimensions of $\text{time}^{-1}$. Any observable like that? Recall $E = \hbar\omega$ $\to$ an angular frequency.

Now, we know that the **Hamiltonian is the generator of time translations** (from classical mechanics), so we'll represent $\Omega$ with the Hamiltonian:

$$
\implies \hat\Omega = \frac{\hat H}{\hbar}
$$

$$
\implies \boxed{\mathcal U(t_0 + dt, t_0) = 1 - \frac{i\hat H dt}{\hbar}}
$$

$\hat H$ is assumed to be Hermitian. Compare it with the other two generators we've seen:

$$
\mathcal J(d\vec x\') = 1 - \frac{i\vec p\cdot d\vec x\'}{\hbar}, \qquad \mathcal D(\hat n, d\phi) = 1 - \frac{i\vec J\cdot\hat n}{\hbar}d\phi, \qquad \mathcal U(t_0 + dt, t_0) = 1 - \frac{i\hat H dt}{\hbar}
$$

$\to$ [momentum](@/notes/quantum_13_translations_and_momentum.md) generates translations, [angular momentum](@/notes/quantum_15_angular_momentum.md) generates rotations, and the Hamiltonian generates time translations.

## The Schrödinger equation

Using composition,

$$
\mathcal U(t + dt, t_0) = \mathcal U(t + dt, t)\mathcal U(t, t_0) = \left(1 - \frac{i\hat H dt}{\hbar}\right)\mathcal U(t, t_0)
$$

$$
\implies \mathcal U(t + dt, t_0) - \mathcal U(t, t_0) = -\frac{i\hat H dt}{\hbar}\mathcal U(t, t_0)
$$

and we can write

$$
\boxed{i\hbar\frac{\partial\mathcal U(t, t_0)}{\partial t} = \hat H\mathcal U(t, t_0)}
$$

$\to$ the **Schrödinger equation for the time evolution operator**.

Now we can obtain this for state kets too: multiply the equation with $|\alpha, t_0\rangle$ (from the right),

$$
i\hbar\frac{\partial\mathcal U}{\partial t}|\alpha, t_0\rangle = \hat H\mathcal U(t, t_0)|\alpha, t_0\rangle
$$

$|\alpha, t_0\rangle$ can go inside the derivative, as it's independent of $t$, and $\mathcal U|\alpha, t_0\rangle = |\alpha, t_0; t\rangle$

$$
\implies \boxed{i\hbar\frac{\partial}{\partial t}|\alpha, t_0; t\rangle = \hat H|\alpha, t_0; t\rangle}
$$

## Solving for the time evolution operator

We need to find solutions to

$$
i\hbar\frac{\partial\mathcal U}{\partial t} = \hat H\mathcal U
$$

3 cases:

**1. $\hat H$ is independent of time.** Then

$$
\boxed{\mathcal U(t, t_0) = \exp\left(-\frac{i\hat H(t - t_0)}{\hbar}\right)}
$$

for all $t, t_0$. Differentiate it and you get back $-\frac{i\hat H}{\hbar}\mathcal U$. It's also what you get by compounding $N$ infinitesimal steps, like we did for finite translations:

$$
\lim_{N\to\infty}\left(1 - \frac{i\hat H(t - t_0)}{N\hbar}\right)^N = \exp\left(-\frac{i\hat H(t - t_0)}{\hbar}\right)
$$

**2. $\hat H$ is time dependent, but $[\hat H(t_1), \hat H(t_2)] = 0$.** Then

$$
\boxed{\mathcal U(t, t_0) = \exp\left[-\frac{i}{\hbar}\int_{t_0}^{t}dt\'\hat H(t\')\right]}
$$

**3. The Hamiltonians at different times don't commute in general.** Some crazy thing called a **Dyson series**.

---

[← Angular momentum](@/notes/quantum_15_angular_momentum.md) | Next: [Energy eigenkets and spin precession →](@/notes/quantum_17_energy_eigenkets.md)
