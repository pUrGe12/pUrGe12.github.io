+++
title = "Hidden quadratic Diophantine equtions (Pells equation)"
date = 2026-09-21
draft = false

[taxonomies]
categories = ["Puzzles", "Math"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

So, I was tackling problem 100 and it quickly taught me a lot about floating point arithmetic and best practices on puzzle solving. The question itself is not that hard to state but realizing its true state is the ball game, which I couldn't do at first and had to see solutions.

But I still want to write it down because it ensures that I truly understand it now and I can spot Pell's equations in the future (Now that I know [how to solve](https://purge12.github.io/blog/project-euler-66/) it)!

## Question

A box contains T number of balls, B are blue and R are red. Find the smallest value of T greater than $10^12$ for which the probability of drawing two blue balls is exactly $\frac{1}{2}$.

## Solution

So, its not too hard to see that the variables follow exactly this equation:

$$
\left(\frac{B}{T}\right)\left(\frac{B-1}{T-1}\right) = \frac{1}{2}
$$

With this, we can find the value of $B$ exactly with the quadratic formula as:

$$
B = \frac{1+\sqrt{1+2(T^2-T)}}{2}
$$

So, now all we have to do is, pick $T \gt 10^12$ and enumerate all values until we hit an integer for $B$.

And that is what I did:

```py
import math

for i in range(10**12, 10**13):
  x = (1 + math.sqrt(1 + 2*(i**2-i)))/2
  if x-math.floor(x) == 0.0:
    print(f"Found an integer x: {x} for total discs: {i}")
```

And this gave me a lot of false positives. Here's why this is wrong:

1. Floating point comparisions are tricky in python and doing `x-math.floor(x) == 0.0` is the worst thing I could've done. Its always better to just compute the `isqrt` instead of `sqrt` if integers are what we need.
2. This will take forever to complete!

Lesson to be learnt here is that, whenever your code seems to run forever, its probably either a less effieicent algorithm or more often, less effiecient math.

In this case, it was less efficient math. Because if we look at the equation written before more carefully, we'll observe this:

$$
2B(B+1) = T(T-1)
\text{let} a = 2B-1; b = 2T-1
\implies 2(a+1)\left(\frac{a-1}{2}\right) = \left(\frac{b+1}{2}\right)\left(\frac{b-1}{2}\right)
\implies b^2 - 2a^2 = -1
$$

This is Pell's equation! And we know how to solve Pell's equation, using continued fractions on $\sqrt{D}$ in this case, $\sqrt{2}$.

The entire reason the first approach failed is because an exact answer for floats is a painful procedure and even if I had the right thing by doing:

```py
import math

for i in range(10**12, 10**13):
  D = math.isqrt(1 + 2*(i**2-i))
  if D * D == 1 + 2*(i**2 - i):
    # Perfect square
    x = (1 + D)/2
    print(f"Found an integer x: {x} for total discs: {i}")
    break
```

Then we'd get the right answer with no false positives, but it'd take a long time. I benchmarked it, its roughly 2M iterations every second, so to reach the ACTUAL solution (which I know by solving the Pell's equation), it'd take roughly 9-10 hours. I can speed this up by like 22 times by assigning it more cores. 

There actually is another very interesting optimization we can do. Going with the maxim of trading space for speed, we can create a lookup table for `squares (mod m)` and instantly reduce the number of `D * D` checks we have to make! This is similar to saying that we can take (mod 10) and that gives us the last digit, and if a last digit is 7, then its instantly not a perfect square! So, we can just extend that idea such that we can rule out more numbers!

Note that passing doesn't mean its a perfect square. But failing means it def. isn't.

So, it took roughly 33 minutes to find the solution! Which is wayyyy worse than continuted fractions of $\sqrt{2}$ but I digress.

## Problem solving tactics

Stuff this problem specifically taught me and hence made it to the post:

1. If your code iterates in trillions, you're probably not thinking all the way through. (This is ONLY because we know the problem has an existing solution. If its an open problem, then its an entirely different ball-game and this is not valid).

2. Think reduction to a known problem. Always.

3. Never compute floats if what you want is to compare integers.