+++
title = "Matrix representations for spin ½ systems"
date = 2026-10-19
draft = false

[taxonomies]
categories = ["Quantum Physics", "Physics"]
tags = ["physics", "quantum-mechanics"]

[extra]
lang = "en"
math = true
+++

## Base kets

For spin $\frac{1}{2}$ systems, base kets are $|S_z;\pm\rangle$, which we can write as $|\pm\rangle$.

$$
\Lambda_{a\'} = |a\'\rangle\langle a\'|, \qquad \sum_{a\'}\Lambda_{a\'} = I = 1
$$

In this case the identity can be written as:

$$
\boxed{\sum_{a\'}|a\'\rangle\langle a\'| = |+\rangle\langle+| + |-\rangle\langle-| = 1}
$$

since it can only take in two values.

## Writing Sz with outer products

The eigenvalue of the state is $\pm\frac{\hbar}{2}$. $\therefore$ we must be able to say $\hat S_z = \sum_{a\'}a\'\Lambda_{a\'}$ (from the [matrix representations notes](@/notes/quantum_06_matrix_representations.md#observables-in-their-own-eigenbasis)):

$$
\hat S_z = \frac{\hbar}{2}|+\rangle\langle+| + \left(-\frac{\hbar}{2}\right)|-\rangle\langle-|
$$

$$
\implies \hat S_z = \frac{\hbar}{2}\left(|+\rangle\langle+| - |-\rangle\langle-|\right)
$$

Applying this to say $|+\rangle$:

$$
\hat S_z|+\rangle = \frac{\hbar}{2}\left(|+\rangle\langle+|+\rangle - |-\rangle\langle-|+\rangle\right)
$$

since these are orthogonal: $\langle+|-\rangle = \langle-|+\rangle = 0$ and $\langle+|+\rangle = 1$ (normal)

$$
\boxed{\hat S_z|+\rangle = \frac{\hbar}{2}|+\rangle \quad\implies\quad \hat S_z|\pm\rangle = \pm\frac{\hbar}{2}|\pm\rangle \quad\text{(general)}}
$$

This is true only because $|+\rangle$ and $|-\rangle$ are

1. basis vectors
2. orthogonal
3. normal.

## Raising and lowering operators

There are two more operators:

$$
\begin{aligned}
S_+ &= \hbar|+\rangle\langle-| \quad \to \text{spin down to up} \\\\
S_- &= \hbar|-\rangle\langle+| \quad \to \text{up to down}
\end{aligned}
$$

again due to orthonormality,

$$
\boxed{S_+|+\rangle = 0, \qquad S_+|-\rangle = \hbar|+\rangle}
$$

The physical sense of $S_\pm$ is that they raise (or lower) the spin component by $\hbar$; if it cannot be raised (or lowered), we get a null ket. We'll see that these are just $S_x \pm iS_y$ in the [measurements notes](@/notes/quantum_08_measurements_and_sg.md#spin-flipping-operators).

## The matrices

Coming back to matrices:

$$
|+\rangle \doteq \begin{pmatrix} 1 \\\\ 0 \end{pmatrix}, \qquad |-\rangle \doteq \begin{pmatrix} 0 \\\\ 1 \end{pmatrix}
$$

$$
S_z \doteq \frac{\hbar}{2}\begin{pmatrix} 1 & 0 \\\\ 0 & -1 \end{pmatrix}, \qquad S_+ \doteq \hbar\begin{pmatrix} 0 & 1 \\\\ 0 & 0 \end{pmatrix}, \qquad S_- \doteq \hbar\begin{pmatrix} 0 & 0 \\\\ 1 & 0 \end{pmatrix}
$$

(This is where the **Pauli matrices** come from: $S_z = \frac{\hbar}{2}\sigma_z$.)

Why? Using the outer product as a matrix:

**Important:**

$$
\boxed{
|\alpha\rangle\langle\beta| \doteq \begin{pmatrix}
\langle a^{(1)}|\alpha\rangle\langle a^{(1)}|\beta\rangle^{\ast} & \langle a^{(1)}|\alpha\rangle\langle a^{(2)}|\beta\rangle^{\ast} & \cdots \\\\
\langle a^{(2)}|\alpha\rangle\langle a^{(1)}|\beta\rangle^{\ast} & \langle a^{(2)}|\alpha\rangle\langle a^{(2)}|\beta\rangle^{\ast} & \cdots \\\\
\vdots & \vdots & \ddots
\end{pmatrix}
}
$$

$$
\hat S_z = \frac{\hbar}{2}\left(|+\rangle\langle+| - |-\rangle\langle-|\right)
$$

$$
\begin{aligned}
\hat S_z \doteq \frac{\hbar}{2}\Bigg[ &\begin{pmatrix} \langle+|+\rangle\langle+|+\rangle^{\ast} & \langle+|+\rangle\langle-|+\rangle^{\ast} \\\\ \langle-|+\rangle\langle+|+\rangle^{\ast} & \langle-|+\rangle\langle-|+\rangle^{\ast} \end{pmatrix} \\\\
{-} &\begin{pmatrix} \langle+|-\rangle\langle+|-\rangle^{\ast} & \langle+|-\rangle\langle-|-\rangle^{\ast} \\\\ \langle-|-\rangle\langle+|-\rangle^{\ast} & \langle-|-\rangle\langle-|-\rangle^{\ast} \end{pmatrix} \Bigg]
\end{aligned}
$$

$$
\hat S_z \doteq \frac{\hbar}{2}\left[\begin{pmatrix} 1 & 0 \\\\ 0 & 0 \end{pmatrix} - \begin{pmatrix} 0 & 0 \\\\ 0 & 1 \end{pmatrix}\right] = \frac{\hbar}{2}\begin{pmatrix} 1 & 0 \\\\ 0 & -1 \end{pmatrix}
$$

---

[← Matrix representations](@/notes/quantum_06_matrix_representations.md) | Next: [Measurements, probabilities and the S-G experiment →](@/notes/quantum_08_measurements_and_sg.md)
