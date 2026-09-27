+++
title = "GRiddle's Puzzle: Past forward"
date = 2026-09-27
draft = false

[taxonomies]
categories = ["Puzzles", "Games"]
tags = ["blog"]

[extra]
lang = "en"
+++

## Question

The city council is building a museum of the city’s history: an $8 × 8$ block of $64$ galleries, one for each of the $64$ eras the city has lived through, numbered $1$ to $64$ from the oldest to the most recent. Every side shared by two galleries will be made into either a doorway or a wall. Visitors come in off the street into the entrance gallery, yellow in Figure 1. Six walls have already been built and five galleries have already had their exhibits installed, as shown in Figure 1.

A museum plan is a set of walls containing the six already built, together with a labelling of the galleries by the eras $1$ to $64$, one to each, extending the five already installed, such that from the entrance there is exactly one route to each gallery that never enters the same gallery twice, and along that route the era numbers increase. The cost of a museum plan is the expected number of doorways a visitor passes walking from the entrance to a gallery chosen uniformly at random among the $64$. An optimal wall plan is a set of walls occurring in a museum plan of least cost. How many optimal wall plans are there?

{{INSERT IMAGE HERE}}

## Solving

> Total number of optimal grid plans given the setup is $15 \cdot 2^{29} = 8053063680$

### Explanation

#### Number of walls and doorways

(Before I start the explanation, I should mention that I have chosen gallery 1 as the top-left cell. In case I don’t mention that again, it should be understood. Also, my cell representation will be (row, column) so $(i, j)$ means $i^{th}$ row $j^{th}$ column).

The problem says that the museum plan is such that from the entrance (top-left) there is exactly one route to each gallery that never enters the same gallery twice, and along that route the era numbers increase.

This implies that the number of doorways must exactly equal the number of cells in the grid. But since we’re already in the starting position we need to remove 1 from it. This is similar to having one continuous loop throughout the board, that’s exactly the number of doorways we’d need.

{{ figure(src="assets/image_1.png", alt="Image 1", caption="-") }}

Doing this for $N=8$, we get $63$ doorways. There exist exactly $2N(N-1)$ possible grid lines where walls can be placed. This is a standard formula. For $N=8$ that’s $112$ possible grid lines.

This implies, we need exactly $49$ walls, and it's non-negotiable. These two numbers are invariant to the problem.

We can see this for a few sample cases as well:

{{ figure(src="assets/image_2.png", alt="Image 2", caption="-") }}

#### Expected values and walls

Let’s start by assuming a plain $8 \times 8$ grid with no walls or numbers at all. We’ll write down the number of steps (which just means the number of doorways) it takes to reach a cell in that grid from the top-left (the starting gallery) following the shortest path in green.

{{ figure(src="assets/image_3.png", alt="Image 3", caption="-") }}

The expected value of the number of doorways it takes to reach any cell in this grid is 7 as:

$$
\frac{(1(2)+2(3)+3(4)+4(5)+5(6)+6(7)+7(8)+8(7)+9(6)+10(5)+11(4)+12(3)+13(2)+14)}{64} = 7
$$

Adding walls to this base grid will only increase the expected value in counts of 2 (that is, each cell will either be +2 or +4 or +6 and so on). The reason for that is simple:

- For a cell $(i, j)$, the shortest path to it comes from either $(i-1, j)$ or $(i, j-1)$ where the starting point is the top-left cell at $(0, 0)$. Thus, only a wall that blocks both of them can increase the shortest number of steps needed to reach the cell $(i, j)$.

- Once the two walls are setup, the shortest path must now go through $(i-1, j)$ ->  $(i-1, j+1)$ -> $(i, j+1)$ -> $(i, j)$ or $(i, j-1)$ -> $(i+1, j-1)$ -> $(i+1, j)$ -> $(i, j)$. That’s two more steps in the minimum.

