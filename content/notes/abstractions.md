+++
title = "Abstractions"
date = 2026-05-16
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## How to create specifications

The template for specifying the behaviour of a function has 4 pieces to it:

```ocaml
(**
[f x] is ...
Example: ...
Requires: ...
Raises: ...
*)
val f : t -> u
```

To write a good documentation you need to provide specifications like these to the client. This is usually write in the `.mli` file above the declaration of the name.

We can also add effiency details as part of the function (like saying, this function will always run with constant space). You don't have to write types in the precondition of course.

- For pre-conditions, programmers often tend to say "this accepts only X" and NOT check for it.

This is a defensive programming technique, if you don't pass in X, and instead pass in Y to that function, you're at fault. The idea is to not **assert** the precondition because that might **mess** with the time complexity or space complexity of the function.

So there is mutual trust that you will READ THE FUCKING MANUAL.

## Data abstraction

A **data abstraction** is a specification of operations on a set of values, while a **data structure** is an implementation of the data abstraction with a particular implementation.

Let's try this out for sets:

```ocaml

module type Set = sig
	type 'a t

	(*Defines an empty set*)
	val empty : 'a t
	
	(*Adds an element to the set*)
	val add : 'a -> 'a t -> 'a t

	(*returns the size of the set*)
	val size : 'a t -> int

	(*Checks if a particular item exists in the set or not*)
	val mem : 'a -> 'a t -> bool
end
```

and we've written out a data abstraction for a data structure! (I am finding this chapter 6 pretty boring...)


Let's implement this with a data structure based on lists:

```ocaml
module ListSet : Set = struct
	type 'a t = 'a list

	let empty = []

	let rec mem vali = function
		| [] -> false	(*Or raise an error -> Depends on specs*)
		| a::t -> (
			if vali = a then true
			else mem vali t
		)

	let add vali s = 
		if not mem vali s then vali :: s
		else s

	let size s = 
		let rec aux acc s = match s with
			| [] -> acc
			| h::t -> aux (acc+1) t
		in
		aux 0 s

end
```

The problem is, this implementation of sets is correct iff the list being passed to it, contains no duplicates! The onus then falls onto the client (the consumer of the struct) to make sure that there are no duplicates in whatever list they are giving us.

This is where specs are helpful cause we can shift the blame! Now ofcourse a set where you have to manually deduplicate is kinda dumb because then I'll just use a normal list right! -> That's the tradeoff your pre-conditions can have!

## Efficiency

Look closely at the add function:

```ocaml
let add vali s = 
	if not mem vali s then vali :: s
	else s
```

If we had the naive add, it would be constant time, but because we're running `mem vali s` before that, time complexity is bumped to linear time. (Even though `mem` is tail-recursive, its still a linear time function).

The reason why we do this is because we had added a pre-condition that we won't allow lists to contain duplicates! But what if we did:

```ocaml
let add vali s = vali :: s
```

but then what of the size function? We cannot return the total list size as that would violate the principle of sets, we'd be counting duplicates. Hence, the `size` function needs to change then:

```ocaml
let size s = 
	let rec aux acc s = match s with
		| [] -> acc
		| h::t -> (
			if mem h s then aux acc t else aux (acc+1) t)
	in
	aux 0 s
```

And now we should be good! But note how this is actually even worse than **O(n)** (**O(n^2)**)!

The simplest thing to do ofcourse would be to remove all the elements of the list first, then we can just take the length of the list. To do this, let's make use of the list library functions:

```ocaml
let size s =
	s |> List.sort_uniq Stdlib.compare |> List.length
```

Note that this not a recursive function call anymore, but its `O(nlogn)`, better than before!

## Union operation

Let's add a union operation to the signature

```ocaml
module type Set = sig
...
	val union : 'a t -> 'a t -> 'a t
end
```

Now this is tricky because the naive way of doing this is simply `s1 @ s2`, but that's not going to work if we **disallow duplicates!** (that is, no duplications is our invariant). We need to therefore figure this out.

Another easy way is to do the union naively, then sort it uniquely!

```ocaml

module ListSet = struct
...
	let union s1 s2 = 
		s1 @ s2 |> List.sort_uniq Stdlib.compare
end
```

The idea is to make sure you understand what you don't violate and what you do!

## Abstraction functions

There were question questions which we needed to answer for representations:

1. How to interpret the representation type as the data abstraction?
-> Abstraction Function (**AF**)

2. How to determine which values of the representation type are meaningful?
-> Representation Invariant (**RI**)

To demonstrate this, we can write the specification for the **module** above as:

```ocaml

module ListSet : Set = module
	(**
	AF: The List [a1;a2;a3...] represents the set {a1;a2;a3...}, and
	the empty list [[]] represents the empty set.

	RI: The List may (may not, whatever you choose here) contain duplicates
	*)
	...
end
```

The purpose of the abstraction function is to clarify the **client's point of view** of the representation.

- The idea is very simple. Abstract away.

## Representation invariant

The representation invariant is basically telling us which values of the concrete type are allowable and which aren't. This is for the client to understand how to specify certain params to the functions.

> You should write this first before implementing operations -> Because it forces you to think about the design before hand

We can violate the RI in the body of the structure but the input and output must hold for the RI.

## Implementing the RI

This is actually a very useful technique. You can usually implement a function like `rep_ok` and ensure that the RI holds:

```ocaml
let rep_ok x:t = if (*check for RI*) then t else fail_with "RI_ERROR" 
```

This is checking the properties of both the input and the output. Note that this **can/will** change the time complexity of the programs you are trying to implement, so use this with caution!

To avoid that, you can change the implementation to a variation of the check, something simpler which has the same guarantees.
And you can also add code to turn it off or on. Think of that like an `ifdef` in C/C++ or config flags.

## Commutation of the abstraction function

The idea behind this is that, an **abstraction function** is correct if it commutes, that is, the order of application of the abstraction function and the concrete operation doesn't matter.

> AF(OP(S)) = OP(AB(s)) ; where OP -> Some operation of the concrete value and AF -> Abstraction function representation

