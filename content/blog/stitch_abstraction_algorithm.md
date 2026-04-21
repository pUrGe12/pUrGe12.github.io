+++
title = "Understanding the Stitch Algorithm for abstractions"
date = 2026-04-03
draft = false

[taxonomies]
categories = ["abstractions", "program-synthesis"]
tags = ["ML"]

[extra]
lang = "en"
+++

This is the paper published by MIT on something called the **Top-Down synthesis for Library Learning**. It's another technique for generating abstractions from a set of primitives into a library for future use, similar to what `wake-sleep` cycles were doing for DreamCoder (see [this post](https://purge12.github.io/blog/dreamcoder/)).

To quote the authors:

>  We present an implementation of the approach in a tool called Stitch and evaluate it against the state-of-the-art deductive library learning algorithm from DreamCoder. Our evaluation shows that Stitch is 3-4 orders of magnitude faster and uses 2 orders of magnitude less memory while maintaining comparable or better library quality (as measured by compressivity).

## Introduction

The idea is very simple, faced with the task of writing a program from low-level primitives, multiple-times, you would want to create parameterized abstractions. 

> One popular approach to library learning is to search for common tree fragments
across a corpus of programs, which can be introduced as new abstractions

Some authors have found very good algorithms that gave good results but are not feasible to scale for large datasets of longer and deeper programs. All these `deductive` approaches to library learning will inevitably lead to higher memory and compute requirements (so the author claims, I don't understand why though.)

- Here the authors say that they don't take the deductive approach of "refactoring the corpus with rewrite rules". Instead, they "directly synthesize abstractions".
- They call this **corpus-guided top-down synthesis**.

Finally we come to what stitch is, I genuinely didn't know that!

>  Stitch, a corpus-guided top-down library learning tool written in Rust

And boom: https://github.com/mlb2251/stitch

The code!

- Now the authors are saying that stitch can do in seconds or single-digit minutes, what is beyond the compute of the `DreamCoder` algorithm! That's really insane

## How it works

The authors are awesome! They are giving an example. Let's work through that. Suppose that the Stitch algorithm has been given these corpus of programs and the goal is to learn a single abstraction.

```
λx. + 3 (* (+ 2 4) 2)
λxs. map (λx. + 3 (* 4 (+ 3 x))) xs
λx. * 2 (+ 3 (* x (+ 2 1)))
```

Defining a good abstraction, the authors write that a good abstraction is one that **minimizes the size of the corpus when re-written with the abstraction**. We'll talk about `compression` as a utility function. Let's talk a little bit about that now.

In compression we seek to minimize some measure of the size, or more generally the cost, of a corpus of programs after rewriting them with a new abstraction.

```
U_{P,R} (A) ≜ −cost(A) + cost(P) − cost(Rewrite_{R} (P, A))
```

Here P represents the corpus and **A** is the abstraction. The `cost(.)` is a function with the following properties:

```
cost(λ.e′) = cost_λ + cost(e')
cost(e'e'') = cost_{app} + cost(e') + cost(e'')
cost($i) = cost_{$i}
cost(t) = cost_{t}(t), for t ∈ Gsym
cost(α) = cost_{α}
```

where `cost_λ`, `cost_{app}`, `cost_{$i}`, and `cost_{α}` are non-negative constants, and `cost_{t}(t)` is a mapping
from grammar primitives to their (non-negative) costs. `Gsym`, as we will talk about later as well, is the set of primitives in a DSL.

Now they (the authors) dive deeper into explaning how this works. But I won't do that just yet because we haven't covered a lot of stuff, so let's do that first. 

> At a high level the utility function above seeks to maximize the product of the size of the abstraction and the number of locations where the abstraction can be used

In the case of the three snippets shown, a single abstraction that maximizes the utility would be:

```
fn0 = λa. λb.(+ 3 (* a b))
```

and hence when we write the 3 snippets using the shared abstraction, the size of the corpus is minimized:

```
λx. fn0 (+ 2 4) 2
λxs. map (λx. fn0 4 (+ 3 x)) xs
λx. * 2 (fn0 x (+ 2 1))
```

- Here we need to understand what a `top-down` search even means. For this, I am going to make use of their python API.

```python3
from stitch_core import compress

# The same programs as above, written in de Bruijn style
programs = [
    "(lam (+ 3 (* (+ 2 4) 2)))",
    "(lam (map (lam (+ 3 (* 4 (+ 3 $0)))) $0))",
    "(lam (* 2 (+ 3 (* $0 (+ 2 1)))))"
]

# Iterations control the number of abstractions
res = compress(programs, iterations=1, max_arity=2)

res.abstractions[0]
# fn_0(#0,#1) := (+ 3 (* #1 #0))

# We can rewrite with the abstractions

from stitch_core import rewrite
a = rewrite(["(lam (+ 3 (* (+ 1 1) 1)))", "(lam (- 5 (+ 3 (* $0 (+ 2 1)))))"], res.abstractions)
# [
#     '(lam (fn_0 1 (+ 1 1)))',
#     '(lam (- 5 (fn_0 (+ 2 1) $0)))'
# ]

# We can also do silent=False

res2 = compress(programs, iterations=1, max_arity=2, silent=False)
# This will produce a lot of interesting outputs
```

Let me show you the output produced by the verbose mode:

```
**********
* Stitch *
**********
Programs:
	 num: 3
	 max cost: 910
	 max depth: 9

=======Iteration 0=======
num_paths_to_node(): 0ms
associate_tasks() and other task stuff: 0ms
num unique tasks: 3
num unique programs: 3
cost_of_node structs: 0ms
get_zippers(): 0ms
85 zips
arg_of_zid_node size: 85
Tracking setup: 0ms
ran analyses: 0ms
arity 0: 0ms
got 1 arity zero inventions
built SharedData: 0ms
TOTAL PREP: 0ms
running pattern search...
TOTAL SEARCH: 0ms
TOTAL PREP + SEARCH: 0ms
Stats { worklist_steps: 59, finished: 1, calc_final_utility: 23, calc_unargcap: 4, donelist_push: 1, azero_calc_util: 2, azero_calc_unargcap: 1, upper_bound_fired: 0, free_vars_fired: 11, single_use_fired: 43, single_task_fired: 45, useless_abstract_fired: 2, force_multiuse_fired: 0 }
Cost before: 2526
0: utility: 302 | final_cost: 1920 | 1.32x | uses: 3 | body: [fn_0 arity=2: (+ 3 (* #1 #0))]
post processing: 0ms
Chose Invention fn_0: utility: 302 | final_cost: 1920 | 1.32x | uses: 3 | body: [fn_0 arity=2: (+ 3 (* #1 #0))]

=======Compression Summary=======
Found 1 inventions
Cost Improvement: (1.32x better) 2526 -> 1920
fn_0 (1.32x wrt orig): utility: 302 | final_cost: 1920 | 1.32x | uses: 3 | body: [fn_0 arity=2: (+ 3 (* #1 #0))]
Time: 0ms
```

- You can see that it found the same abstraction as before, and moreoever, some stats.

Now let's understand their **Corpus Guided Top-Down Search** mechanism.

### Corpus Guided Top-Down Search (CTS)

The paper is actually written in a very textbook like manner which is lovely for me cause now I can read and understand (as opposed to read and not understand).

1. `Grammar`: The algorithm operates on lambda calculus expressions with de brujin variables. We say `e'` is a **subexpression** of `e` if `e=C[e']`, where C is a context defined by another paper.

Breaks... What is `C`? [This](https://www2.ccs.neu.edu/racket/pubs/tcs92-fh.pdf) is the relevant paper. From the paper some relevant things which I found are summarized below:

```
The expression C[e] stands for the result of putting the expression e into the hole of the context C, which may bind free variables in e

For the formal definition, we rely on the concept of a term context, which are expressions with a hole ([ ]) at the place of a subexpression: 

C ::= [ ] | (e C) | (C e) | (λx.C).
```

A few questions that you may have are:

1. What's a **free variable in e**?
2. What's **binding** that mean?
3. What is a **hole of the context**?
4. What's exactly a **subexpression**n?

I will only answer the subexpression part because others are a little hard :>. For us OCaml programmers (haha, I am calling myself an OCaml programmer now), we can reason about what's happening exactly in the following way:

- You can think of a Context `C` as an AST where exactly one node is missing.

Something like:

```ocaml
type context =
  | Hole                 (* The [·] *)
  | CLam of context
  | CAppLeft of context * expr
  | CAppRight of expr * context
```

- Then we take the context and plug the expression `e'` into the hole

Assume a curried application of the `+` operator like `(+) 3 4`, we can have an AST variant in OCaml like this:

```ocaml
type expr =
  | Lam of expr          (* \lambda. e *)
  | App of expr * expr   (* e1 e2 *)
  | Var of int           (* $i (de Bruijn index) *)
  | Prim of string       (* t (built-in primitives like +, 3) *)
```

Then this application would look like:

```ocaml
let e = App (App (Prim "+", Prim "3"), Prim "4")
```

Now a `subexpression` is anything you pluck out out this definition of `e`. Say `Prim "3"`, which is a valid subexpression for `e`. Because according to the paper, we need to find a context C such that if we plug `Prim "3"` into it, we get `e`.

So, if we let the context C be:

```ocaml
let C = App (App (Prim "+", Hole), Prim "4")
```

And we plug in the Hole with `Prim "3"`, we get `e`, hence `Prim "3"` is a subexpression for `e`. Hope that atleast gives you a concrete example to keep in your head.

Now the fact of the matter here is that, it's not very relevant for us to dive deep into **De Bruijn's indices** because its a whole new post of its own. Some relevant information can be:

- This was of writing the variables will turn them into integers
- There are `levels` to this (quite literally)
- The specific integer depends on how many lambdas are between it and its root lambda.

Example:

```
λx. λy. (x y) ==> λ λ ($1 $0)
```

The `($0)` means its bound to the first lambda going right to left, while the dollar `$1` means its bound to the left-most lambda. The `1` indicates the number of lambda inbetween it and the lambda its bound to.

A free-variable can be thought of as something like:

```ocaml
let y = 10
let my_func = fun x -> x + y
```

in this case, the variable `x` is bound, but `y` is free. Hence the expression for `my_func` is **not** closed. 

- According to the paper, if you have a closed expression, it can be thought of a program. And a bunch of those programs is what is called the `corpus`.

2. `Abstraction`: This is basically G (the grammar) extended by the abstractions we've discovered, or any other.

3. `Partial abstraction`: This is when there are `Holes` in the tree of abstraction.

4. `Lambda unification`: This is the technique they're using to help with De Bruijn's indices and subexpressionss.

> Here the authors have written a lot about what each function should do. If you're interested then check if out. I think the algorithm is more exciting.

## The algorithm

> Given a corpus P, rewrite strategy R, and utility function U_{P,R} (A), the objective is to find the abstraction A that maximizes the utility U_{P,R} (A).

CTS takes a **branch-and-bound** approach which will be described further on.