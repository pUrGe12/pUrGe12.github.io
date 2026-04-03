+++
title = "Trees, higher-order functions and maps"
date = 2026-04-03
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## Binary trees

A binary tree is a tree wherein each node has at most **2 children**. Its very similar to a singly linked list (support for which is the default in OCaml), except that it has two nodes instead of one.

```ocaml
type 'a tree = 
	| Leaf
	| Node of 'a * 'a tree * 'a tree

(*
Recall how we'll make a match case for this:

match x with
	| Leaf -> None
	| Node (a, b, c) -> Some a (*maybe*)
*)
```

Its a recursively parameterized variant. A `Leaf` is an empty tree that contains nothing. Why does the `Node` have 3 elements in it? Recall what we said for:

```ocaml
type 'a mylist = 
	| Nil
	| Cons 'a * 'a mylist 
```

we said that the `Cons` tag can be thought of as something having a `head` and a `tail` which is mylist again. In case of the tree, we have 2 branches not one, so we'll have two of the recursive `'a list` definitions, and the first **alpha** can be thought of as the branch that points TO the node.

Now understand this, to create a binary tree, I will have to define it like this:

```ocaml
let some_tree = Node (1, Node (2, Leaf, Leaf), Node (3, Leaf, Leaf));;
```

We're saying the some_tree is a `Node`, with a branch `1` that points to it (that is, the root of this node). It then creates two more nodes, one with a `2` and another with a `3`. The tree ends here because every other branch is a `Leaf`.

What if we wanted to take the size of the tree? That is to say, how many nodes does a tree have, how will you do it?

```ocaml
let rec size = function
	| Leaf -> 0
	| Node (_, left, right) -> 1 + size left + size right
(*This works because left and right will return type of 'a tree! or in this case int tree*)
```

This is awesome, and pretty easy to define right! What if you wanted to sum up all the elements, again pretty simple:

```ocaml
let rec sum = function
	| Leaf -> 0
	| Node (root, left, right) -> root + sum left + sum right
```

Man functional programming makes it really easy to work with trees.

## Functions as higher order

In OCaml (and in functional programming in general), functions are **higher order**, as in they can be passed around and used just like anything else.

```ocaml
let double x = 2 * x;;

let quad x = 4 * x;;
let quad_ x = double (double x);;
let quad__ x = x |> double |> double;;
```

What if we wanted to take the 4th power of a number? We can assume that we have the following primitives:

```ocaml
let square x = x * x;;

let forth_power x = x |> square |> square;;
```

There is a notion here of "applying a function multiple times" (in this case, twice). What if we could write a function that applies a function twice?

```ocaml
let twice f x = f (f x);;
```

That's it! This is a function that takes in as a function f and an argument x, applies f twice on x. Now we can do something like:

```ocaml
let forth_power x = twice square x;;
```

But we can also have partial functions. Something like this:

```ocaml
let partial_forth = twice square;;
```

Now `partial_forth` is a function, which is awaiting an argument `x` which it inherited from `twice`. 

## Map

Apparently Google's `MapReduce` was inspired from Lisp and functional programming. Anyways...

The idea of a `map` is to give it a function and an iteratable element and it will apply that function to each element of that iteratable element.

Do note that, doing something like this:

```ocaml
let a = (fun x -> some_function x) x;;
```

is the same as doing:

```ocaml
let a = some_function x;;
```

Do not get confused!

Alright, suppose we want to add one to every element of a list:

```ocaml
let rec add_1 = function
	| [] -> []
	| a::t -> a+1::add_1 t;;
(*yes I know its not optimial and not tail recursive, but its okay for now*)
```

What if we wanted to concatenate a string "3110" to every element of the list?:

```ocaml
let rec concat_3110 = function
	| [] -> []
	| a::t -> (a ^ "3110") :: concat_3110 t;;
```

Now they are quite similar right? The similar patterns are:

1. There is a **pattern matching** on the input
2. There is returning of the **empty list**
3. There is a pattern matching for **head and tail** of a non-empty list
4. There is a **cons** operation
5. To the right of the cons is a **recursive call**
6. To the left of the cons is **another operation**

This screams that the entire thing can be abstracted away! Let's try and factor out most of the code:

```ocaml
let rec transform = function
	| [] -> []
	| a::t -> ?? :: transform t;;
```

But now the question is, what do we push in place of the `??`? So, how about we take in the function as an argument that tells me how to do the transformation!

```ocaml
let rec transform ~f:f = function
	| [] -> []
	| a::t -> f a :: transform ~f:f t;;
```

beautiful! Now we can do something like:

```ocaml
let add_1 x = 1+x;;
let concat_3110 x = x ^ "3110";;

transform ~f:add_1 [1;3;4];;
transform ~f:concat_3110 ["hi"; "there"];;
```

Pretty neat right! But we could also write the `add_1` and `concat_3110` functions using the `transform` function:

```ocaml
let add_1 y = transform (fun x -> 1+x) y;;
let concat_3110 y = transform (fun x -> x ^ "3110") y;;
```

Guess what! `transform` is actually named a `map`. Its present in the standard library as `List.map`. You can use it in both of the ways we've defined above.

```ocaml
let rec map ~f:f = function
	| [] -> []
	| a::t -> f a :: map ~f:f t;;

let convert_string lst = map (fun x -> string_of_int x) lst;;

convert_string [1;3;4];;
```

remember what we said about bad programming smells above. We just fell into that trap!

```ocaml
let convert_string lst = map string_of_int lst;;
```

This is the right way of defining it. Both of them work, but this is what separates the great from good. The idea is:

> Factor out recurring code patterns, and reuse them, not re-write them
