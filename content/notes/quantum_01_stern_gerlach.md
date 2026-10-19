+++
title = "The Stern-Gerlach experiment"
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

```text
                                   ┌─────────┐
                                   │    N    │
  ┌────────┐                       └─────────┘        ▲ z
  │   Ag   │        Ag beam            ↓   ↓          │
  │  oven  │ ─────────────────────────────────────►   │
  └────────┘                           ↓   ↓
                                   ┌─────────┐
                                   │    S    │
                                   └─────────┘
```

The Ag atom has an angular momentum solely due to its outer $e^-$ and spin $\implies$ intrinsic.

$$
\therefore \vec\mu_{\text{atom}} \propto \vec S_{\text{electron}}
$$

turns out:

$$
\boxed{\vec\mu_{\text{atom}} = \frac{e}{m_e c}\vec S}
$$

$F_z$ due to the field:

$$
F_z = \frac{\partial}{\partial z}\left(\vec\mu\cdot\vec B\right) \simeq \mu_z\frac{\partial B_z}{\partial z}
$$

ignoring $\vec B$ in other directions.

$\therefore$ a particle with $\mu_z > 0$ ($S_z < 0$) experiences a **downward** force and $\mu_z < 0$ ($S_z > 0$) **upwards**.

Then an SG$\hat z$ is measuring the z-component of $\vec\mu$, or the z-component of $\vec S$ upto a proportionality factor.

```text
                  ┌──────────┐   Sz+     ┌──────────┐   Sx+
   Ag  ─────────► │    SG    │ ────────► │    SG    │ ────────►
                  │  z-axis  │ ──► ■     │  x-axis  │ ────────►
                  └──────────┘   Sz-     └──────────┘   Sx-
                              (blocked)
```

$$
S_z = \pm\frac{\hbar}{2}
$$

↳ splitting into two beams $\to$ referred to as **space quantization**.

## Sequential Stern-Gerlach experiments

```text
               ┌───────┐  Sz+     ┌───────┐  Sx+     ┌───────┐  Sz+
   Ag  ──────► │  SG   │ ───────► │  SG   │ ───────► │  SG   │ ───────►
               │   z   │ ──► ■    │   x   │ ──► ■    │   z   │ ───────►
               └───────┘  Sz-     └───────┘  Sx-     └───────┘  Sz-
```

The selection of the $S_x+$ beam (or $S_x-$) destroys all information about $S_z$ stored previously. The last SG$\hat z$ splits into $S_z+$ and $S_z-$ again, even though we had blocked $S_z-$ at the start!

**For every measurement you make, the other non-commuting observables are in a superposition of all possible states.**

## Analogies from polarized light

Drawing analogies from polarized light,

$$
\begin{aligned}
|S_x;\pm\rangle &\stackrel{?}{=} \pm\frac{1}{\sqrt{2}}|S_z;+\rangle + \frac{1}{\sqrt{2}}|S_z;-\rangle \\\\
|S_y;\pm\rangle &\stackrel{?}{=} \frac{1}{\sqrt{2}}|S_z;+\rangle \pm \frac{i}{\sqrt{2}}|S_z;-\rangle
\end{aligned}
$$

These are vectors in some high dimensional field (the **Hilbert space**). We'll actually derive these later in [measurements and the S-G experiment](@/notes/quantum_08_measurements_and_sg.md).

---

Next: [Kets and the Hilbert space →](@/notes/quantum_02_kets_and_hilbert_space.md)
