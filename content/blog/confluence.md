+++
title = "Algebra for Polyominoes"
date = 2026-08-20
draft = false

[taxonomies]
categories = ["Math", "Algebra"]
tags = ["blog"]

[extra]
lang = "en"
math = true
banner = "assets/banners/confluence.jpg"
+++

<style>
.poly {
  --cell: 1.2em;
  --poly-line: #3c4043;
  --poly-fill: #ffffff;
  --poly-new: #f2ce3c;
  --poly-gray: #d5d7da;
  --poly-red: #f0908a;
  --poly-green: #8ecf96;
  --poly-cyan: #86ccd6;
  display: inline-grid;
  grid-auto-columns: var(--cell);
  grid-auto-rows: var(--cell);
  vertical-align: middle;
  line-height: 0;
}
.poly i {
  display: block;
  border: 1px solid var(--poly-line);
  background: var(--poly-fill);
  margin: 0 -1px -1px 0;
}
.poly i.new { background: var(--poly-new); }
.poly i.g   { background: var(--poly-gray); }
.poly i.r   { background: var(--poly-red); }
.poly i.gr  { background: var(--poly-green); }
.poly i.cy  { background: var(--poly-cyan); }
.poly.sm    { --cell: 0.85em; vertical-align: -0.4em; }

.dark .poly {
  --poly-line: #8b9099;
  --poly-fill: #26282c;
  --poly-new: #b8952a;
  --poly-gray: #4b4f55;
  --poly-red: #9c5450;
  --poly-green: #4f7f57;
  --poly-cyan: #47818b;
}

.polyeq {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  margin: 1.7em 0;
}
.polyeq .op  { font-size: 1.1em; opacity: 0.7; padding: 0 0.1em; }
.polyeq .gap { width: 1.8em; }
.polyeq .lbl { font-size: 1em; white-space: nowrap; }

.latch { display: inline-flex; align-items: center; gap: 0.15em; }
.latch .pr {
  display: inline-block;
  font-size: 1.5em;
  font-weight: 300;
  line-height: 1;
  opacity: 0.55;
  transform: scaleY(1.45);
}
.latch .lt { font-family: KaTeX_Math, Georgia, serif; font-style: italic; font-size: 0.85em; opacity: 0.85; align-self: flex-end; margin-bottom: 0.35em; }

.slot {
  border: 1px dashed currentColor;
  background: rgba(128, 128, 128, 0.06);
  border-radius: 3px;
  padding: 1.1em 1.2em;
  margin: 1.6em 0;
  text-align: center;
  font-style: italic;
  font-size: 0.94em;
  opacity: 0.65;
}

.tetro-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 0.5em 2.4em;
  margin: 1.8em 0;
}
.tetro { display: flex; align-items: center; gap: 1em; min-height: 5.2em; }
.tetro-pic { flex: 0 0 5.2em; line-height: 0; }
.tetro-eq { flex: 1 1 auto; min-width: 0; overflow-x: auto; overflow-y: hidden; }

@media (max-width: 400px) {
  .tetro-grid { grid-template-columns: 1fr; }
  .tetro-eq { font-size: 0.9em; }
}
</style>

## Introduction

Recently I have been thinking about shapes. While I would love to talk about my motivation for doing all this, I don't feel like doing it right now because then I might forget the more important things.

Turns out that drawing squares and connecting them together has a name. They are called "polyominoes" which is very weirdly spelled. I didn't know that when I started out anyway. I had a goal which I will disclose later but the point was to see how far I can come in this field.

And I decided to tackle it by building each polyomino one block a piece, starting from row or column primitives. This was a whole algebra lesson and a pretty fun puzzle tbh, since I was trying to see where my own rules fall short and adding new ones and so on.

## Objects

So we have just two primitives from which we're going to build all others. These are **strips** and **units**.

**Strips.**

$A_R^{(j)}$ is a horizontal strip of $j$ cells; $A_C^{(j)}$ is a vertical strip of $j$ cells. These are the only shapes that exist before any addition happens. These are our primitives.

<div class="polyeq"><span class="lbl">$A_R^{(4)} =$</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i></span><span class="gap"></span><span class="lbl">$A_C^{(4)} =$</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:4/1"></i></span></div>

A strip of length one is a single cell, so $A_R^{(1)} = A_C^{(1)}$.

**Units.**

$1_R$ and $1_C$ are single cells carrying a *direction tag*. The tag says how the cell approaches the shape, not what it looks like.

A $1_R$ and a $1_C$ are the same square but they are attached to the diagram differently which we'll discuss below.

**Compound shapes.**

Anything built by adding units to a strip. This is the whole deal