- We’ll call this kind of a wall configuration as a “cover”. Specifically, a cover is a wall on cell $(i, j)$ that is placed above and to the left of it, that is, between $(i-1, j)$ -> $(i, j)$ and $(i, j-1)$ -> $(i, j)$.


{{ figure(src="assets/image_4.png", alt="Image 4", caption="-") }}

The effect of adding walls to the base grid can be quantified now, if the wall is a “cover” then we’ll see a change in the number of steps required to get there, else we won’t.

For example:

{{ figure(src="assets/image_5.png", alt="Image 5", caption="-") }}

I have added a few walls to the base grid and it's clear how the numbers have changed. I have highlighted a few of them in pink.

The new expected value after adding these specific set of walls is $7.1875$ which is exactly

$$
\frac{46}{64}+7= frac{\sum_{i} \Delta_{i}}{64}+7
$$

Here, $\Delta_{i}$ represents the deviations of the $i^{th}$ cell from the base case. To make this idea more explicit this is another grid with more walls and labelled deviations for all cells.

{{ figure(src="assets/image_6.png", alt="Image 6", caption="-") }}


This is the “delta map” which is counting the deviations for each cell for minimum distance from the starting point. The sum of deviations in this grid is $228$ and hence the expected value of steps (doorways) is $10.5625$. So, we can already note that with walls added, the expected value will increase.


#### Optimality with walls

So we understand that a cover increases the number of steps and we ideally want to avoid covers as much as possible. If we completely manage to avoid covers, then the expected value will turn out to be 7 (since, the delta map will only be +0 with no walls or numbers). If there already exist covers as in the problem given, then the lack of any MORE will mean the expected value will not budge from the current one. 

In order to see how this is possible, consider this diagram which considers the walls that have been provided by the question in brown.

{{ figure(src="assets/image_7.png", alt="Image 7", caption="-") }}

This shows the flow from the top-left corner to each cell such that the cell can be reached in the minimum possible steps. The diagram shows all such possible cases. Notice how they’re all headed to the right and down in the normal case, except near walls. This is again because we’re trying to minimize the distance from the top-left. 

The red arrows show that we cannot put up a wall in those transitions because that will definitely increase the number of steps to get to that cell. The pink arrows are neutral and can be walled, while the yellow arrows are special cases (inverted). 

The reason we can say that the optimal condition is achieved when we have walled a cell with two inputs is because there is a link between the delta map of a grid and its expected value! In the diagram above, we have tried to minimize or contain the damage from the walls w.r.t. the number of doorways each cell takes, and hence, we’ve optimized for the expected value.

Now for each cell that has more than or equal to 2 inputs, we can wall one of them, and only one of them at a time. If we count those cells (shown as shaded green ones)

{{ figure(src="assets/image_8.png", alt="Image 8", caption="-") }}

There’s exactly $43$ of them (It’s not a coincidence that $43$ = $49 - 6$). Therefore the number of ways we can wall these such that optimality is preserved (note that by selecting these cells, we have already said optimality will be preserved if we wall one of the two inputs), is $243$.

In general there are $\binom{112}{49}$ possible ways to add $49$ walls here, and this number is roughly $20$ orders of magnitude larger than $2^{43}$. We have already filtered out quite a lot by assuming the condition of optimality to be represented via the arrows. But we haven’t even considered the numbers there yet.

#### Optimality with Numbers and Walls

Before we make the arrow diagram, let me explain the new constraints that the numbers bring.

{{ figure(src="assets/image_9.png", alt="Image 9", caption="-") }}

Firstly, we notice that 64 already placed implies it CANNOT lead to any other number and hence the chain must end at it. This can be done in a few ways but we choose the one I have represented with the purple because that’s the only one that will not create a cover. If a cover is created, then the number of steps to reach 64 will increase by 2 (at minimum), and hence the layout will NOT be optimal.

Now we also have 62 and we know that 62 can only lead to 63 and 63 cannot possibly lead to 64 since they are too far apart. So the chain must also end at 63. There are 4 ways to place 63 and end the chain and we’ll choose the 4th one.

