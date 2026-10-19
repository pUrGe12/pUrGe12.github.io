+++
title = "The hydrogen atom: angular part"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## The Hamiltonian

We start with the Hamiltonian ($\mu$ is the reduced mass):

$$
\hat H = \frac{\hat p^2}{2\mu} - \frac{e^2}{4\pi\varepsilon_0r}
$$

but we want to transition to spherical (polar) coordinates.

In 3D, $\hat{\vec p} = -i\hbar\nabla$ (the 3D version of $p_x = -i\hbar\frac{\partial}{\partial x}$ from the [wave functions notes](@/notes/quantum_14_wave_functions.md#momentum-in-the-position-basis)):

$$
p_x = -i\hbar\frac{\partial}{\partial x}, \qquad p_y = -i\hbar\frac{\partial}{\partial y}, \qquad p_z = -i\hbar\frac{\partial}{\partial z}
$$

$$
\hat p^2 = p_x^2 + p_y^2 + p_z^2 = -\hbar^2\nabla^2
$$

$\to$ the Laplacian.

$$
\implies \hat H = -\frac{\hbar^2\nabla^2}{2\mu} - \frac{e^2}{4\pi\varepsilon_0r}
$$

Pick $\nabla^2$ in spherical coordinates:

$$
\nabla^2 = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial}{\partial r}\right) + \frac{1}{r^2}\left[\frac{1}{\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial}{\partial\theta}\right) + \frac{1}{\sin^2\theta}\frac{\partial^2}{\partial\phi^2}\right]
$$

## Angular momentum in spherical coordinates

Now, we know

$$
\vec L = \vec r\times\vec p = \begin{vmatrix} \hat x & \hat y & \hat z \\\\ x & y & z \\\\ p_x & p_y & p_z \end{vmatrix}
$$

$$
\implies L_x = yp_z - zp_y, \qquad L_y = zp_x - xp_z, \qquad L_z = xp_y - yp_x
$$

$$
\implies L_z = -i\hbar\left(x\frac{\partial}{\partial y} - y\frac{\partial}{\partial x}\right)
$$

With $x = r\sin\theta\cos\phi$, $y = r\sin\theta\sin\phi$, $z = r\cos\theta$:

$$
\frac{\partial}{\partial\phi} = \frac{\partial x}{\partial\phi}\frac{\partial}{\partial x} + \frac{\partial y}{\partial\phi}\frac{\partial}{\partial y} + \frac{\partial z}{\partial\phi}\frac{\partial}{\partial z} = -y\frac{\partial}{\partial x} + x\frac{\partial}{\partial y}
$$

$$
\implies \boxed{L_z = -i\hbar\frac{\partial}{\partial\phi}}
$$

Turns out $-\frac{\hat L^2}{\hbar^2}$ in spherical coordinates is exactly the bracket above:

$$
\hat L^2 = -\hbar^2\left[\frac{1}{\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial}{\partial\theta}\right) + \frac{1}{\sin^2\theta}\frac{\partial^2}{\partial\phi^2}\right]
$$

$$
\implies \boxed{\nabla^2 = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial}{\partial r}\right) - \frac{\hat L^2}{\hbar^2r^2}}
$$

Substituting this back:

$$
\boxed{\hat H = -\frac{\hbar^2}{2\mu r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial}{\partial r}\right) + \frac{\hat L^2}{2\mu r^2} - \frac{e^2}{4\pi\varepsilon_0r}}
$$

## Separation of variables

Now from the eigenvalue equation, we know $\hat H\psi = E\psi$

$$
\implies -\frac{\hbar^2}{2\mu}\frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial\psi}{\partial r}\right) + \frac{\hat L^2\psi}{2\mu r^2} - \frac{e^2\psi}{4\pi\varepsilon_0r} = E\psi
$$

We guess the solution to be

$$
\psi(r, \theta, \phi) = R(r)Y(\theta, \phi)
$$

$\implies \frac{\partial}{\partial r}$ acts only on $R(r)$, and $\hat L^2$ only on $(\theta, \phi)$:

$$
-\frac{\hbar^2}{2\mu r^2}Y\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \frac{R\hat L^2Y}{2\mu r^2} - \frac{e^2}{4\pi\varepsilon_0r}RY = ERY
$$