## The latch

This is an interesting concept because I am debating whether to call it a push button instead. The idea is simply that we need to have some mechanism to say whether a cell is to be added to a row or a column (also, which one?).

This latch is like an internal state of a turning machine, if a turning machine had only 2 internal states. Latch can be a "R" for row or a "C" for column.

It's a latch for the "type" but NOT for the "selection".

**Type.**

Whether the target is a row or a column.

**Selection.**

*Which* row or column.

The bracket subscript $(\\,\cdot\\,)_X$ is how I am denoting the latching mechanism and it really is a **push button**. Pressing it does two things at once: it sets the type to $X$, and it selects the line of type $X$ **holding the most cells**, counted at the moment the bracket closes.

Now this is important because this is about as far as I go right now to select a row or a column, just selecting the max cells one.

That **selection** lasts for the next addition ONLY. Afterwards the type is still $X$, but the selection has fallen back to the **default**, that is, the rightmost column, or the topmost row.

To target the most populous line again, press the button again.

There are a few more rules on this:

- $A_X^{(j)}$ sets the type to $X$ when it appears.
- If more than one row or column have max cells, then the winner is the **rightmost** column, or the **topmost** row.
- $1_X$ never pushes. Its subscript is a direction tag.

So in $\left(\\,\cdot\\,\right)_C + 1_C + 1_C$ the two additions do not behave the same. The $\left(\\,\cdot\\,\right)_C$ latches onto the most populous column. So, the first $+1_C$ happens for the most populous column. The next $+1_C$ however, has no memory of the "most populated", it only know it must go to a column. And it indeed only goes to the default column (rightmost).

We'll see many examples of these in a while.

There is no syntax for naming a particular row or column, and none is needed. Any line can be reached by mirroring the shape (described in section 5) so that the line becomes the rightmost column or topmost row, and then adding by default.

## Addition

Addition attaches **one unit cell** to the shape. The left operand is a shape, the right operand is always a single tagged unit. There is no shape-plus-shape addition because I thought that would make things just more complicated, cause we'll have to end up defining which edges interact, what happens when there is space between them and so on.

Let's now talk about how a unit cells attaches to the shape. Note that we already established it should attach to the latched row or column, and we therefore have all 4 possiblities (2! (Row latched | Column latched) * 2! (row oriented unit | column oriented unit))

- $1_R$ **floats** in from the right, moving leftwards, and comes to rest against the first cell it meets (on the latched line)
- $1_C$ **falls** from above, moving downwards, and comes to rest on top of the first cell it meets (on the latched line).

The latch decides *which* line it travels along:

| latch | unit | travels along | lands |
|---|---|---|---|
| row $\rho$ | $1_R$ | row $\rho$ | right of $\rho$'s rightmost cell |
| row $\rho$ | $1_C$ | the column of $\rho$'s rightmost cell | above that column's topmost cell |
| column $\gamma$ | $1_R$ | the row of $\gamma$'s topmost cell | right of that row's rightmost cell |
| column $\gamma$ | $1_C$ | column $\gamma$ | above $\gamma$'s topmost cell |

So a $1_R$ always finishes on the right-hand side of the shape and a $1_C$ always on top. Growth is rightwards and upwards. To get the other two directions, we mirror and not use a different rule.

Note: The third row is pretty cool. It says that we can float in from the right and attach onto a column. Which makes sense if you think about it visually too.

### Latched column, $+\\,1_R$

The unit reaches the top of the chosen column from the side (the diagrams may not depect the position of "flowing in" perfectly).

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:1/2"></i></span></div>

### Latched column on a compound shape

Take

<div class="polyeq"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span></div>

Columns 2 and 3 both hold two cells, which means latching a column here is tied. According to the rules, the tie goes to the rightmost so the latch is column 3.

Adding $1_R$, the unit floats in along column 3's topmost row (always the topmost row for a chosen column) and attaches next to its rightmost cell:

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span><span class="pr">)</span><sub class="lt">C</sub></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i class="new" style="grid-area:1/4"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span></div>

Adding $1_C$ instead, the unit falls down (like gravity) column 3 and rests on top of it:

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span><span class="pr">)</span><sub class="lt">C</sub></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i class="new" style="grid-area:1/3"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i></span></div>

### Latched row, $+\\,1_R$

With the latch on a row, the unit extends that row rightwards.

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i><i class="new" style="grid-area:1/5"></i></span></div>

Here the top row holds four cells and the second row three, so the latch takes the top row:

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span><span class="pr">)</span><sub class="lt">R</sub></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i class="new" style="grid-area:1/5"></i></span></div>

### Latched row, $+\\,1_C$

