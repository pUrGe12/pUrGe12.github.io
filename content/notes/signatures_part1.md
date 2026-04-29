+++
title = "Signatures and module types"
date = 2026-04-23
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## Signatures

OCaml has something called `signatures`. These can be thought of as type definitions for a module as we literally start with `module type`. Let's define a signature for the factorial function:

```ocaml
module type Fact = sig
	val fact : int -> int
end
```

So, yes even though I was spekaing about it in the sense of a module, its really applicable to functions as well. Here, we're saying that there exists a `value` called `fact` which has the type `int->int`.

The `val` keyword is pretty important, we see it in utop all the time. Don't try to use it in your programs as variable names!

Now we can define Modules which have this type:

```ocaml
module Factorial : Fact = struct
	let fact x = 
		let rec aux x acc = match x with
			| 1 -> acc
			| x -> aux (x-1) (x * acc)
		in
		aux x 1
end
```

This is just for the type checker to check that all the types work out correctly and for the programmer to ensure that they make lesser mistakes as the compiler will catch it!

- The `module type` is where we go to read the documentation for what a certain module is supposed to be doing. Its the public facing documentation for the world to see. You know where we're going with this? (shhh... `.mli` files).

- If in the module Factorial, we changed the name of the function to say `factorial`, it will throw an error saying that it expected to find `fact` but its not there.

The cool thing is, if say you write something like this:

```ocaml
module Factorial : Fact = struct
	let rec aux x acc = match x with
		| 1 -> acc
		| x -> aux (x-1) (acc *x)

	let fact x = 
		aux x 1
end
```

This is a valid way of writing the tail recursive function. Now if someone wants to access the `fact` function, they can do so like this:

```ocaml
let a = Factorial.fact 10
```

But what they **cannot** do is this:

```ocaml
let a = aux 10 1
```

Because we have not made the `aux` function accessible via the type definition of `Fact`. Hence, if we want users to access the `aux` function as well, we'll write:

```ocaml
module type Fact = sig
	val fact : int -> int
	val aux : int -> int -> int
end
```

## Describing our stacks

Porting code from the older notes:

```ocaml
module ListStack : Stack = struct
(*It's basically a list with two methods push and pop, that is, a list with extra steps
Note: Stack is defined below
*)
	type 'a stack = 'a list

	let empty = []

	let push ~entry:e ~stack:s = e::s
	let pop ~stack:s = match s with
		| [] -> failwith "Cannot pop an empty stack"
		| _::b -> b

	let peek = function
		| [] -> failwith "Cannot peek at an empty stack"
		| a::_ -> a
end

module MyStack = struct
	type 'a stack = 
		| Empty
		| Entry of 'a * 'a stack

	let empty = Empty

	let push ~entry:e ~stack:s = Entry (e, s)
	let pop ~stack:s = match s with
		| Empty -> failwith "Cannot pop an empty stack"
		| Entry (_, b) -> b

	let peek = function
		| Empty -> failwith "Cannot peek at an empty stack"
		| Entry (a, _) -> a
end
```

Now let's define these in the interface so that the public can use it:

```ocaml
module type Stack = sig
	val empty : a' list
	val push : a' -> a' list -> a' list
	val pop : a' list -> a' list
	val peek : a' list -> a'
end
```

Typically we would write more comments to explain what each of these do but its fine for now. So, this stack signature will fit the `ListStack` definition very well, but what about `MyStack`? The signature we have written is looking for `'a list` everywhere, which means its not general enough. Let's generalize this:

```ocaml
module type NewStack = sig
	(*A general stack*)
	type 'a stack

	(*definitions and methods for the general stack*)
	val empty : a' stack
	val push : a' -> a' stack -> a' stack
	val pop : a' stack -> a' stack
	val peek : a' stack -> a'
end
```

Therefore, we can now write:

```ocaml
module MyStack : NewStack = struct
	type 'a stack = 
		| Empty
		| Entry of 'a * 'a stack

	let empty = Empty

	let push ~entry:e ~stack:s = Entry (e, s)
	let pop ~stack:s = match s with
		| Empty -> failwith "Cannot pop an empty stack"
		| Entry (_, b) -> b

	let peek = function
		| Empty -> failwith "Cannot peek at an empty stack"
		| Entry (a, _) -> a
end
```

Let's also create these signatures for queues:

```ocaml

module type Queue = sig
	(*General representation of a queue*)
	type 'a queue

	val empty_queue : 'a queue
	val enqueue : 'a -> 'a queue -> 'a queue

	(*Recall how dequeue gave us Some or None -> Completely dependent on
	the implementation though*)
	val dequeue : 'a queue -> 'a queue option
	val peek : 'a queue -> 'a
end
```

Okay, now the thing is, if you want to apply this to your modules, and you had defined your modules before, you could also do a rebinding like this:

```ocaml
module NewListQueue : Queue = listQueueImp
```

Since this is also immutable, we've simply just created a new memory space and allocated the old module to it with a new name and more importantly, new type.

## Semantics

- You can specify `val`, `type`, `exception` and even other `module` inside a module type signature
- Two ways to define a module to be of a particular module type:

```ocaml
module name : Type = struct
	definitions...	
end

(*and*)

module name = (struct
	definitions...
end : Type)
```

- The type checker will ensure that everything defined in signature is defined in the attached module.
- Further it will ensure that **only** what is specified in signature will be accessible outside of the module. We say that the module is sealed at that signature.
- The definitions in the signature can be very general. (for example for a function giving `int -> int`, we can write `'a->'a` so long as it makes sense)
- And vice-versa, we can have `int->int`, and we can attach this to a more general function working on anything like `'a->'a`.

