+++
title = "Types and function applications"
date = 2026-03-29
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## function types

- type `t -> u` is the type of a function which takes an input of type `t` and returns an output of type `u`.

We can extend this to multiple arguments,

- type `t1 -> t2 -> u` is the type of a function which takes an input of type `t1`, another input of type `t2` and returns an output of type `u`.

- So the type of a function is determined by the type of its arguments and the type of its output. This is why you cannot have different output types in ocaml for any branching conditions! That violates this rule.

## Partial function applications

When we define a multi-argument function, we don't **HAVE** to pass in all the arguments at once. We can partially pass in arguments. For example:

```ocaml
let func x y z = x ^ y ^ z;;
(* val func : string -> string -> string -> string = <fun> *)
```

now I can say something like:

```ocaml
let a = func "Hi", " There!";;
```

This is perfectly valid! So what will this expression evaluate to? It's going to assign a function to `a`, which is equivalent to a partially applied `func` on the arguments, that is:

```ocaml
(**Effectively: 
val a : string -> string = <fun> *)
a " HelloWorld! ";;	(*gives: "Hi There! HelloWorld! "*)
```

That's awesome! But the reason it works is even more awesome! The truth is that OCaml actually doesn't have multi-argument functions!!

A function like this:

```ocaml
let add = (fun x y z -> x + y + z);;
add 1 2 3;;
```

is completely equivalent to:

```ocaml
let add = (fun x -> (fun y -> (fun z -> x + y + z)));;
add 1 2 3;;
```

These are all partial function applications! Damn. That's awesome. This means multi-argument function functions are syntactical sugar for applying multiple single level anonymous functions. This actually comes directly from the founding father of functional programming `Alonzo Church`!

## Parametric polymorphic

These are function's who don't have a predefined type, that is, the compiler cannot figure out a single type to give such a function. This means that we can pass anything to such functions!

The simplest example is:

```ocaml
let f x = x;;
(* val f : 'a -> 'a = <fun> *)
```

Notice that ocaml assigns a special type to this, `'a` (pronounced "alpha"). This is similar to "Any" in python (but nope, that's just for humans and code editors, this is a compile time restriction!)

## Operators as functions

There are three types of ways of writing operations:

1. Infix
2. Postfix
3. Prefix

We're typically used to writing operations in the infix form, that is: `1+1=2`, but prefix actually allows us to look at a subtle variation in functional programming:

```ocaml
( = ) 1 2;; (*gives false*)
( + ) 1 2;; (*gives : int = 3*)
( - ) ((+) 1 1) 2;; (*gives 0*)
( * ) 4 5;; (*Gives 20, don't forget to put the space!*)
```

So, we can think of operators as functions as well if we look at the prefix form.

Let's look at `max`:

```ocaml
max;;
(*- : 'a -> 'a -> 'a = <fun>*)
max 1 2;; (*gives 2*)
```

But we can define `max` as an infix operator as well

```ocaml
let (<^>) x y = max x y;;
(<^>) 1 2;;	(*This gives 2*)
1 <^> 2;; (*This also works and gives 2*)
```

## Function application operators

- The `application operator` is simple:

```ocaml
let ( @@ ) f x = f x;; (*Takes in f and x, applies f to x*)
```

So, this lets us do something like:

```ocaml
print_endline @@ string_of_int 9;;
(*Which can also be written in the prefix format*)
( @@ ) print_endline (string_of_int 9)
```

Both of which are an equivalent way of writing:

```ocaml
print_endline (string_of_int 9);;
```

- The `reverse application` is also simpler, just reverse of application:

```ocaml
let ( |> ) x f = f x;;
```

This takes in an argument and a function, and applies the function to the argument. How can we use it?

```ocaml
let square x = x * x;;

let a = 5 in
	a |> succ |> square |> square;;
```

We basically say, increment 5, then square it (36), then square it again (1296). Without using the operator, we'd have to write:

```ocaml
let square x = x * x;;
let a = 5 in
	square (square (succ a));;
```

Which is ugly.