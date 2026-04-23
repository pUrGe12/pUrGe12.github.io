+++
title = "Modules and structures in OCaml"
date = 2026-04-23
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## Modules and structures

Let's start by looking at some code we had seen before:

```ocaml
type 'a mylist = 
	| Nil
	| Cons of 'a * 'a mylist

let rec map ~f:f = function
	| Nil -> Nil
	| Cons (a, b) -> Cons ((f a), map ~f:f b)
```

and for trees,

```ocaml
type 'a tree = 
	| Leaf -> Leaf
	| Node of 'a * 'a tree * 'a tree

let rec map ~f:f = function
	| Leaf -> Leaf
	| Node (a,b,c) -> Node ((f a), map ~f:f b, map ~f:f c)
```

Now the problem is, both of these functions are named `map`! And we also don't want map to be called `maplist` or `maptree` cause that makes it harder to remember and call it. So, we'll have to be clever about this, and encode each of these in a `module`.

This is how we'd do it for the lists part:

```ocaml
module MyList = struct
	type 'a mylist = 
		| Nil
		| Cons of 'a * 'a mylist

	let rec map ~f:f = function
		| Nil -> Nil
		| Cons (a, b) -> Cons ((f a) * map ~f:f b)
end
```

The `module` syntax is as follows:

- Start's like `module <module-name> = struct`
- Then you write all your definitions and functions
- Then you write `end` and boom. Its a module.

```ocaml
module Tree = struct
	type 'a tree = 
		| Leaf -> Leaf
		| Node of 'a * 'a tree * 'a tree

	let rec map ~f:f = function
		| Leaf -> Leaf
		| Node (a,b,c) -> Node ((f a), map ~f:f b, map ~f:f c)
end
```

Now we can call it nicely using:

```ocaml
MyList.map succ (Cons (1, Nil))
Tree.map succ (Node 1, Node (1, Leaf, Leaf), Node (2, Leaf, Leaf))
```

Of course, OCaml won't know that a Node is since its inside a module now!. So, how do we tell it?

```ocaml
let t = Tree.Node (1, Tree.Node (2, Tree.Nil, Tree.Nil), Tree.Node (3, Tree.Nil, Tree.Nil))
let t : int Tree.tree = Node (1, Node (2, Nil, Nil), Node (3, Nil, Nil))
```

Like that! Clearly the second version is superior.

## Stacks

Let's code up a stack in OCaml:

```ocaml
module MyStack = struct
(*It's basically a list with two methods push and pop, that is, a list with extra steps*)
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

The subtle problem with implementing a stack like this is that there is no notion of actually holding the value! So, why not just implement the stack as a list?

```ocaml

module MyList = struct
	type 'a stack = 'a list (*This is saying, alpha stack just means alpha list*)

	let empty = []

	let push x s = x :: s

	let pop s = match s with
		| [] -> failwith "cannot pop from empty stack"
		| _::t -> t

	let peek = function
		| [] -> failwith "cannot peek at empty stack"
		| a::_ -> a
end

```

Note that to create the stack we don't have a new keyword, we just use the empty stack defined inside the module. Also, ALL OF THESE OPERATIONS ARE **immutable**. So, if you `pop` from `s`, notice how it doesn't really change `s`. It gives you a new list in itself.

This is called a **functional data structure**. It is always immutable!

- To evaluate a module, we evaluate each definition from the top to the bottom and that gives us the module value, henceforth called the module.

- You cannot pass a module to a **function as a parameter**
- You cannot bind a module with `let`
- Cannot return module from a function output

Modules are their very own thing. Unlike classes which you can pass to functions in python (note that those are class objects not classes though!), (python is like jarringly different man!), you cannot do any such shit here.

## Scopes and opening

Okay now lets say we want to create a stack, push to it, and peek at the top value:

```ocaml
let a = MyList.peek (MyList.push 0 MyList.empty)
```

I had to write `MyList` 3 times! That's bad. We can tell the compiler that I am going to using the `MyList` module using:

```ocaml
let a = MyList.(empty |> push 0 |> peek) 
(*or doing this, using a local open*)
let w = 
	let open MyList in 
	empty |> push 0 |> peek
```

Both are equivalent ways of doing it, their utility depending on what the program calls for. For example, you would typically use the second let expression local opening when you have a long body of code where you want to use this as opposed to a single line.

Another way to write this is to do a **global** open!

```ocaml
open MyList
let w = empty |> push 0 |> peek
```

If you open two global modules which use the same names -> we're gonna have a problem here!