- The reason for this is again optimality. Choosing 1 will completely block off 26, so that is definitely wrong. Choosing the 2nd one (top right), will FURTHER increase the number of steps to the shaded green region by +2 which is not optimal.
- Between 3 (bottom left) and the last one, consider their delta maps:

{{ figure(src="assets/image_10.png", alt="Image 10", caption="-") }}

- Sum of deviations for 1: $78$ (minimum expected doorways = $8.21875$)
- Sum of deviations for 2: $68$ (minimum expected doorways = $8.0625$)

- Since expected doorways depend on the sum of deviations, we’ll opt for the second one for optimality.


For the chosen grid, note how the $62$ can ONLY feed to $63$ (that is, $62 -> 63$). For optimality, only the cell from the TOP of $62$ can feed it (because if not, then reaching $62$ would require more doorways). It’s effectively a box around $62$ as well, which will be clear in the image below.

{{ figure(src="assets/image_11.png", alt="Image 11", caption="-") }}

Let’s also reason about the 9 there because that will give us some more constraints.

We need 5, 6 and 7 to be exactly as shown in the image below. They cannot move from there because otherwise 9 will never be satisfied according to the rules of the museum plan. Since we know that 16 cannot feed 6 (when trying to reach 6 with least doorways) according to the game rules, and 6 feeding 16 is sub-optimal, this implies a wall in between 6 and 16.

- But note that cell $(2,5)$ CANNOT hold an 8. If it does hold as 8 as it's shown, then the minimum number of steps to reach $(1,5)$ increases from 6 to 8 as we cannot go through 16 anymore. This is sub-optimal. Hence the 8 is also pretty much fixed in place.

Let me draw the arrow diagram for the chosen grid with numbers and walls (including inferred):

{{ figure(src="assets/image_12.png", alt="Image 12", caption="-") }}

See the box around 62. No such box exists for 16, 9 or 26 because they only have 2 possible inputs around them and both paths take up the same number of doorways. 

This is a very specially constructed grid so I’ll take some time to walk through this:


- 16 has two inputs both sitting 4 doors away from the starting position. That’s through $(2,3)$ and $(1,4)$.
- 9 has special attention as we saw before. $(2,5)$ cannot feed into 9 due to sub-optimality and for the same reason 9 cannot feed $(2,5)$.
- Similarly, $(2,5)$ feeding to $(1,5)$ is the only optimal choice, and $(1,6)$ cannot be doing that.
- Feeding $(1,6)$ with 9 is sub-optimal because 9 is fed through $(3,6)$ only and not $(2,5)$ as discussed before hence, the cell $(1,6)$ will get a +2 if done through 9.
- The cell at $(3,6)$ CANNOT receive anything from 9. It must feed it. So, it has only one input source and 3 outputs, it holds the fixed 8.
- Cells $(4,2)$, $(5,2)$ and $(6,2)$ are all single input channels due to the wall introduced by 64. To get to $(4,1)$ the most optimal way is to feed it from $(4,2)$ and hence the arrow that used to be pointing right (see previous diagram) is now pointing left. The same goes for the others.
- 62 has a box around it. 62 feeds 63, and it takes in an input. If it takes an input from $(7,5)$ that's suboptimal compared to taking it from $(6,4)$ due to a +2 in doorways. Similarly taking an input from $(8,4)$ is a +4 compared to $(6,4)$. So, in effect it has a wall there, since the numbers in its neighbourhood WILL be smaller and hence a potential path to 62 must be blocked from these sides.
- 26 cannot feed $(7,2)$. Because that’s again suboptimal compared to feeding $(7,2)$ with $(8,2)$ as the former adds a +2. 
- Cell $(3,7)$ is another splitting point. It must feed $(2,7)$ and not TAKE from it. Another thing to note here is that optimal conditions imply we must always go down in the normal case (see the previous arrow diagram without numbers). For the entire column 7 and 8 (and others too), we’re always trying to go down.
- Cell $(3,8)$ feeds up and down both. This is pretty straightforward since $(3,7)$ -> $(2,7)$ -> $(2,8)$ is the same as $(3,7)$ -> $(3,8)$ -> $(2,8)$ in terms of the number of doorways. The same argument holds for $(1,8)$.

