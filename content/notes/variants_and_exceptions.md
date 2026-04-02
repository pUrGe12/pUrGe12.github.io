+++
title = "Variants and exceptions"
date = 2026-04-02
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

# Recursive parameterized variants

Let's create our own type for representing lists (a list of integers for now):

```ocaml
type intlist = 
	| Nil
	| Cons of int * intlist
```

Now that's weird. The type `intlist` is recursive, as in it mentions its own name inside its definition.

- You can think of the `intlist` inside as being the **tail** of the list and `int` being the **head**.
- We can build functions for our `intlist`

```ocaml
let rec length = function
	| Nil -> 0
	| Cons (_, tail) -> 1 + length tail;;
```

- The weird part is **how do we create an intlist**? Since the definition uses itself?

```ocaml
let a = Cons (1, Cons (2, Nil));;
```

That seems kinda weird. I won't have a good feel for it until I see it in the wild somewhere.

- Now what if we also needed a `string_list`? Do we just copy the whole thing and change names? That's kinda naive. Nope.

- The idea is to **parameterize** the type that is in the invariant, rather than hardcode it.

How to do that? Using our old friend `alpha`.

```ocaml
type 'a slist = 
	| Nil
	| Cons of 'a * 'a slist
```

The `alpha` goes to the left of the `slist`. Think of `slist` as a function that operates on types. That is, it takes in a type and returns a variant type. In this case, it's taking in the type `'a`.

```ocaml
let a = Cons (1, Cons (2, Nil));;
let b = Cons ("string1", Cons ("string2", Nil));;
```

We can optionally replace the **constructors** with the operators for those!

```ocaml
type 'a mylist = 
	| []
	| (::) of 'a * 'a mylist
```

Pretty cool right! Cause now my length function becomes:

```ocaml
let rec length = function
	| [] -> 0
	| _ :: t -> 1 + length t;;
```

That's exactly what we'd do for an inbuilt OCaml list. You know what this means?!

> A list is parameterized invariant on alpha!

# Options

This is another built in variable in the OCaml standard library. An `option` is defined very simply:

```ocaml
type 'a option = None | Some of 'a
```

Recall how we said that a type definition is essentially a function that operates on types? In this case, it takes a type `alpha`, and its a variant which is either `None`, or `Some` with the metadata `alpha`. The question is, what is `None` and `Some`.

> Think of the **option** like a box. Either the box is empty (**None**) or there is something in it (**Some**). The thing that **may be** inside it is **alpha**.

Nice. Its kind of like saying:

```ocaml
Some [1;2;3];; 
(* - : int list option = Some [1;2;3]*)
(*This can be read as: optionally, this is a list of integers*)
```

Why would you ever use these? For pattern matching! In cases where we **don't know** what to expect, we can do:

```ocaml
let get_val = function
	| None -> failwith "?? Nothing there"
	| Some x -> x
```

Basically says, if you find anything, gimme that value! We can optionally ask the programmer to give us a default value to return in case there is nothing inside the box:

```ocaml
let get_val default = function
	| None -> default
	| Some x -> x;;


type a = TAtype of {abcd:string;ab:int} | TBtype | TCtype;;
let c = TAtype {abcd="hello"; ab=10};;

get_val (TAtype {abcd="default";ab=20}) (Some c);;
get_val (TAtype {abcd="default";ab=20}) (None);;
```

But a better example of how this is used is for computing the maximum of a list. The maximum of an empty list can be defined as 0 or whatever by you, but the OCaml way of doing this, is to return **None** and for the cases where the list has a max, return **Some x**

```ocaml
let rec list_max = function 
	| [] -> None
	| a::t -> Some (max a (list_max t))

(*or if I write it with all types*)

let rec list_max (lst: 'a list) : 'a option = match lst with
	| [] -> None
	| a::t -> Some (max a (list_max t))
```

But these aren't gonna work. Because the compiler will throw and error saying that we're trying to compare an `alpha` type with an `alpha option`. Inside **max**. To resolve that we're gonna have to get the value out of the box.

```ocaml
let rec list_max (lst: 'a list) : 'a option = 
	match lst with
	| [] -> None
	| a::t -> match list_max t with
		| None -> Some a
		| Some m -> Some (max (a m));;
```

But this ALSO will throw errors, because you really should wrap your nested checks around **begin** and **end**.

```ocaml
let rec list_max (lst: 'a list) : 'a option = 
	match lst with
	| [] -> None
	| a::t -> begin
		match list_max t with
			| None -> Some a
			| Some m -> Some (max a m)
		end;;
```

`begin` and `end` are basically `(` and `)` but we use the words for pattern matching cause it looks better.

This was a nice heavy lecture. We don't complain about syntax remember.

## Exceptions

All exceptions in OCaml are `extensible variants`. What does that mean? Well, something like:

```ocaml
type exn = 
	| OhNo
	| File_not_found of string
```

The type `exn` is a built-in type in OCaml for all exceptions. This is a built in `extensible` variant.

```ocaml
exception OhNo of string;;
OhNo "oops";;
raise (OhNo "oops");;
```

You can define your exceptions then very easily. The `raise` function never produces a value. That's why the return type for raise will show up to be `alpha` because it's never truly going to return.

A few important exceptions:

1. `failwith "string"` => Raise when you know a part is harmful
2. `invalid_arg "string"` => Raise when you know the arguments don't make sense 

## Handling exceptions

Handling exceptions is basically pattern matching! For example, if we were trying to handle `Division_by_zero`, here's how we'd do it:

```ocaml
let safe_div x y = 
	try x/y with
		| Division_by_zero -> 0
```

Just like how we had `match .. with` this is `try .. with` and its specifically to match exceptions. You don't even have to write the case for when no exceptions are raised, and of course you cannot match against all exceptions!

So, `try .. with` is separated from `match .. with` because one of the reasons was the `match .. with` is exhaustive and compiler will throw an error.
