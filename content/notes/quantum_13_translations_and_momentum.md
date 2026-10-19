+++
title = "Translations and momentum"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Continuous spectrum

In a discrete, finite world: $\hat A|a\'\rangle = a\'|a\'\rangle$. In a continuous one: $\hat\xi|\xi\'\rangle = \xi\'|\xi\'\rangle$. They mean the same shit.

Everything we had carries over, with sums becoming integrals and the Kronecker delta becoming the Dirac delta:

$$
\begin{aligned}
\langle a\'|a\'\'\rangle = \delta_{a\'a\'\'} &\quad\longrightarrow\quad \langle\xi\'|\xi\'\'\rangle = \delta(\xi\' - \xi\'\') \\\\
\sum_{a\'}|a\'\rangle\langle a\'| = 1 &\quad\longrightarrow\quad \int d\xi\'|\xi\'\rangle\langle\xi\'| = 1 \\\\
|\alpha\rangle = \sum_{a\'}|a\'\rangle\langle a\'|\alpha\rangle &\quad\longrightarrow\quad |\alpha\rangle = \int d\xi\'|\xi\'\rangle\langle\xi\'|\alpha\rangle \\\\
\sum_{a\'}|\langle a\'|\alpha\rangle|^2 = 1 &\quad\longrightarrow\quad \int d\xi\'|\langle\xi\'|\alpha\rangle|^2 = 1 \\\\
\langle\beta|\alpha\rangle = \sum_{a\'}\langle\beta|a\'\rangle\langle a\'|\alpha\rangle &\quad\longrightarrow\quad \langle\beta|\alpha\rangle = \int d\xi\'\langle\beta|\xi\'\rangle\langle\xi\'|\alpha\rangle \\\\
\langle a\'\'|\hat A|a\'\rangle = a\'\delta_{a\'a\'\'} &\quad\longrightarrow\quad \langle\xi\'\'|\hat\xi|\xi\'\rangle = \xi\'\delta(\xi\'\' - \xi\')
\end{aligned}
$$

(the last one assuming eigenkets).

## Position eigenkets

$$
\hat x|x\'\rangle = x\'|x\'\rangle
$$

The eigenkets $|x\'\rangle$ of $\hat x$ form a complete set. The state ket of any state $|\alpha\rangle$ can be written as

$$
|\alpha\rangle = \int_{-\infty}^{\infty}dx\'|x\'\rangle\langle x\'|\alpha\rangle
$$

$\implies$ when we detect the position ($x\'$), $|\alpha\rangle$ jumps into the $|x\'\rangle$ state. Same way as an SG$\hat x$ measurement makes $|+\rangle \to |S_x;+\rangle$, for example.

In practice of course, we can't detect "exactly" at $x\'$, so we do it around a small band, $x\' - \frac{\Delta}{2}$ to $x\' + \frac{\Delta}{2}$:

$$
\underbrace{|\alpha\rangle = \int_{-\infty}^{\infty}dx\'\'|x\'\'\rangle\langle x\'\'|\alpha\rangle}\_{\text{before measurement: can be anywhere}} \xrightarrow{\text{measure}} \int_{x\' - \Delta/2}^{x\' + \Delta/2}dx\'\'|x\'\'\rangle\langle x\'\'|\alpha\rangle
$$

with $\Delta \to dx\'$. The prob. for this detector to click is

$$
|\langle x\'|\alpha\rangle|^2dx\'
$$

The prob. of the particle being "somewhere" is $\int dx\'|\langle x\'|\alpha\rangle|^2$, and if $|\alpha\rangle$ is normalized, this is 1. Duh.

$$
\int_{-\infty}^{\infty}dx\'|\langle x\'|\alpha\rangle|^2 = 1
$$

We of course know that $\langle x\'|\alpha\rangle$ is the wave function (more on that in the [next notes](@/notes/quantum_14_wave_functions.md)).

### In 3 dimensions

$$
|\alpha\rangle = \int d^3x\'|\vec x\'\rangle\langle\vec x\'|\alpha\rangle
$$

where $|\vec x\'\rangle = |x\', y\', z\'\rangle$ is a simultaneous eigenket:

$$
\hat x|\vec x\'\rangle = x\'|\vec x\'\rangle, \qquad \hat y|\vec x\'\rangle = y\'|\vec x\'\rangle, \qquad \hat z|\vec x\'\rangle = z\'|\vec x\'\rangle
$$

We know from the [simultaneous eigenket](@/notes/quantum_09_compatible_observables.md) definition

$$
\implies [x_i, x_j] = 0
$$

## Translations

Take a state $|\alpha\rangle$ from $\vec x\'$ to $\vec x\' + d\vec x\'$, leaving everything else unchanged $\to$ an **infinitesimal translation**. We have an operator for this:

$$
\mathcal J(d\vec x\')|\vec x\'\rangle = |\vec x\' + d\vec x\'\rangle
$$

(not an eigenvalue equation). Now, we can expand $|\alpha\rangle$ in position eigenkets:

$$
\begin{aligned}
\mathcal J(d\vec x\')|\alpha\rangle &= \mathcal J(d\vec x\')\int d^3x\'|\vec x\'\rangle\langle\vec x\'|\alpha\rangle \\\\
&= \int d^3x\'|\vec x\' + d\vec x\'\rangle\langle\vec x\'|\alpha\rangle \\\\
&= \int d^3x\'|\vec x\'\rangle\langle\vec x\' - d\vec x\'|\alpha\rangle
\end{aligned}
$$

(the last line by a change of variables).

What properties should $\mathcal J$ have?

1. It's reasonable to assume that if $|\alpha\rangle$ is normalized, then a shifted $|\alpha\rangle$ must also be. $\langle\alpha|\alpha\rangle = \langle\alpha|\mathcal J^\dagger\mathcal J|\alpha\rangle$, so $\mathcal J^\dagger\mathcal J = 1$ $\to$ **unitary**, from the prob. $= 1$ thing.
2. Two translations add like vectors: $\mathcal J(d\vec x\'\')\mathcal J(d\vec x\') = \mathcal J(d\vec x\' + d\vec x\'\')$
3. $\mathcal J(-d\vec x\') = \mathcal J^{-1}(d\vec x\')$
4. $\lim_{d\vec x\' \to 0}\mathcal J(d\vec x\') = 1$ $\to$ no translation $\implies$ unchanged state.

These come from simply reasoning about $d\vec x$ as a vector.

$$
\implies \boxed{\mathcal J(d\vec x\') = 1 - i\vec K\cdot d\vec x\'}
$$

$\to$ this fits, where $\vec K$ has $K_x, K_y, K_z$, and all 3 are Hermitian. Then all the properties are satisfied to first order. Eg. $\mathcal J^\dagger\mathcal J = (1 + i\vec K\cdot d\vec x\')(1 - i\vec K\cdot d\vec x\') = 1 + O(d\vec x\'^2)$.

### Position and translations don't commute

Note that,

$$
\begin{aligned}
\hat{\vec x}\mathcal J(d\vec x\')|\vec x\'\rangle &= \hat{\vec x}|\vec x\' + d\vec x\'\rangle = (\vec x\' + d\vec x\')|\vec x\' + d\vec x\'\rangle \\\\
\mathcal J(d\vec x\')\hat{\vec x}|\vec x\'\rangle &= \vec x\'\mathcal J(d\vec x\')|\vec x\'\rangle = \vec x\'|\vec x\' + d\vec x\'\rangle
\end{aligned}
$$

Hence,

$$
\boxed{[\hat{\vec x}, \mathcal J(d\vec x\')]|\vec x\'\rangle = d\vec x\'|\vec x\' + d\vec x\'\rangle \approx d\vec x\'|\vec x\'\rangle}
$$

(to first order). Now $|\vec x\'\rangle$ can be any position eigenket, and they form a complete set.

$\therefore$ we must have

$$
[\hat{\vec x}, \mathcal J(d\vec x\')] = d\vec x\'
$$

$\to$ just that with the ket removed, since it holds always.

This basically says that "measure and move" vs "move and measure" are off by a factor that's always how much you moved, which makes sense.

Substituting $\mathcal J = 1 - i\vec K\cdot d\vec x\'$, the $i$-th component is

$$
-i\hat x_i(\vec K\cdot d\vec x\') + i(\vec K\cdot d\vec x\')\hat x_i = dx_i\' \implies -i\sum_j[\hat x_i, K_j]dx_j\' = dx_i\'
$$

$$
\implies \boxed{[x_i, K_j] = i\delta_{ij}}
$$

$\to$ an imaginary no.

## Momentum as a generator of translations

We have $[x_i, K_j] = i\delta_{ij}$ $\to$ the commutation relation b/w the position operators $x, y, z$ and the $K$ operators $K_x, K_y, K_z$.

What's the physical meaning of $\vec K$?

> $\to$ it is related to the momentum operator in QM.

$\hat K \neq \hat p$, because the dimensions are all wrong ($\vec K\cdot d\vec x$ has to be dimensionless, so $K \sim 1/\text{length}$). We set

$$
\hat K = \frac{\hat p}{\text{constant}}
$$

$\to$ just to set the dimensions right, but we have no way of knowing the exact value. We let it be $\hbar$, because it fixes the dimensionality problem. Recall that

$$
\frac{p}{\hbar} = \frac{2\pi}{\lambda}
$$

from the de Broglie wavelength relation.

> $\implies \hat K$ corresponds to the wave no.

$$
\implies \boxed{\mathcal J(d\vec x\') = 1 - \frac{i\vec p\cdot d\vec x\'}{\hbar}}
$$

where $\vec p$ is the momentum operator. And from $[x_i, K_j] = i\delta_{ij}$ we get

$$
\boxed{[x_i, p_j] = i\hbar\delta_{ij}}
$$

$\implies x$ and $p_x$ are incompatible observables with no simultaneous eigenkets, since $[x, p_x] = i\hbar \neq 0$ $\implies$ they cannot be measured simultaneously. We can even obtain the relation (from the [general uncertainty relation](@/notes/quantum_11_incompatible_observables.md#the-general-uncertainty-relation), $\frac{1}{4}|i\hbar|^2$):

$$
\langle(\Delta x)^2\rangle\langle(\Delta p_x)^2\rangle \geq \frac{\hbar^2}{4}
$$

## Finite translations

Note that $\mathcal J(d\vec x\')$ is an operator for infinitesimal translations. Now we want to concern ourselves with **finite translations** $\implies$ compounding $N$ infinitesimal ones.

A finite translation in $\hat x$ by $\Delta x\'$:

$$
\mathcal J(\Delta x\'\hat x)|\vec x\'\rangle = |\vec x\' + \Delta x\'\hat x\rangle
$$

($\hat x$ just to specify the direction).

$$
\implies \mathcal J(\Delta x\'\hat x) = \lim_{N\to\infty}\left(1 - \frac{ip_x\Delta x\'}{N\hbar}\right)^N
$$

$$
\boxed{\mathcal J(\Delta x\'\hat x) = \exp\left(-\frac{ip_x\Delta x\'}{\hbar}\right)}
$$

$\to$ the operator of finite translations.

### Translations commute

Finite translations along $\hat x$ and $\hat y$ commute, that is, going to a point D can be done via A $\to$ B $\to$ D or A $\to$ C $\to$ D.

```text
        C ─────────────► D
        ▲                ▲
        │ Δy             │ Δy
        │                │
        A ─────────────► B
               Δx
```

$$
\begin{aligned}
\mathcal J(\Delta y\'\hat y)\mathcal J(\Delta x\'\hat x) &= \mathcal J(\Delta x\'\hat x + \Delta y\'\hat y) \\\\
\mathcal J(\Delta x\'\hat x)\mathcal J(\Delta y\'\hat y) &= \mathcal J(\Delta x\'\hat x + \Delta y\'\hat y)
\end{aligned}
$$

$$
\implies [\mathcal J(\Delta x\'\hat x), \mathcal J(\Delta y\'\hat y)] = 0
$$

Recall that $\exp(x) = 1 + x + \frac{x^2}{2!} + \dots$

$$
\begin{aligned}
\exp\left(-\frac{ip_x\Delta x\'}{\hbar}\right) &= 1 - \frac{ip_x\Delta x\'}{\hbar} - \frac{p_x^2\Delta x\'^2}{2\hbar^2} + \dots \approx \mathcal J(\Delta x\'\hat x) \\\\
\exp\left(-\frac{ip_y\Delta y\'}{\hbar}\right) &= 1 - \frac{ip_y\Delta y\'}{\hbar} - \frac{p_y^2\Delta y\'^2}{2\hbar^2} + \dots \approx \mathcal J(\Delta y\'\hat y)
\end{aligned}
$$

Plug these into the commutator. The $1$s commute with everything, and the squared terms only show up at higher orders, so to 2nd order

$$
\left[1 - \frac{ip_x\Delta x\'}{\hbar} - \frac{p_x^2\Delta x\'^2}{2\hbar^2},\ 1 - \frac{ip_y\Delta y\'}{\hbar} - \frac{p_y^2\Delta y\'^2}{2\hbar^2}\right] \approx -\frac{\Delta x\'\Delta y\'}{\hbar^2}[p_x, p_y]
$$

Since we know that the commutator is 0,

$$
\implies [p_x, p_y] = 0
$$

and more generally,

$$
\boxed{[p_i, p_j] = 0}
$$

This relation is due to the fact that translations in diff. directions commute. (Note how [rotations](@/notes/quantum_15_angular_momentum.md) won't commute!)

So, $[p_i, p_j] = 0$ $\implies$ we have a simultaneous eigenket

$$
|p_x\', p_y\', p_z\'\rangle \equiv |\vec p\'\rangle, \qquad p_x|\vec p\'\rangle = p_x\'|\vec p\'\rangle, \dots
$$

for momentum. And clearly the infinitesimal translation operator also gives an eigenvalue equation here:

$$
\mathcal J(d\vec x\')|\vec p\'\rangle = \left(1 - \frac{i\vec p\cdot d\vec x\'}{\hbar}\right)|\vec p\'\rangle = \left(1 - \frac{i\vec p\'\cdot d\vec x\'}{\hbar}\right)|\vec p\'\rangle
$$

So even though $|\vec x\'\rangle$ is not an eigenket of $\mathcal J(d\vec x\')$ (as $\mathcal J(d\vec x\')|\vec x\'\rangle = |\vec x\' + d\vec x\'\rangle$), $|\vec p\'\rangle$ **is** an eigenket of $\mathcal J(d\vec x\')$.

$$
[\vec p, \mathcal J(d\vec x\')] = 0
$$

## The fundamental commutation relations

So, we have the following commutation relations:

$$
\boxed{[x_i, x_j] = 0, \qquad [p_i, p_j] = 0, \qquad [x_i, p_j] = i\hbar\delta_{ij}}
$$

These are the **"fundamental commutation relations"**.

---

[← Change of basis and the transformation matrix](@/notes/quantum_12_change_of_basis.md) | Next: [Wave functions in position and momentum space →](@/notes/quantum_14_wave_functions.md)
