+++
title = "The hydrogen atom: radial part and energy levels"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## The radial equation

Now let's focus on the radial part. From here on, $e^2$ means $\frac{e^2}{4\pi\varepsilon_0}$ (Gaussian units), to keep things short.

So, we now know (from the [angular part](@/notes/quantum_20_hydrogen_atom_angular.md)) $\beta = l(l + 1)$, and $V = -\frac{e^2}{r}$. Dividing equation (2) from there by $r^2$:

$$
\boxed{0 = \frac{1}{r^2}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \frac{2\mu}{\hbar^2}\left(E + \frac{e^2}{r}\right)R - \frac{l(l + 1)}{r^2}R}
$$

↳ the equation we had for the radial part.

Define

$$
u(r) = rR(r)
$$

$$
\implies \frac{dR}{dr} = \frac{d}{dr}\left(\frac{u}{r}\right) = \frac{u\'r - u}{r^2} \implies r^2\frac{dR}{dr} = u\'r - u
$$

$$
\implies \frac{d}{dr}\left(r^2\frac{dR}{dr}\right) = u\'\'r + u\' - u\' = u\'\'r
$$

Substituting this,

$$
0 = \frac{u\'\'}{r} + \frac{2\mu}{\hbar^2}\left(E + \frac{e^2}{r}\right)\frac{u}{r} - \frac{l(l + 1)u}{r^3}
$$

$$
\implies \boxed{\frac{d^2u}{dr^2} + \frac{2\mu}{\hbar^2}\left(E + \frac{e^2}{r} - \frac{\hbar^2l(l + 1)}{2\mu r^2}\right)u = 0}
$$

This is the 1D Schrödinger equation with $E - V_{\text{eff}}$, where

$$
\boxed{V_{\text{eff}} = -\frac{e^2}{r} + \frac{\hbar^2l(l + 1)}{2\mu r^2}}
$$

(the second term is the centrifugal barrier).

## Bound states and large r

We work with $E < 0$ to ensure bound states, $E = -|E|$:

$$
\implies u\'\' + \frac{2\mu}{\hbar^2}\left(-|E| + \frac{e^2}{r} - \frac{\hbar^2l(l + 1)}{2\mu r^2}\right)u = 0
$$

As $r \to \infty$, $\frac{1}{r}$ and $\frac{1}{r^2} \to 0$, and we have the constant $\frac{2\mu|E|}{\hbar^2}$ left.

$\therefore$ as $r \to \infty$, the equation reduces to

$$
\boxed{u\'\' = \frac{2\mu|E|}{\hbar^2}u}
$$

The general solution for this is $Ae^{-kr} + Be^{kr}$. We ignore the $e^{kr}$ solution because it diverges as $r \to \infty$. Here,

$$
k = \sqrt{\frac{2\mu|E|}{\hbar^2}}
$$

## A dimensionless variable

We now define

$$
y = 2kr
$$

$\to$ a dimensionless no. We'll differentiate $u$ against $y$ instead of $r$:

$$
\frac{du}{dr} = \frac{du}{dy}\frac{dy}{dr} = 2k\frac{du}{dy}, \qquad \frac{d^2u}{dr^2} = 4k^2\frac{d^2u}{dy^2}
$$

And now we rewrite the equation in terms of $u$ and $y$:

$$
\implies 4k^2u_{yy} + \frac{2\mu}{\hbar^2}\left(-|E| + \frac{e^2}{r} - \frac{\hbar^2l(l + 1)}{2\mu r^2}\right)u = 0
$$

Dividing by $4k^2 = \frac{8\mu|E|}{\hbar^2}$:

$$
\implies u_{yy} + \frac{1}{4}\left(-1 + \frac{e^2}{|E|r} - \frac{\hbar^2l(l + 1)}{2\mu|E|r^2}\right)u = 0
$$

and we can replace $r$ with $y$, as $r = \frac{y}{2k}$:

$$
\implies u_{yy} + \left(-\frac{1}{4} + \frac{e^2k}{2|E|y} - \frac{l(l + 1)}{y^2}\right)u = 0
$$

↳ all constants in the middle term. We'll call them $\lambda$:

$$
\lambda = \frac{e^2k}{2|E|} \implies \boxed{u_{yy} + \left(-\frac{1}{4} + \frac{\lambda}{y} - \frac{l(l + 1)}{y^2}\right)u = 0}
$$

$$
\lambda = \frac{e^2}{2|E|}\cdot\frac{\sqrt{2\mu|E|}}{\hbar} = \left(\frac{\mu e^4}{2\hbar^2|E|}\right)^{1/2} \qquad \therefore \boxed{\lambda \propto \frac{1}{\sqrt{|E|}}}
$$

$\to$ this is energy in disguise. $\therefore$ finding the allowed values of $\lambda$ gives the allowed values of energy.

## Near the origin

So, we did $R = \frac{u(r)}{r}$. Let's try out a particular solution for $u$ as $y^s$, and have $y \to 0$:

$$
u_{yy} = s(s - 1)y^{s-2}, \qquad \frac{\lambda}{y}u = \lambda y^{s-1}, \qquad \frac{l(l + 1)}{y^2}u = l(l + 1)y^{s-2}, \qquad \frac{1}{4}u = \frac{1}{4}y^s
$$

As $y \to 0$, $y^{s-2} \gg y^{s-1}$ or $y^s$. Since we have $u_{yy} - \frac{l(l + 1)}{y^2}u$ in the equation, they must cancel out as $y \to 0$ for $u = y^s$:

$$
\implies s(s - 1) = l(l + 1) \implies (s - l - 1)(s + l) = 0
$$

$\therefore s = l + 1$ or $s = -l$, i.e. $y^{l+1}$ or $y^{-l}$.

We'll discard $y^{-l}$: $u(0) = 0$ is a condition (so that $R = \frac{u}{r}$ stays finite), and that's impossible with $y^{-l}$.

So, near the origin,

$$
u(y) \approx y^{l+1}
$$

## The series solution

So, we know: as $y \to \infty$, $u \approx e^{-y/2}$ (that's the $e^{-kr}$), and as $y \to 0$, $u \approx y^{l+1}$.

So, the general function $u(y)$ can be written as

$$
\boxed{u(y) = e^{-y/2}y^{l+1}\sum_{k=0}^{\infty}a_ky^k = e^{-y/2}\sum_{k=0}^{\infty}a_ky^{k+l+1}}
$$

($a_0 \neq 0$ ensures $y^{l+1}$ is leading) ↳ some $\infty$ series. (This $k$ is just a summation index, not the $k$ from before.)

Let's differentiate, with $v = \sum_k a_ky^{k+l+1}$ so that $u = e^{-y/2}v$:

$$
u\'(y) = \left(e^{-y/2}\right)\'v + e^{-y/2}v\' = e^{-y/2}\left(v\' - \frac{1}{2}v\right)
$$

Differentiating again,

$$
u\'\' = e^{-y/2}\left(v\'\' - v\' + \frac{1}{4}v\right)
$$

Okay, now let's put these back into the differential equation we had for $u$:

$$
\implies e^{-y/2}\left(v\'\' - v\' + \frac{1}{4}v\right) + \left(-\frac{1}{4} + \frac{\lambda}{y} - \frac{l(l + 1)}{y^2}\right)e^{-y/2}v = 0
$$

$$
\implies \boxed{v\'\' - v\' + \left(\frac{\lambda}{y} - \frac{l(l + 1)}{y^2}\right)v = 0}
$$

Plugging in $v = \sum_k a_ky^{k+l+1}$:

$$
\begin{aligned}
v\' &= \sum_k a_k(k + l + 1)y^{k+l} \\\\
v\'\' &= \sum_k a_k(k + l + 1)(k + l)y^{k+l-1} \\\\
\frac{\lambda}{y}v &= \sum_k \lambda a_ky^{k+l} \\\\
\frac{l(l + 1)}{y^2}v &= \sum_k l(l + 1)a_ky^{k+l-1}
\end{aligned}
$$

$$
\implies \sum_{k\geq 0}a_k\underbrace{\left((k + l + 1)(k + l) - l(l + 1)\right)}\_{k(k + 2l + 1)}y^{k+l-1} + \sum_{k\geq 0}a_k\left(\lambda - (k + l + 1)\right)y^{k+l} = 0
$$

$\therefore$ the $k = 0$ term of the first sum is 0. Now we can shift it ($k \to k + 1$) and use the same summation, as the powers are the same:

$$
\sum_{k=0}^{\infty}\left[a_{k+1}(k + 1)(k + 2l + 2) + a_k(\lambda - k - l - 1)\right]y^{k+l} = 0
$$

This is true $\forall y$ iff each coefficient is 0

$$
\implies \boxed{a_{k+1} = \frac{k + l + 1 - \lambda}{(k + 1)(k + 2l + 2)}a_k}
$$

$\to$ the **recurrence relation**.

## The series must terminate

We know the series must terminate $\implies$ some $a_N \neq 0$ must have $a_{N+1} = 0$. (Why? Think 'bout it.)

If it didn't, then for large $k$, $\frac{a_{k+1}}{a_k} \to \frac{1}{k}$, which is exactly how the series for $e^y$ behaves. So $v \sim e^y$ and $u \sim e^{y/2}$, which blows up as $y \to \infty$: the $e^{kr}$ solution we threw away sneaks back in.

$a_{N+1} = 0$ iff

$$
\boxed{N + l + 1 - \lambda = 0}
$$

Let $n$ be an integer, $n = N + l + 1$ (so $l \leq n - 1$). The termination condition is

$$
\lambda = n
$$

## The energy levels

But $\lambda = \left(\frac{\mu e^4}{2\hbar^2|E|}\right)^{1/2}$

$$
\implies |E_n| = \frac{\mu e^4}{2\hbar^2n^2}
$$

and since $E_n = -|E_n|$,

$$
\implies \boxed{E_n = -\frac{\mu e^4}{2\hbar^2n^2}}
$$

$\to$ in SI units, it's

$$
\boxed{E_n = -\frac{\mu e^4}{2(4\pi\varepsilon_0)^2\hbar^2n^2} \approx -\frac{13.6\text{ eV}}{n^2}}
$$

$\therefore$ those are the energy levels of the H-atom! They only depend on $n$, so every $l \leq n - 1$ (and every $m$) at the same $n$ has the same energy.

## The radial wave functions

Now let's put $\lambda = n$ back into $\lambda = \frac{e^2k}{2|E|}$ and solve for $k$:

$$
k_n = \frac{2|E_n|n}{e^2} = \frac{2n}{e^2}\cdot\frac{\mu e^4}{2\hbar^2n^2} = \frac{\mu e^2}{\hbar^2n} = \frac{1}{na_B}
$$

where

$$
\boxed{a_B = \frac{\hbar^2}{\mu e^2}}
$$

$\to$ the Bohr radius. $\implies y = 2kr$ becomes

$$
\boxed{y = \frac{2r}{na_B}}
$$

and

$$
\boxed{R_{nl}(r) = \frac{u}{r} = \frac{1}{r}e^{-r/na_B}\sum_{k=0}^{N}a_k\left(\frac{2r}{na_B}\right)^{k+l+1}}, \qquad N = n - l - 1
$$

To fix $a_0$, we normalize with

$$
\int_0^{\infty}|R_{nl}|^2r^2dr = 1
$$

Eg. the ground state, $n = 1$, $l = 0$ $\implies N = 0$: $R_{10} = \frac{2a_0}{a_B}e^{-r/a_B}$, and normalizing gives

$$
R_{10}(r) = 2a_B^{-3/2}e^{-r/a_B}
$$

The full wave function is $\psi_{nlm}(r, \theta, \phi) = R_{nl}(r)Y_{lm}(\theta, \phi)$.

And with that... we're done for now.

---

[← The hydrogen atom: angular part](@/notes/quantum_20_hydrogen_atom_angular.md)