If we add $1_C$ to a system where the TYPE is row and it has no memory of the largest group:

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i style="grid-area:2/4"></i><i class="new" style="grid-area:1/4"></i></span></div>

If we enforce max row selection and then add $1_C$:

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i style="grid-area:2/4"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i></span><span class="pr">)</span><sub class="lt">R</sub></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i style="grid-area:2/4"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i><i class="new" style="grid-area:1/4"></i></span></div>

### Further addition examples

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i></span><span class="pr">)</span><sub class="lt">R</sub></span><span class="op">+</span><span class="poly"><i class="new" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i><i class="new" style="grid-area:1/3"></i></span><span class="op">+</span><span class="poly"><i class="r" style="grid-area:1/1"></i></span><span class="op">=</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i><i class="r" style="grid-area:1/4"></i><i class="new" style="grid-area:1/3"></i></span></div>

I'll add more later. Feeling sleepy now.

## Mirrors

$(\\,\cdot\\,)^{M}_X$ **replaces** a shape with its reflection. We have two kinds of reflections, along the row or along the column.

NOTE: It's important to realize that this means flips are mathematically impossible to replicate. Thus, if during construction we ever need to flip from a diagonal or cross diagonal axis, the construction needs to change.

The mirror tag at the bottom, does **not** latch. It's just directionality, like $1_R$. It doesn't even change the latch momentarily or anything.

- $(\\,\cdot\\,)^{M}_R \implies$ mirror laid horizontally against the **bottommost row**. The shape flips top-to-bottom.
- $(\\,\cdot\\,)^{M}_C \implies$ mirror laid vertically against the **rightmost column**. The shape flips left-to-right.

Take an L, three cells down a column and three across the bottom row:

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i></span></div>

A column mirror stands the mirror on the right of the shape, so column 1 swaps with column 3 and the stem moves to the other side:

<div class="polyeq"><span class="latch"><span class="pr">(</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i><i style="grid-area:3/3"></i></span><span class="pr">)</span><sup class="lt" style="align-self:flex-start;margin:0.3em 0 0">M</sup><sub class="lt">C</sub></span><span class="op">=</span><span class="poly"><i class="new" style="grid-area:1/3"></i><i class="new" style="grid-area:2/3"></i><i class="new" style="grid-area:3/1"></i><i class="new" style="grid-area:3/2"></i><i class="new" style="grid-area:3/3"></i></span></div>

Rows are untouched, the bottom row stays where it is, and the shape now points right.

## Pinning with P

We also have a Pin (`P`) which can be used as $(\\,\cdot\\,)_P$. This pins the shape whenever called so all top rows and columns are referenced from the pinned shape.

The rule splits into two halves at this point:

1. Selection (which row, which column) counts only the cells inside P.
2. Landing (where the unit actually comes to rest) still uses the whole figure.

Pinning is for the reference only. It allows us to specify which figure's row or column are we talking about.

A few more rules:

1. It only changes what the selection is allowed to look at.
2. Pinning again re-pins to whatever the shape is at that moment. You can pin as many times as you like.
3. The pin travels with mirrors. Mirror the shape and the pinned cells mirror along with it.
4. Before any pin, the scope is the whole shape.

yes, scope is a better word for this. It scopes the references to a specific figure.

This shape cannot be built without P:

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/3"></i><i class="g" style="grid-area:2/2"></i><i class="g" style="grid-area:2/3"></i><i class="g" style="grid-area:2/4"></i><i class="g" style="grid-area:3/1"></i><i class="g" style="grid-area:3/2"></i><i class="g" style="grid-area:3/3"></i><i class="g" style="grid-area:4/2"></i></span></div>

This pattern has a peculiarity that at some point we'll have to add an element to the middle of the figure, so our topmost and bottommost terminology fails us here.

With P it comes out like this:

$$
\left(\left(\left(\left(\left(\left(\left(\left(A_C^{(2)}+1_R\right)^M\right)_C+1_R\right)_P+1_C\right)_R+1_R\right)^M\right)^M_C+1_C\right)+1_R\right)^M
$$