Now counting the number of shaded boxes and the numbers (given or inferred) that have more than 1 possible inputs, we get $33$ (30 shaded green along with 16, 5 and 26) of them. So the number of ways of putting walls around them is $2^{33}$.

**Now the case for 26.**

The best case number depth for 26 is 16 and there are only 25 numbers which can feed into it. Out of those, we have already used up 1-9 for 9 and the number 16 is also already used. So that leaves us with 15 numbers. That’s an exact number of numbers we need to get to 26! 

This means we will have to reuse the 5,6,7 that we planted for reaching 9 and get to 26. 

To put pictures to this, this diagram valid is works with 0 margin for error (I am still following the same lines I drew in the diagram above)


{{ figure(src="assets/image_13.png", alt="Image 13", caption="-") }}

The green dotted path goes to 26, pink path to 9 and yellow to 16. This entirely uses 1-26 numbers so no margin for error. 

But if we look at the below diagram:

{{ figure(src="assets/image_14.png", alt="Image 14", caption="-") }}

This time we’ve split off for 26 from $(2,2)$ itself which is a PERFECTLY valid move according to the arrow diagram I showed above but in this case will break the margins we were playing with! So, this is wrong.

So, there are just these 4 sets of precious conditions that need to be true for us to never reach 26. Those are:

- Reach 16 from $(1,4)$ so that no one can use those numbers. By no one I mean 9 and 26.
- Reach 5 from $(2,3)$ and go to 9
- Reach $(2,3)$ from $(2,2)$ and $(2,2)$ from $(2,1)$ only, ensuring that we don’t use any of the 16-route numbers.
- Start for 26 from $(2,2)$ -> (3,2)

If all 4 of these happen, then we’re cooked. So,

- Reaching 16 from $(1,4)$ implies we remove a binary choice from 16.
- Reaching 5 from $(2,3)$ and not $(3,2)$ removes another binary choice.
- We remove the binary choice from $(2,2)$ and $(3,2)$ as well.
- This doesn’t change anything, since $(3,2)$ had only one input anyway.

So basically, the arrow diagram now looks like this:

{{ figure(src="assets/image_15.png", alt="Image 15", caption="-") }}

That’s a total of $2^{29}$ cases! ($28$ green shaded ones and 26)

This means out of the $2^{33}$ possible wall choices for optimality, there are $2^{29}$ choices that will be optimal but WILL NEVER WORK as 26 will never be reached. This means the real VALID choices, are only $2^{33}-2^{29}=2^{29}(16-1)=15 \cdot 2^{29}$.

And now we’re done. The answer is $15 \cdot 2^{29}$.

### Formulas

1. The number of grid individual grid lines inside an $N \times N$ grid is given by

$$
L=2N(N-1)
$$

2. The number of walls (which is invariant) for a given $N \times N$ grid is given by

$$
W=(N-1)^{2}
$$

	Note: This is derived based on the questions constraints

3. The number of doorways (which is invariant) for a given N N grid is given by

$$
D=N^{2}-1
$$

4. The expected value (mean) of the number of doorways for reaching a square in the grid is given by
	
$$
\hat{E}= \frac{\sum_{i} \Delta_i}{N^2} + N - 1
$$

Where $\Delta_i$ is the deviation as explained above

5. Number of possible placements of walls such that $\Delta_i = 0 \forall i$ is given by

$$
2^{(N-1)^2}
$$

6. Number of possible placements of walls such that $\Delta_i = 0 \forall i$; with $m$ walls already added is given by

$$
2^{(N-1)^{2}-m}
$$

---
