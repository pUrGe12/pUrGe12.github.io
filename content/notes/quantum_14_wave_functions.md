+++
title = "Wave functions in position and momentum space"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Wave functions in position space

Let's talk about the 1D case only:

$$
\hat x|x\'\rangle = x\'|x\'\rangle, \qquad \langle x\'\'|x\'\rangle = \delta(x\' - x\'\')
$$

(normalized). We're talking continuous spaces here:

$$
|\alpha\rangle = \int dx\'|x\'\rangle\langle x\'|\alpha\rangle
$$

and $|\langle x\'|\alpha\rangle|^2dx\'$ $\to$ the prob. of the particle being found in the interval $x\'$ to $x\' + dx\'$.

We recall that $\langle x\'|\alpha\rangle$ is the **wave function** of the state $|\alpha\rangle$:

$$
\boxed{\langle x\'|\alpha\rangle = \psi_\alpha(x\')}
$$

and we know the prob. is $|\psi_\alpha(x\')|^2dx\'$, which is what we have above too.

### Inner products

Consider the inner product $\langle\beta|\alpha\rangle$. From $|\alpha\rangle = \int dx\'|x\'\rangle\langle x\'|\alpha\rangle$,

$$
\langle\beta|\alpha\rangle = \int dx\'\langle\beta|x\'\rangle\langle x\'|\alpha\rangle
$$

$$
\boxed{\langle\beta|\alpha\rangle = \int dx\'\psi_\beta^{\ast}(x\')\psi_\alpha(x\')}
$$

$\to$ represents the prob. amplitude of the state $|\alpha\rangle$ to be found in $|\beta\rangle$.

### Operators

Consider also the application of an operator $f(\hat x)$:

$$
f(\hat x)|\alpha\rangle = \int dx\'f(\hat x)|x\'\rangle\langle x\'|\alpha\rangle = \int dx\'f(x\')|x\'\rangle\langle x\'|\alpha\rangle
$$

and

$$
\langle\beta|f(\hat x)|\alpha\rangle = \int dx\'\langle\beta|x\'\rangle f(x\')\langle x\'|\alpha\rangle
$$

$$
\boxed{\langle\beta|f(\hat x)|\alpha\rangle = \int dx\'\psi_\beta^{\ast}(x\')f(x\')\psi_\alpha(x\')}
$$

↳ only true if $f$ is a function of the observable $\hat x$. Why?

In general,

$$
\langle\beta|\hat A|\alpha\rangle = \int dx\'\langle\beta|\hat A|x\'\rangle\langle x\'|\alpha\rangle
$$

We can introduce the identity by the completeness of the $|x\'\'\rangle$:

$$
1 = \int dx\'\'|x\'\'\rangle\langle x\'\'|
$$

$$
\begin{aligned}
\langle\beta|\hat A|\alpha\rangle &= \int dx\'\int dx\'\'\langle\beta|x\'\'\rangle\langle x\'\'|\hat A|x\'\rangle\langle x\'|\alpha\rangle \\\\
&= \int dx\'\int dx\'\'\psi_\beta^{\ast}(x\'\')\langle x\'\'|\hat A|x\'\rangle\psi_\alpha(x\')
\end{aligned}
$$

If $\hat A = f(\hat x)$, say $\hat x^2$, then

$$
\hat x^2|x\'\rangle = x\'^2|x\'\rangle \implies \langle x\'\'|\hat x^2|x\'\rangle = x\'^2\delta(x\' - x\'\')
$$

(since $\langle x\'\'|x\'\rangle = \delta(x\' - x\'\')$). The delta kills one of the integrals:

$$
\langle\beta|\hat x^2|\alpha\rangle = \int dx\'\langle\beta|x\'\rangle x\'^2\langle x\'|\alpha\rangle = \int dx\'\psi_\beta^{\ast}(x\')x\'^2\psi_\alpha(x\')
$$

and in general, if $\hat A = f(\hat x)$,

$$
\boxed{\langle\beta|f(\hat x)|\alpha\rangle = \int dx\'\psi_\beta^{\ast}(x\')f(x\')\psi_\alpha(x\')}
$$

$f(\hat x)$ on the left is an operator, the $f(x\')$ inside is **not** an operator (just a function). That's the why: for a function of $\hat x$, the matrix $\langle x\'\'|\hat A|x\'\rangle$ is diagonal. For a general $\hat A$ (like $\hat p$) it isn't.

## Momentum in the position basis

Let's apply an infinitesimal [translation](@/notes/quantum_13_translations_and_momentum.md) $\mathcal J(\Delta x)$ to an arbitrary state $|\alpha\rangle$:

$$
\begin{aligned}
\left(1 - \frac{ip_x\Delta x}{\hbar}\right)|\alpha\rangle &= \int dx\'\mathcal J(\Delta x)|x\'\rangle\langle x\'|\alpha\rangle \\\\
&= \int dx\'|x\' + \Delta x\rangle\langle x\'|\alpha\rangle
\end{aligned}
$$

Introduce a dummy $y = x\' + \Delta x$, so $dy = dx\'$ and $x\' = y - \Delta x$:

$$
\begin{aligned}
\int dy|y\rangle\langle y - \Delta x|\alpha\rangle &= \int dx\'|x\'\rangle\langle x\' - \Delta x|\alpha\rangle \\\\
&= \int dx\'|x\'\rangle\left(\langle x\'|\alpha\rangle - \Delta x\frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle\right)
\end{aligned}
$$

through a first order Taylor expansion:

$$
\langle x\' - \Delta x|\alpha\rangle = \langle x\'|\alpha\rangle - \frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle\cdot\Delta x
$$

And on the other side,

$$
\left(1 - \frac{ip_x\Delta x}{\hbar}\right)|\alpha\rangle = \int dx\'|x\'\rangle\langle x\'|\alpha\rangle - \frac{i\Delta x}{\hbar}p_x|\alpha\rangle
$$

Comparing these two, we get

$$
\boxed{p_x|\alpha\rangle = \int dx\'|x\'\rangle\left(-i\hbar\frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle\right)}
$$

i.e. $p_x = -i\hbar\frac{\partial}{\partial x}$ in the position basis. To see it as a wave function, hit it with $\langle x\'\'|$:

$$
\langle x\'\'|\hat p|\alpha\rangle = \int dx\'\underbrace{\langle x\'\'|x\'\rangle}\_{\delta(x\'\' - x\')}\left(-i\hbar\frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle\right)
$$

$$
\boxed{\langle x\'|\hat p|\alpha\rangle = -i\hbar\frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle}
$$

$\to$ momentum in the position basis.

## Momentum space wave function

In the $p$ basis, we can span the entire space too:

$$
1 = \int dp\'|p\'\rangle\langle p\'|, \qquad |\alpha\rangle = \int dp\'|p\'\rangle\langle p\'|\alpha\rangle
$$

$$
\hat p|p\'\rangle = p\'|p\'\rangle, \qquad \langle p\'|p\'\'\rangle = \delta(p\' - p\'\')
$$

(orthonormal).

$$
\boxed{\langle p\'|\alpha\rangle = \phi_\alpha(p\')}
$$

$\to$ called the **momentum space wave function**. If $|\alpha\rangle$ is normalized, $\langle\alpha|\alpha\rangle = 1$

$$
\implies \langle\alpha|\alpha\rangle = \int dp\'\langle\alpha|p\'\rangle\langle p\'|\alpha\rangle = 1
$$

$$
\implies \int dp\'|\langle p\'|\alpha\rangle|^2 = 1 \implies \int dp\'|\phi_\alpha(p\')|^2 = 1
$$

The interpretation of $\langle p\'|\alpha\rangle$: the prob. that a measurement of $p$ gives an eigenvalue $p\'$ within a narrow interval $dp\'$ is $|\langle p\'|\alpha\rangle|^2dp\'$.

## The momentum eigenfunction

Recall that

$$
\langle x\'|\hat p|\alpha\rangle = -i\hbar\frac{\partial}{\partial x\'}\langle x\'|\alpha\rangle
$$

Let $|\alpha\rangle = |p\'\rangle$:

$$
\langle x\'|\hat p|p\'\rangle = -i\hbar\frac{\partial}{\partial x\'}\langle x\'|p\'\rangle
$$

but $\hat p|p\'\rangle = p\'|p\'\rangle$

$$
\implies \boxed{p\'\langle x\'|p\'\rangle = -i\hbar\frac{\partial}{\partial x\'}\langle x\'|p\'\rangle}
$$

$$
\implies \boxed{\langle x\'|p\'\rangle = N\exp\left(\frac{ip\'x\'}{\hbar}\right)}
$$

$\to$ note that this is a function of 2 variables. It can be regarded as the wave function for the momentum eigenstate $|p\'\rangle$ $\implies$ the **momentum eigenfunction**.

To find $N$, note:

$$
|x\'\'\rangle = \int dp\'|p\'\rangle\langle p\'|x\'\'\rangle \implies \langle x\'|x\'\'\rangle = \int dp\'\langle x\'|p\'\rangle\langle p\'|x\'\'\rangle
$$

and since $\langle x\'|x\'\'\rangle = \delta(x\' - x\'\')$ (normalized),

$$
\boxed{\int dp\'\langle x\'|p\'\rangle\langle p\'|x\'\'\rangle = \delta(x\' - x\'\')}
$$

With $\langle x\'|p\'\rangle = N\exp\left(\frac{ip\'x\'}{\hbar}\right)$ and $\langle p\'|x\'\'\rangle = N^{\ast}\exp\left(-\frac{ip\'x\'\'}{\hbar}\right)$,

$$
\begin{aligned}
\delta(x\' - x\'\') &= |N|^2\int dp\'\exp\left(\frac{ip\'(x\' - x\'\')}{\hbar}\right) \\\\
&= 2\pi\hbar|N|^2\delta(x\' - x\'\')
\end{aligned}
$$

(using $\int dk\ e^{ik(x\' - x\'\')} = 2\pi\delta(x\' - x\'\')$ with $k = p\'/\hbar$).

$$
\implies \boxed{N = \frac{1}{\sqrt{2\pi\hbar}}}
$$

$\to$ this is the normalization constant (choosing it real and positive).

$$
\implies \boxed{\langle x\'|p\'\rangle = \frac{1}{\sqrt{2\pi\hbar}}\exp\left(\frac{ip\'x\'}{\hbar}\right)}
$$

## Switching between the two

We know $|\alpha\rangle = \int dp\'|p\'\rangle\langle p\'|\alpha\rangle$, so

$$
\langle x\'|\alpha\rangle = \int dp\'\langle x\'|p\'\rangle\langle p\'|\alpha\rangle, \qquad \langle p\'|\alpha\rangle = \int dx\'\langle p\'|x\'\rangle\langle x\'|\alpha\rangle
$$

$$
\boxed{
\begin{aligned}
\psi_\alpha(x\') &= \frac{1}{\sqrt{2\pi\hbar}}\int dp\'\exp\left(\frac{ip\'x\'}{\hbar}\right)\phi_\alpha(p\') \\\\
\phi_\alpha(p\') &= \frac{1}{\sqrt{2\pi\hbar}}\int dx\'\exp\left(-\frac{ip\'x\'}{\hbar}\right)\psi_\alpha(x\')
\end{aligned}
}
$$

↳ the wave functions in the position and momentum basis, written in terms of each other (they're Fourier transforms of each other).

## Gaussian wave packets

Wave function in the position basis:

$$
\boxed{\langle x\'|\alpha\rangle = \frac{1}{\pi^{1/4}\sqrt d}\exp\left(ikx\' - \frac{x\'^2}{2d^2}\right)}
$$

(a plane wave $e^{ikx\'}$ under a Gaussian envelope of width $d$).

Recall $|\alpha\rangle = \int dx\'|x\'\rangle\langle x\'|\alpha\rangle$, so

$$
\langle p\'|\alpha\rangle = \int dx\'\langle p\'|x\'\rangle\langle x\'|\alpha\rangle, \qquad \langle p\'|x\'\rangle = \frac{1}{\sqrt{2\pi\hbar}}\exp\left(-\frac{ip\'x\'}{\hbar}\right)
$$

$$
\langle p\'|\alpha\rangle = \int_{-\infty}^{\infty}dx\'\frac{1}{\sqrt{2\pi\hbar}}\frac{1}{\pi^{1/4}\sqrt d}\exp\left(-\frac{ip\'x\'}{\hbar} + ikx\' - \frac{x\'^2}{2d^2}\right)
$$

$$
\boxed{\langle p\'|\alpha\rangle = \sqrt{\frac{d}{\hbar\sqrt\pi}}\exp\left(-\frac{(p\' - \hbar k)^2d^2}{2\hbar^2}\right)}
$$

$\to$ also a Gaussian, centred at $p\' = \hbar k$.

### Uncertainty of the Gaussian

To obtain $\langle(\Delta x)^2\rangle = \langle x^2\rangle - \langle x\rangle^2$ we need these two.

$$
\langle x\rangle = \int_{-\infty}^{\infty}dx\'\langle\alpha|x\'\rangle x\'\langle x\'|\alpha\rangle
$$

with (writing $C = \frac{1}{\pi^{1/4}\sqrt d}$)

$$
\langle\alpha|x\'\rangle = C\exp\left(-ikx\' - \frac{x\'^2}{2d^2}\right) \implies \langle\alpha|x\'\rangle\langle x\'|\alpha\rangle = C^2\exp\left(-\frac{x\'^2}{d^2}\right)
$$

$\to$ a Gaussian (the phases cancel).

$$
\implies \langle x\rangle = \int_{-\infty}^{\infty}C^2\exp\left(-\frac{x\'^2}{d^2}\right)x\'dx\' = 0
$$

$\to$ by symmetry (odd integrand). And

$$
\langle x^2\rangle = \int dx\'\langle\alpha|\hat x^2|x\'\rangle\langle x\'|\alpha\rangle = \int dx\'x\'^2\langle\alpha|x\'\rangle\langle x\'|\alpha\rangle
$$

$\to$ remember this trick.

$$
= \frac{1}{\sqrt\pi d}\int_{-\infty}^{\infty}dx\'x\'^2\exp\left(-\frac{x\'^2}{d^2}\right)
$$

$$
\boxed{\langle x^2\rangle = \frac{d^2}{2}} \implies \langle(\Delta x)^2\rangle = \langle x^2\rangle - \langle x\rangle^2 = \frac{d^2}{2}
$$

Similarly (doing the same thing with the momentum space Gaussian, $\langle p\rangle = \hbar k$),

$$
\langle(\Delta p)^2\rangle = \langle p^2\rangle - \langle p\rangle^2 = \frac{\hbar^2}{2d^2} + \hbar^2k^2 - \hbar^2k^2 = \frac{\hbar^2}{2d^2}
$$

$$
\therefore \boxed{\langle(\Delta x)^2\rangle\langle(\Delta p)^2\rangle = \frac{\hbar^2}{4}}
$$

$\to$ **exactly**!

↳ this is an equality, and hence the Gaussian is the **minimum uncertainty wave packet**.

---

[← Translations and momentum](@/notes/quantum_13_translations_and_momentum.md) | Next: [Angular momentum →](@/notes/quantum_15_angular_momentum.md)
