+++
title = "Formula reduction for Polyominoes"
date = 2026-08-23
draft = false

[taxonomies]
categories = ["Math", "Algebra"]
tags = ["blog"]

[extra]
lang = "en"
math = true
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

In the last [blog](https://purge12.github.io/blog/shape_algebra_1/), I discussed about some fundamental rules for the shape algebra. I closed with a remark on how we're able to not construct shapes like these:

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/1"></i><i class="g" style="grid-area:2/1"></i><i class="g" style="grid-area:3/1"></i><i class="g" style="grid-area:1/2"></i><i class="g" style="grid-area:3/2"></i><i class="g" style="grid-area:1/3"></i><i class="g" style="grid-area:1/4"></i><i class="g" style="grid-area:3/4"></i><i class="g" style="grid-area:1/5"></i><i class="g" style="grid-area:2/5"></i><i class="g" style="grid-area:3/5"></i></span></div>

In this blog, I'll explore a way of solving this first, then I'll write some generalized notation so that we can talk about the length of the formula as a "feature" of the algebra and ponder over it.

## Introducing Subtraction

That's exactly 
