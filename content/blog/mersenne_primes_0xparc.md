+++
title = "0xPARC's mersenne prime puzzle"
date = 2026-09-16
draft = true

[taxonomies]
categories = ["Puzzles", "Math"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

Well, technically they never mentioned Mersenne primes, but it was pretty obvious if you've watched the [Numberphile videos](https://www.youtube.com/playlist?list=PLt5AfwLFPxWKsTwVXpLscZdfiiqAkkGCA) on them, or followed the hype around the LARGEST PRIMES ever discovered, they were all Mersenne primes!

Let's get to the question.

## Question

Are there any nontrivial solutions to the system of equations

$$
\begin{aligned}
a + b + c + d &\equiv 0 \pmod{p} &&\text{(1)} \\\\
a^2 + b^2 + c^2 + d^2 &\equiv 0 \pmod{p} &&\text{(2)} \\\\
a^3 + b^3 + c^3 + d^3 &\equiv 0 \pmod{p} &&\text{(3)}
\end{aligned}
$$

for $p = 2^{127} - 1$?

## Solution

### Collapsing the system into a single product

From (1) we can write:

$$
d \equiv -(a + b + c) \pmod{p} \tag{4}
$$

Substituting (4) into (3) gives:

$$
a^3 + b^3 + c^3 - (a + b + c)^3 \equiv 0 \pmod{p} \tag{5}
$$

Now we have an `identity` with these cubes, and that is:

$$
(a+b+c)^3 - (a^3+b^3+c^3) = 3(a+b)(b+c)(a+c) \tag{6}
$$

We can write (6) as a congruence, since any equation can be written as a congruent relation in the mods. Combining it with (5), we get the following implication:

$$
\begin{aligned}
3(a+b)(b+c)(a+c) &\equiv 0 \pmod{p} \\\\
\implies (a+b)(b+c)(a+c) &\equiv 0 \pmod{p}
\end{aligned}
\tag{7}
$$

Dropping the $3$ is allowed because $p \neq 3$, so $3$ is invertible mod $p$.

Now, $p$ is prime, and a product can only vanish mod a prime if one of its factors does — that's Euclid's lemma. So one of the three factors in (7) must be $\equiv 0 \pmod{p}$. They are interchangeable under a relabelling of $a$, $b$ and $c$, so we lose nothing by assuming it's $(a+b)$:

$$
\begin{aligned}
a+b &\equiv 0 \pmod{p} \\\\
\implies a &\equiv -b \pmod{p}
\end{aligned}
\tag{8}
$$

And from (1), we can say:

$$
d \equiv -c \pmod{p} \tag{9}
$$

### Bringing in the squares

Substituting (8) and (9) into (2):

$$
\begin{aligned}
a^2 + b^2 + c^2 + d^2 &\equiv 0 \pmod{p} \\\\
\implies 2a^2 + 2c^2 &\equiv 0 \pmod{p} \\\\
\implies a^2 &\equiv -c^2 \pmod{p}
\end{aligned}
\tag{10}
$$

Halving is fine here, since $p$ is odd. Now suppose $c \not\equiv 0 \pmod{p}$. Then $c$ is invertible mod $p$, and we can divide (10) through by $c^2$:

$$
\left(\frac{a}{c}\right)^2 \equiv -1 \pmod{p} \tag{11}
$$

So the whole question comes down to this: does $-1$ have a square root mod $p$?

### Why (11) cannot happen

The following statement is true and well known in modular math:

> No prime $p$ of the form $2^n - 1$, with $n \geq 2$, can divide $x^2 + 1$

Why's that? Here's a quick derivation — we'll do it for our $p$, but the same argument works for any $n \geq 2$. We start by assuming that $x^2+1$ is indeed divisible by $p$:

$$
x^2 \equiv -1 \pmod{p} \tag{12}
$$

Raising both sides of (12) to the power of $\frac{p-1}{2}$:

$$
x^{p-1} \equiv (-1)^{\frac{p-1}{2}} \pmod{p} \tag{13}
$$

The LHS of (13) is where Fermat's little theorem comes in. It states that:

> If $p$ is a prime number and $p$ does not divide $a$, then $a^{p-1}$ leaves a remainder of $1$ when divided by $p$.

In our case, $p$ doesn't divide $x$, it really can't, because if it did, then $p$ would divide $x^2$ and hence could not divide $x^2+1$. So the LHS of (13) is just $1$.

And due to $p$ being a Mersenne prime, we have:

$$
\begin{aligned}
p &= 2^{127} - 1 \\\\
\implies p - 1 &= 2^{127} - 2 \\\\
\implies \frac{p - 1}{2} &= 2^{126} - 1
\end{aligned}
\tag{14}
$$

And $2^{126} - 1$ is an odd number, which means the RHS of (13) just stays $-1$. So (13) becomes:

$$
\begin{aligned}
1 &\equiv -1 \pmod{p} \\\\
\implies 2 &\equiv 0 \pmod{p}
\end{aligned}
\tag{15}
$$

Or, $p$ divides $2$ exactly. But this is only possible when $p$ is either $1$ or $2$. Our $p$ is very much larger than $2$, so our assumption (12) is false.

### Wrapping up

So $-1$ has no square root mod $p$, and (11) is impossible. That kills the supposition we made to get there, leaving $c \equiv 0 \pmod{p}$.

Everything else follows immediately. From (10), $a^2 \equiv -c^2 \equiv 0 \pmod{p}$, and since $p$ is prime, $a \equiv 0 \pmod{p}$ as well. From (9), $d \equiv -c \equiv 0$, and from (8), $b \equiv -a \equiv 0$. So every solution has

$$
a \equiv b \equiv c \equiv d \equiv 0 \pmod{p} \tag{16}
$$

that is, all four are multiples of $p$. These are exactly the trivial solutions!

Hence, we have shown that there cannot be any nontrivial solutions to (1), (2) and (3).