Now we rearrange a bit (multiply through by $\frac{2\mu r^2}{\hbar^2RY}$):

$$
\underbrace{\frac{1}{R}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \frac{2\mu r^2}{\hbar^2}\left(E + \frac{e^2}{4\pi\varepsilon_0r}\right)}\_{\text{only } r} = \underbrace{\frac{1}{\hbar^2}\frac{\hat L^2Y}{Y}}\_{\text{only } (\theta, \phi)}
$$

This is only possible when they're both the same constant, call it $\beta$:

$$
\implies \hat L^2Y = \beta\hbar^2Y \qquad (1)
$$

$$
\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \frac{2\mu r^2}{\hbar^2}\left(E + \frac{e^2}{4\pi\varepsilon_0r}\right)R - \beta R = 0 \qquad (2)
$$

(2) is the radial part, for the [next notes](@/notes/quantum_21_hydrogen_atom_radial.md).

## The angular part

We solve the angular part first. With $\hat L^2$ from above, (1) is

$$
\frac{1}{\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial Y}{\partial\theta}\right) + \frac{1}{\sin^2\theta}\frac{\partial^2Y}{\partial\phi^2} + \beta Y = 0
$$

This is another PDE, and we try to use $Y = \Theta(\theta)\Phi(\phi)$ (and multiply by $\frac{\sin^2\theta}{\Theta\Phi}$):

$$
\underbrace{\frac{\sin\theta}{\Theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) + \beta\sin^2\theta}\_{\text{only } \theta} + \underbrace{\frac{1}{\Phi}\frac{d^2\Phi}{d\phi^2}}\_{\text{only } \phi} = 0
$$

Each piece is again a constant. Call the $\phi$ constant "$-m^2$":

$$
\implies \frac{1}{\Phi}\frac{d^2\Phi}{d\phi^2} = -m^2 \implies \boxed{\Phi = e^{im\phi}}
$$

$\to$ Euler's equation. If $m$ is negative, it's just $e^{-i|m|\phi}$.

Since $\phi$ and $\phi + 2\pi$ are the same points,

$$
e^{im(\phi + 2\pi)} = e^{im\phi} \implies \boxed{e^{2\pi im} = 1} \implies m \in \mathbb{Z}
$$

as $\cos 2\pi m = 1$ and $\sin 2\pi m = 0$.

Note, in spherical coordinates:

$$
\hat L_z\Phi = -i\hbar\frac{\partial}{\partial\phi}e^{im\phi} = m\hbar e^{im\phi} = m\hbar\Phi
$$

Now $\Theta$:

$$
\boxed{\frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) + \left(\beta - \frac{m^2}{\sin^2\theta}\right)\Theta = 0}
$$

## We already know beta

Now this ODE is tough to solve. Notice that $Y(\theta, \phi)$ is a simultaneous eigenfunction of $\hat L^2$ and $\hat L_z$.

Let's look at the ladder operator $L_\pm = L_x \pm iL_y$:

$$
(L_+)^\dagger = L_x^\dagger - iL_y^\dagger = L_x - iL_y = L_-
$$

(since $L$ is Hermitian), and

$$
[L_z, L_+] = [L_z, L_x + iL_y] = [L_z, L_x] + i[L_z, L_y]
$$

with $[L_z, L_x] = i\hbar L_y$ and $[L_z, L_y] = -i\hbar L_x$ (from $[L_i, L_j] = i\hbar\varepsilon_{ijk}L_k$)

$$
\implies \boxed{[\hat L_z, \hat L_+] = \hbar\hat L_+}, \qquad [\hat L_z, \hat L_-] = -\hbar\hat L_-
$$

And $[L^2, L_\pm] = 0$ $\to$ they commute with $L^2$. Duh.

So $L_+|\beta, m\rangle$ raises $m$ by 1 and leaves $\beta$ alone. From $[L_z, L_+] = \hbar L_+ \implies L_zL_+ = L_+L_z + \hbar L_+$:

$$
\begin{aligned}
L_zL_+|\beta, m\rangle &= L_+L_z|\beta, m\rangle + \hbar L_+|\beta, m\rangle \\\\
&= m\hbar L_+|\beta, m\rangle + \hbar L_+|\beta, m\rangle = (m + 1)\hbar L_+|\beta, m\rangle
\end{aligned}
$$