To illustrate that better:

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i class="r" style="grid-area:1/1"></i><i class="r" style="grid-area:1/2"></i><i class="r" style="grid-area:2/1"></i><i class="r" style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i class="new" style="grid-area:1/2"></i><i class="r" style="grid-area:2/1"></i><i class="r" style="grid-area:2/2"></i><i class="r" style="grid-area:3/1"></i><i class="r" style="grid-area:3/2"></i></span></div> <div class="polyeq"><span class="poly"><i style="grid-area:1/2"></i><i class="r" style="grid-area:2/1"></i><i class="r" style="grid-area:2/2"></i><i class="new" style="grid-area:2/3"></i><i class="r" style="grid-area:3/1"></i><i class="r" style="grid-area:3/2"></i></span><span class="op">→</span><span class="poly"><i class="r" style="grid-area:1/1"></i><i class="r" style="grid-area:1/2"></i><i class="r" style="grid-area:2/1"></i><i class="r" style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i style="grid-area:3/2"></i></span><span class="op">→</span><span class="poly"><i class="r" style="grid-area:1/2"></i><i class="r" style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i class="r" style="grid-area:2/2"></i><i class="r" style="grid-area:2/3"></i><i style="grid-area:3/2"></i></span><span class="op">→</span><span class="poly"><i class="new" style="grid-area:1/3"></i><i class="r" style="grid-area:2/2"></i><i class="r" style="grid-area:2/3"></i><i style="grid-area:3/1"></i><i class="r" style="grid-area:3/2"></i><i class="r" style="grid-area:3/3"></i><i style="grid-area:4/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/3"></i><i class="r" style="grid-area:2/2"></i><i class="r" style="grid-area:2/3"></i><i class="new" style="grid-area:2/4"></i><i style="grid-area:3/1"></i><i class="r" style="grid-area:3/2"></i><i class="r" style="grid-area:3/3"></i><i style="grid-area:4/2"></i></span></div>

Explanation:

1. Start from $A_C^{(2)}$.
2. Add a row block. It goes to the topmost row.
3. Mirror top-to-bottom.
4. $()_C$ selects the largest column, the left one with 2 blocks. Latch is now $C$.
5. Add a row block. That completes the red square.
6. $()_P$ pins the square.
7. Add a column block. The latch type is still $C$ and the selection has fallen back to default, so it goes to the rightmost column.
8. $()_R$ now selects the largest row **among the pinned cells only**. Both pinned rows hold 2, so the tie goes topmost. Note that the block from step 7 doesn't contribute a row at all, because it isn't pinned. Then add a row block.
9. Mirror top-to-bottom.
10. Mirror left-to-right.
11. Latch is $R$, so we're on the topmost pinned row. Add a column block.
12. Same row, add a row block.

A final $(\\,\cdot\\,)^{M}$ picks which of the two enantiomers we'll end up with.


## Worked examples

<div class="slot">maybe I can add a few here</div>

### The plus-pentomino

$$
\left(\left(\left(A_R^{(2)} + 1_C\right)^{M}_R\right)_R + 1_R\right)_C + 1_C
$$

This is the smallest shape where the push button changes the outcome.

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i></span><span class="op">→</span><span class="poly"><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i class="new" style="grid-area:1/3"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i><i style="grid-area:3/2"></i></span></div>

The steps are: add $1_C$ above the row; mirror top-to-bottom; select most populous row $()_R$ and extend the top row; then select most populous column $()_C$ and add $1_C$.

At that point the shape is <span class="poly sm"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/2"></i></span>, whose columns hold one, two and one cells. We select the *most populous* column, that is the middle one, and the box lands on top of it.

### The staircase

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/1"></i><i class="g" style="grid-area:1/2"></i><i class="g" style="grid-area:2/2"></i><i class="g" style="grid-area:2/3"></i><i class="g" style="grid-area:3/3"></i></span></div>

$$
\left(\left(\left(A_R^{(2)} + 1_C\right)_C + 1_R\right) + 1_C\right)^M
$$

I deliberately made this to use the dynamics of the push button. The first latch is on $R$, then we explicitly latch on $C$. This latch selects the most populous column and we add $1_R$ to it. Then the latch type is still $C$ but we move selection to default which is rightmost row. And we add $1_C$ to that to finish the inverted staircase. Then its a mirror image.

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i></span><span class="op">→</span><span class="poly"><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i class="new" style="grid-area:1/2"></i><i class="r" style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="op">→</span><span class="poly"><i class="gr" style="grid-area:1/3"></i><i class="new" style="grid-area:2/2"></i><i class="r" style="grid-area:2/3"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i class="new" style="grid-area:2/2"></i><i class="r" style="grid-area:2/3"></i><i class="gr" style="grid-area:3/3"></i></span></div>

### The $3\times3$ ring

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/1"></i><i class="g" style="grid-area:1/2"></i><i class="g" style="grid-area:1/3"></i><i class="g" style="grid-area:2/1"></i><i class="g" style="grid-area:2/3"></i><i class="g" style="grid-area:3/1"></i><i class="g" style="grid-area:3/2"></i><i class="g" style="grid-area:3/3"></i></span></div>

