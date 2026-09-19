+++
title = "Solving quadratic Diophantine equations"
date = 2026-09-19
draft = false

[taxonomies]
categories = ["Puzzles", "Math"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

Writing this stuff here so that I can come back to it later and remember these ideas better. Sadly, we can only share solutions to the first 100 problems, but that's for the greater good. Anyway.

> This problem is solved using continued fractions, which I'll explain in section 3, right after a brute-force solution that fails badly.

## Problem (rephrased)

Consider quadratic Diophantine equations of the form:

$$
x^2 - Dy^2 = 1
$$

This equation has a minimum solution in $x$. For example, when $D = 13$, the minimum solution pair $(x, y)$ is $(649, 180)$. We will assume (correctly) that there are no solutions in positive integers when $D$ is a perfect square. For $D \in \\{2, 3, \ldots, 1000\\}$, find the value of $D$ for which the minimum solution $x$ is the largest.

## Solution (brute force)

Going with John Carmack's advice: write any code, optimise later. This equation, btw, is also called Pell's equation. So, we know that if a number $A$ is a perfect square, then:

$$
A \equiv 0 \pmod{4} \quad \text{or} \quad A \equiv 1 \pmod{4}
$$

So, the brute-force solution is essentially: for each $D$, find a $y^2$ value that satisfies either of the two relations above, and then find the corresponding $x^2$. Note that not all numbers of the form $4k$ or $4k+1$ are perfect squares, so we'll have to check whether what we have is one or not.

There are some more cool things we can say about the equation. For example, we can prove that if $D \equiv 3 \pmod{4}$, then $y^2 \equiv 1 \pmod{4}$ has to be true. And all the numbers will satisfy that. But unfortunately, it doesn't really help us speed up the calculations, since we're still checking each number.

**Note:** to check whether a number is a perfect square, I am using:

```python
import math
int(math.sqrt(n))**2 == n # Good for smaller values of n
math.isqrt(n)**2 == n # for larger n
```

This is the brute-force code:

```python
import math

# Optimize the algo

def compute(D):
  smallest = 0
  k_y = 1
  while True:
    if math.isqrt(4*k_y+1)**2 == 4*k_y+1:
      y2 = 4*k_y + 1
      x2 = D*y2+1
      if math.isqrt(x2)**2 == x2:
        if x2 > smallest:
          smallest = x2
        break
    elif math.isqrt(4*k_y)**2 == 4*k_y:
      y2 = 4*k_y
      x2 = D*y2+1
      if math.isqrt(x2)**2 == x2:
        if x2 > smallest:
          smallest = x2
        break
    k_y += 1

  return (smallest, y2)

Dval = 21
x2, y2 = compute(Dval)
print(f"X^2 value: {x2}, Y^2 value: {y2}, Dval: {Dval}")

largest = 0

for D in range(2, 1001):
  if int(math.sqrt(D)) ** 2 == D:
    continue
  x2, y2 = compute(D)
  print(f"For D={D}, x2={x2}, y2={y2}")
  if x2 > largest:
    largest = x2

print(int(math.sqrt(largest)))
```

The first breaking point is $D = 61$, which is a pretty important number: the equation so formed is $x^2 - 61y^2 = 1$, which is the equation that **Jayadeva and Bhaskara** worked on during medieval times, and the equation that **Fermat** posed as a challenge. The medieval guys solved it using the *chakravala* method.

Anyway, the important part is that the numbers go into the trillions, and since we're incrementing by just 1 each time, no amount of parallelization or multiprocessing can fix this!

So, the problem this time is in the math. We haven't used any results! So, I went online, searched for how to solve quadratic Diophantine equations, and found all the theory I shared above, along with the method that everyone uses to solve them!

## The continued fractions method

Consider the equation $x^2 - Dy^2 = 1$ once more. Let's rewrite it as:

$$
\begin{aligned}
(x-\sqrt{D}y)(x+\sqrt{D}y) &= 1 \\\\
\implies \left(\frac{x}{y}-\sqrt{D}\right)\left(\frac{x}{y}+\sqrt{D}\right) &= \frac{1}{y^2} \\\\
\implies \frac{x}{y}-\sqrt{D} &= \frac{1}{y^2 \cdot \left(\frac{x}{y}+\sqrt{D}\right)}
\end{aligned}
$$

Now, since $\frac{x^2}{y^2} = \frac{1+Dy^2}{y^2} = \frac{1}{y^2} + D$ and $y$ is a positive integer, we know that $\frac{x}{y} \gt \sqrt{D}$. This further implies that $\frac{x}{y} + \sqrt{D} \gt 2\sqrt{D}$, and since $D \ge 2$, we get $\frac{x}{y} + \sqrt{D} \gt 2$. This leads to the following inequality:

$$
\left| \frac{x}{y} - \sqrt{D}\right| \lt \frac{1}{2y^2}
$$

And this is beautiful, because if you open page 153 of Hardy and Wright's *An Introduction to the Theory of Numbers*, you'll find a proof of the following theorem:

> If $\left|\frac{p}{q} - x \right| \lt \frac{1}{2q^2}$, then $\frac{p}{q}$ is a convergent.

So, what's a convergent? That's where we'll have to dive into the theory of continued fractions.

### Theory

Finite continued fractions are basically:

$$
a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \cfrac{1}{\ddots + \cfrac{1}{a_N}}}}
$$

which is compactly represented as $[a_0, a_1, \ldots, a_N]$. Each $a_i$ is called a quotient. Now, it's not too hard to see that:

$$
\begin{aligned}
[a_0] &= a_0 \\\\
[a_0, a_1] &= \frac{a_0a_1 + 1}{a_1} \\\\
[a_0, a_1, a_2] &= \frac{a_2a_1a_0 + a_2 + a_0}{a_2a_1 + 1} \\\\
&\vdots
\end{aligned}
$$

We call $[a_0, a_1, \ldots, a_k]$ the $k^{\text{th}}$ *convergent*, for all $k \le N$.

There's a whole world of work that has been done on these guys, but lemme jump to what's important for us here: the page 153 theorem.

> If $\left|\frac{p}{q} - x \right| \lt \frac{1}{2q^2}$, then $\frac{p}{q}$ is a convergent.

Now that we understand the terms, let's see how continued fractions even come into the picture. Firstly, let's write the inequality as an equality:

$$
\frac{p}{q} - x = \frac{\epsilon \theta}{q^2}, \quad \text{where } \epsilon = \pm 1 \text{ and } \theta \in \left(0, \tfrac{1}{2}\right)
$$

Now, we'll represent $\frac{p}{q}$ as a continued fraction (we can do that for any rational number). So, $\frac{p}{q} = [a_0, a_1, \ldots, a_N]$.

Now consider a simple example. Say the continued fraction was $[1, 2, 3]$; this would mean the number $\frac{p}{q}$ is:

$$
\frac{p}{q} = 1 + \cfrac{1}{2 + \cfrac{1}{3}} = \frac{10}{7}
$$

We could always rewrite the continued fraction with one extra term, like this: $[1, 2, 2, 1]$. Note what it does:

$$
\frac{p}{q} = 1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{1}}} = \frac{10}{7}
$$

Since $\frac{1}{1}$ is just $1$, we can effectively **change** the number of terms in the continued fraction. In general:

$$
[a_0, a_1, \ldots, a_N] = [a_0, a_1, \ldots, a_N - 1, 1]
$$

Awesome. Now, since $\epsilon$ is just an artifact of the modulus, and we control the value of $N$, we can choose $N$ so that $\epsilon = (-1)^{N-1}$.

Now consider a number $x$ defined as follows:

$$
x = \frac{wp_N + p_{N-1}}{wq_N + q_{N-1}}
$$

where $\frac{p_N}{q_N}$ and $\frac{p_{N-1}}{q_{N-1}}$ are the last and second-last convergents of $\frac{p}{q}$, respectively.

The reason we do this is that we can show by induction that:

$$
\frac{p_n}{q_n} = \frac{a_np_{n-1} + p_{n-2}}{a_nq_{n-1} + q_{n-2}}
$$

and since in our case $x$ is larger than $\frac{p_N}{q_N} = \frac{p}{q}$, we let it be the "next hypothetical convergent" with some quotient $w$.

With that, the equation becomes:

$$
\frac{\epsilon \theta}{q_N^2} = \frac{p_N}{q_N} - x = \frac{q_{N-1}p_N - p_{N-1}q_N}{q_N(wq_N + q_{N-1})}
$$

And since we know what $\epsilon$ is:

$$
\frac{(-1)^{N-1} \theta}{q_N^2} = \frac{q_{N-1}p_N - p_{N-1}q_N}{q_N(wq_N + q_{N-1})}
$$

Okay, back to example land. Consider again $[1, 2, 3]$ as the continued fraction for some $\frac{p}{q}$:

$$
\begin{aligned}
\frac{p_2}{q_2} &= [1, 2, 3] = \frac{10}{7} \\\\
\frac{p_1}{q_1} &= [1, 2] = \frac{3}{2}
\end{aligned}
$$

You can see that $p_2q_1 - p_1q_2 = -1$. In fact, this will always be true for the $N^{\text{th}}$ case as well:

$$
p_Nq_{N-1} - p_{N-1}q_N = (-1)^{N-1}
$$

So with this, we get:

$$
\begin{aligned}
\frac{(-1)^{N-1} \theta}{q_N^2} &= \frac{(-1)^{N-1}}{q_N(wq_N + q_{N-1})} \\\\
\implies \theta &= \frac{q_N}{wq_N + q_{N-1}} \\\\
\implies w &= \frac{1}{\theta} - \frac{q_{N-1}}{q_N}
\end{aligned}
$$

Therefore, $w > 1$, since $\theta \in \left(0, \frac{1}{2}\right)$. Now, there is another theorem which states the following:

> If $x = \frac{P\zeta + R}{Q\zeta + S}$, where $\zeta \gt 1$ and $P, Q, R, S$ are integers such that $Q \gt S \gt 0$ and $PS - QR = \pm 1$, then $\frac{R}{S}$ and $\frac{P}{Q}$ are consecutive convergents to the simple continued fraction whose value is $x$.

And:

> If $\frac{R}{S}$ is the $(n-1)^{\text{th}}$ convergent and $\frac{P}{Q}$ is the $n^{\text{th}}$, then $\zeta$ is the $(n+1)^{\text{th}}$ or the last convergent.

You can probably see now why we chose our $x$ the way we did: our setup falls directly under this theorem. Hence, we can say that $\frac{p_{N-1}}{q_{N-1}}$ and $\frac{p_N}{q_N}$ are consecutive convergents to $x$. But since $\frac{p}{q} = \frac{p_N}{q_N}$, this means $\frac{p}{q}$ is a convergent.

## Back to the problem

So, we now know that in the inequality:

$$
\left| \frac{x}{y} - \sqrt{D}\right| \lt \frac{1}{2y^2}
$$

the fraction $\frac{x}{y}$ must be a convergent of $\sqrt{D}$. This is helpful, because now we can understand why the continued fractions algorithm even works out.