(recall how $J_z$ acted), and

$$
L^2L_+|\beta, m\rangle = L_+L^2|\beta, m\rangle = \beta\hbar^2L_+|\beta, m\rangle
$$

> Dude, I'm basically re-deriving the eigenvalues of $J_z$ and $\vec J^2$ ($L_z$ and $L^2$ here).

Everything from the [angular momentum notes](@/notes/quantum_15_angular_momentum.md) applies. Come back.

So, we know $Y(\theta, \phi) = \Theta(\theta)e^{im\phi}$, and we also have $L^2Y = \beta\hbar^2Y$ $\implies$ $Y$ is an eigenfunction of $L^2$. And

$$
L^2\left(\Theta(\theta)e^{im\phi}\right) = -\hbar^2\left(\frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) - \frac{m^2}{\sin^2\theta}\Theta\right)e^{im\phi}
$$

(we already showed that $-\frac{L^2}{\hbar^2}$ is the bracketed part of $\nabla^2$, and $\frac{\partial^2}{\partial\phi^2}$ on $e^{im\phi}$ gives $-m^2$).

$$
\implies \beta\hbar^2\Theta(\theta)e^{im\phi} = -\hbar^2\left(\frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) - \frac{m^2}{\sin^2\theta}\Theta\right)e^{im\phi}
$$

$$
\implies \frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) + \left(\beta - \frac{m^2}{\sin^2\theta}\right)\Theta = 0
$$

Damn, that's the $\Theta$ equation! So, it's the $L^2$ eigenvalue equation in polar coordinates.

But we know that $L^2|l, m\rangle = \hbar^2l(l + 1)|l, m\rangle$. $\therefore$ in our case,

$$
\boxed{\beta = l(l + 1)}
$$

$$
\implies \boxed{\frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) + \left(l(l + 1) - \frac{m^2}{\sin^2\theta}\right)\Theta = 0}
$$

We know $m \in \mathbb{Z}$ because of $e^{2\pi im} = 1$ $\implies$ $l$ is an integer too (since $m$ runs from $-l$ to $l$ in integer steps).

$\therefore$ for orbital angular momentum ($\hat L$, not the general $\hat J$) we only have integer values of $l$. The half-integers are left for spin.

## Building the spherical harmonics

We also know $J_-J_+ = \vec J^2 - J_z^2 - \hbar J_z$. In orbital angular momentum we replace $J$ with $L$ and rearrange:

$$
\boxed{L^2 = L_-L_+ + L_z^2 + \hbar L_z}
$$

We know $L_z|l, m\rangle = m\hbar|l, m\rangle$ from before

$$
\implies L^2Y = L_-L_+Y + (m^2 + m)\hbar^2Y
$$

($Y$ being the state $|l, m\rangle$). But $L^2Y = l(l + 1)\hbar^2Y$

$$
\implies l(l + 1)\hbar^2Y = L_-L_+Y + (m^2 + m)\hbar^2Y
$$

$$
\implies L_-L_+Y = \left[l(l + 1) - m(m + 1)\right]\hbar^2Y
$$

At this point, we can start denoting $Y$ as $Y_{lm}$.

At the top state, $m = l$. We know $L_+$ kills it, to give a null ket, and $l(l + 1) - l(l + 1) = 0$:

$$
\implies \boxed{L_+Y_{ll} = 0}
$$

### The ladders in spherical coordinates

We need $L_\pm$ as differential operators. It's the same chain-rule game as $L_z = -i\hbar\frac{\partial}{\partial\phi}$, just longer, and it gives

$$
L_x = i\hbar\left(\sin\phi\frac{\partial}{\partial\theta} + \cot\theta\cos\phi\frac{\partial}{\partial\phi}\right), \qquad L_y = i\hbar\left(-\cos\phi\frac{\partial}{\partial\theta} + \cot\theta\sin\phi\frac{\partial}{\partial\phi}\right)
$$

so that ($\sin\phi - i\cos\phi = -ie^{i\phi}$)

$$
\boxed{L_+ = \hbar e^{i\phi}\left(\frac{\partial}{\partial\theta} + i\cot\theta\frac{\partial}{\partial\phi}\right)}, \qquad \boxed{L_- = -\hbar e^{-i\phi}\left(\frac{\partial}{\partial\theta} - i\cot\theta\frac{\partial}{\partial\phi}\right)}
$$