This is just a 3x3 grid with a missing center square. This formula will construct it:

$$
\left(\left(\left(\left(\left(A_C^{(3)} + 1_R\right) + 1_R\right)^M\right)_C + 1_R\right)_R+1_C\right)+1_C
$$

Let me show you the intermediate steps here:

<div class="polyeq"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:1/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:1/2"></i><i class="new" style="grid-area:1/3"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:3/2"></i><i class="new" style="grid-area:3/3"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:3/2"></i><i class="new" style="grid-area:3/3"></i><i class="r" style="grid-area:1/2"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:3/2"></i><i class="new" style="grid-area:3/3"></i><i class="r" style="grid-area:1/2"></i><i class="gr" style="grid-area:2/3"></i></span><span class="op">→</span><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i class="new" style="grid-area:3/2"></i><i class="new" style="grid-area:3/3"></i><i class="r" style="grid-area:1/2"></i><i class="gr" style="grid-area:2/3"></i><i class="cy" style="grid-area:1/3"></i></span></div>

That's kinda beautiful, ngl.

## The nineteen tetrominoes for N=4

Every shape of four cells, counted with all orientations distinct. A formula for each:

<div class="tetro-grid"><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:1/4"></i></span></div><div class="tetro-eq">$A_R^{(4)}$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:4/1"></i></span></div><div class="tetro-eq">$A_C^{(4)}$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span></div><div class="tetro-eq">$\left(\left(A_R^{(2)} + 1_R\right)^M\right)_C+1_R$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/2"></i></span></div><div class="tetro-eq">$\left(A_R^{(2)}+1_C\right)^M+1_R$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:3/2"></i></span></div><div class="tetro-eq">$\left(\left(A_C^{(2)}+1_R\right)_C+1_C\right)^M_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span></div><div class="tetro-eq">$\left(\left(A_R^{(2)}+1_C\right)^M+1_R\right)^M$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:3/1"></i></span></div><div class="tetro-eq">$\left(A_C^{(2)}+1_R\right)_C+1_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span></div><div class="tetro-eq">$\left(A_R^{(3)}+1_C\right)^M_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i></span></div><div class="tetro-eq">$A_C^{(3)}+1_R$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/3"></i></span></div><div class="tetro-eq">$\left(A_R^{(3)}+1_C\right)^M$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i></span></div><div class="tetro-eq">$\left(\left(A_C^{(3)}+1_R\right)^M\right)^M_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:3/1"></i><i style="grid-area:3/2"></i></span></div><div class="tetro-eq">$\left(A_C^{(3)}+1_R\right)^M$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i></span></div><div class="tetro-eq">$\left(\left(A_R^{(3)}+1_C\right)^M\right)^M_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i><i style="grid-area:3/2"></i></span></div><div class="tetro-eq">$\left(A_C^{(3)}+1_R\right)^M_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span></div><div class="tetro-eq">$A_R^{(3)}+1_C$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span></div><div class="tetro-eq">$\left(A_R^{(2)} + 1_C\right)_C+1_R$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:3/2"></i></span></div><div class="tetro-eq">$\left(\left(A_C^{(2)}+1_R\right)_R+1_C\right)^M$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i><i style="grid-area:2/2"></i><i style="grid-area:2/3"></i></span></div><div class="tetro-eq">$\left(\left(A_R^{(2)} + 1_C\right)_C+1_R\right)^M$</div></div><div class="tetro"><div class="tetro-pic"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i><i style="grid-area:3/1"></i></span></div><div class="tetro-eq">$\left(A_C^{(2)}+1_R\right)_R+1_C$</div></div></div>

## Conclusion

I'll settle some more questions and new ideas in the next post as this is already getting too long. Do note that so far, with the rules we have, we can make all shapes upto N=10. The only problem with higher shapes (N=11 gives 4 shapes which we cannot make) is interior reachability.

For example, this the shape we just cannot reach for N=11 (this and its mirror pair and 90 degree rotated versions).

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/1"></i><i class="g" style="grid-area:2/1"></i><i class="g" style="grid-area:3/1"></i><i class="g" style="grid-area:1/2"></i><i class="g" style="grid-area:3/2"></i><i class="g" style="grid-area:1/3"></i><i class="g" style="grid-area:1/4"></i><i class="g" style="grid-area:3/4"></i><i class="g" style="grid-area:1/5"></i><i class="g" style="grid-area:2/5"></i><i class="g" style="grid-area:3/5"></i></span></div>

I will address this in the next blog and will solve it. I'll also talk about formula sizes and define some basic rules for reduction and maybe think about counting.

Link: [part 2](https://purge12.github.io/blog/shape-algebra-2/)