On a general $Y_{lm}$:

$$
L_+\left(\Theta e^{im\phi}\right) = \hbar e^{i(m + 1)\phi}\left(\frac{d\Theta}{d\theta} - m\cot\theta\Theta\right)
$$

### The top state

At $m = l$, this is 0:

$$
\implies \boxed{\frac{d\Theta}{d\theta} - l\cot\theta\Theta = 0}
$$

Solve this ($\frac{d\Theta}{\Theta} = l\cot\theta d\theta \implies \ln\Theta = l\ln\sin\theta$) to get

$$
\boxed{\Theta = \sin^l\theta}
$$

$$
\implies \boxed{Y_{ll} = c_l\sin^l\theta e^{il\phi}}
$$

$\to$ $c_l$ is some constant.

### Going down

Applying the lowering formula from the [angular momentum notes](@/notes/quantum_15_angular_momentum.md#the-ladder-coefficients):

$$
J_-|j, m\rangle = \hbar\sqrt{(j + m)(j - m + 1)}|j, m - 1\rangle
$$

and

$$
L_-\left(\Theta e^{im\phi}\right) = -\hbar e^{i(m - 1)\phi}\left(\frac{d\Theta}{d\theta} + m\cot\theta\Theta\right)
$$

Equating this with the previous formula,

$$
\implies \boxed{\Theta_{l,m-1} = \frac{-1}{\sqrt{(l + m)(l - m + 1)}}\left(\frac{d\Theta_{lm}}{d\theta} + m\cot\theta\Theta_{lm}\right)}
$$

We use this to build up the $Y_{lm}$ equations.

### Example: l = 2

For $l = 2$: $\beta = l(l + 1) = 6$, and 5 states of $m$: $-2, -1, 0, 1, 2$.

We know from $\Theta_{ll} = \sin^l\theta$ $\implies \Theta_{22} = \sin^2\theta$

$$
\implies \boxed{Y_{22} = c\sin^2\theta e^{2i\phi}}
$$

Now we can go lower using $\Theta_{l,m-1}$ $\implies$ $\Theta_{21}$ (cause we started from $m = l$). The prefactor is $\frac{-1}{\sqrt{4\cdot 1}} = -\frac{1}{2}$, and

$$
\frac{d\Theta_{22}}{d\theta} + 2\cot\theta\Theta_{22} = 2\sin\theta\cos\theta + 2\cos\theta\sin\theta = 4\sin\theta\cos\theta
$$

$$
\implies \boxed{\Theta_{21} = -\frac{1}{2}(4\sin\theta\cos\theta) = -2\sin\theta\cos\theta}
$$

and so on, until we get to $\Theta_{2,-2}$.

The constant $c$ can be obtained by forcing normalization:

$$
\int|Y_{22}|^2d\Omega = c^2\int_0^{2\pi}d\phi\int_0^{\pi}\sin^4\theta\sin\theta d\theta = c^2\cdot 2\pi\cdot\frac{16}{15} = 1 \implies c = \sqrt{\frac{15}{32\pi}}
$$

$$
\therefore \boxed{Y_{22} = \sqrt{\frac{15}{32\pi}}\sin^2\theta e^{2i\phi}}, \qquad \boxed{Y_{21} = -\sqrt{\frac{15}{8\pi}}\sin\theta\cos\theta e^{i\phi}}
$$

(the same $c$ carries down, since the lowering formula keeps things normalized). These are the standard **spherical harmonics**.

> Imp. stuff: a state like $\frac{1}{\sqrt 2}Y_{21} + \frac{1}{\sqrt 2}Y_{3,-2}$ means $|\psi\rangle = \frac{1}{\sqrt 2}|2, 1\rangle + \frac{1}{\sqrt 2}|3, -2\rangle$, and $L_z|\psi\rangle = m\hbar|\psi\rangle$ only if $|\psi\rangle$ is an eigenket. This one isn't: it mixes $m = 1$ and $m = -2$.

---

[← Harmonic oscillator wave functions and time dependence](@/notes/quantum_19_harmonic_oscillator_wave_functions.md) | Next: [The hydrogen atom: radial part →](@/notes/quantum_21_hydrogen_atom_radial.md)
