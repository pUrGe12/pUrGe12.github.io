+++
title = "Higher order abstractions for repetitive code"
date = 2026-04-04
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## Fold

What if we want to sum or concatenate all elements of the list? Pretty simple functions:

```ocaml
let rec sum = function
	| [] -> 0
	| a::t -> a + sum t;;

let rec concat = function
	| [] -> ""
	| a::t -> a ^ concat t;;
```

Now again, just like last time, we're seeing a lot of the same patterns, let's abstract it away:

```ocaml
let rec combine ~init:init = function
	| [] -> init
	| a::t -> a some_op combine t;;
```

What should be the return type when the list is empty? We'll let the combine function, take in that initial value. And how do we decide what operation? We'll again take it as a function:

```ocaml
let rec combine ~init:init ~f:f = function
	| [] -> init
	| a::t -> f a (combine ~init:init ~f:f t);;
```

Now let's see, how does the sum look like now?

```ocaml
let sum x y = x + y;;

let sumlist = combine ~init:0 ~f:sum

(*now we should be able to use sumlist, because we just defined it
as a partial function. We could also write it as an anon function
cause why risk readability*)

let sumlist = combine ~init:0 ~f:(fun x y -> x+y);;

let a = sumlist [1;2;3];;
```

And what about the concat one?

```ocaml
let concatlist = combine ~init:"" ~f:(fun x y -> x ^ y);;
```

The OCaml library exposes a function called `fold` which has the same idea as the `combine` function we wrote.

## fold_right

Now `fold` has a few variants, one of them is `fold_right`, that is, it **folds** the elements of the list from the right to the left. The fold function is also available inside the `List` module (we'll study about modules later).

```ocaml
List.fold_right ~f:f [a;b;c] ~init:init
```

Think of this as `accumulating` an answer by:

- Repeatedly applying `f` to an element of list and the "answer so far"
- Computes `f a (f b (f c init))` (This is kinda like currying!)

So "apply f to c and init, then apply f to b and the answer to the previous one, then to a and the answer to the previous one."

Can we code the `fold_right` algo ourselves?

```ocaml
let rec fold_right ~f:f ~acc:acc = function
	| [] -> acc
	| a::t -> f a (fold_right f acc t);;
```

We'll start calling the initial value the `accumulator`. The standard library actually implements it like this:

```ocaml
let rec fold_right f lst acc = 
	match lst with
	| [] -> acc
	| a::t -> f a (fold_right f t acc);;
```

So, `fold_right` basically means that you must accumulate the result of the right-most element of the list first. Similarly, there exists a `fold_left` which accumulates the left-most elements of the list first. Effectively it is `f(f(f(init a) b) c)`.

```ocaml
let rec fold_left f acc = function
		| [] -> acc
		| a :: t -> 
			let acc' = f acc a 	 (*This is what we have acculumated so far, first accumulate the left part*)
			in (fold_left f acc' t)

(*We could then write this as*)

let rec fold_left f acc = function
		| [] -> acc
		| a :: t -> fold_left f (f acc a) t
``` 

When the operation is associative, folding from the left or right doesn't make a difference. But its for those other operators where it does make a difference! 

> fold_left is tail_recursive! So, compiler can optimize it.

Note that we can reverse a list by using `fold_left`... (and its naturally tail-recursive)

```ocaml
fold_left (fun lst x -> x :: lst) [] [1;2;3]
```

## Filter

Let's now consider the task of keeping some elements in a list, while dropping others (that is, filtering):

```ocaml
(*This is a function that would keep only even elements of the list*)
let rec filter_even_values = function
	| [] -> []
	| a :: t -> begin 
		if a mod 2 = 0 
			then a :: filter_even_values t
		else
			filter_even_values t
	end

(*This is a function that would keep only odd elements of the list*)
let rec filter_odd_values = function
	| [] -> []
	| a :: t -> begin 
		if a mod 2 = 1 
			then a :: filter_odd_values t
		else
			filter_odd_values t
	end
```

Now again we can notice a very similar pattern here, so we should do that. We'll probably need a filtering condition, a function that takes in a value and decides whether to keep it or not. It can simply give me a `boolean`.

```ocaml
let rec filter ~f = function
	| [] -> []
	| a :: t -> begin
		let b = f a in
			if b then
				a :: filter ~f:f t
			else
				filter ~f:f t
	end

(*Or a bit syntactically simplified*)

let rec filter ~f:f = function
	| [] -> []
	| a :: t -> begin
		if f a then
			a :: filter ~f:f t
		else
			filter ~f:f t
	end
```

And that's the filter version I came up with! (I haven't watched what the professor did yet). But then I can use this version as:

```ocaml
filter ~f:(fun x -> if x mod 2 = 0 then true else false) [1;2;3;4];;
filter ~f:(fun x -> if x mod 2 = 1 then true else false) [1;2;3;4];;
```

Note that filter is not tail recursive because there is still extra work left to do :(. How do you generally build a tail-recursive function? You use an accumulator:

```ocaml
let filter f acc lst = 
	let rec aux f acc lst = match lst with
		| [] -> acc
		| a :: t -> begin
			aux f (if f a then a::acc else acc) t
		end
	aux f [] lst;;
```

1. Add an **accumulator** to the main function call
2. Simplify the main call to a normal function and create an **auxliary recursive function** inside it
3. The base case changes to return the **accumulator**
4. Just **call the aux** function, then find a way to fill the accumulator inside it, with an expression

One interesting observation with this is that, if we run it like this, we get the output but in the reversed order! So, if we want to fix that (think about it, because we're accumulting the first few values first, so we're essentially reversing the list). To fix that we'll have to return `List.rev acc` in the base case.

That's only for the tail-recursive case though.

## Trees with map and fold

So, we have read about using map and fold for lists, now let's try doing it for trees, creating our usual definitions:

```ocaml
type 'a tree = 
	| Leaf
	| Node of 'a * 'a tree * 'a tree

(*A recursive invariant for trees*)

let t = Node (
	3,
	Node (2, Leaf, Leaf),
	Node (2, Leaf, Leaf)
)
```

To `map` a tree (as in, take a function, and apply it to every node of the tree), we can do something like this:

```ocaml
let rec map ~f:f = function
	| Leaf -> Leaf
	| Node (a, b, c) -> Node (f a, map ~f:f b, map ~f:f c)
```

That's cool, it's going to return another tree with a function `f` applied to each of its node (we're only considering a binary tree for now). Let's create a simply function `f` to increment the value of each node.

```ocaml
map ~f:(fun x -> x +1) t;;
```

If we trace out the map function in UTop to see what's happening, we get this:

```
map <-- f:<fun>
map --> <fun>
map* <-- Node (<poly>, Node (<poly>, Leaf, Leaf), Node (<poly>, Leaf, Leaf))
map <-- f:<fun>
map --> <fun>
map* <-- Node (<poly>, Leaf, Leaf)
map <-- f:<fun>
map --> <fun>
map* <-- Leaf
map* --> Leaf
map <-- f:<fun>
map --> <fun>
map* <-- Leaf
map* --> Leaf
map* --> Node (<poly>, Leaf, Leaf)
map <-- f:<fun>
map --> <fun>
map* <-- Node (<poly>, Leaf, Leaf)
map <-- f:<fun>
map --> <fun>
map* <-- Leaf
map* --> Leaf
map <-- f:<fun>
map --> <fun>
map* <-- Leaf
map* --> Leaf
map* --> Node (<poly>, Leaf, Leaf)
map* --> Node (<poly>, Node (<poly>, Leaf, Leaf), Node (<poly>, Leaf, Leaf))
- : int tree = Node (4, Node (3, Leaf, Leaf), Node (3, Leaf, Leaf))
```

Let's also try `fold`:

```ocaml
let rec fold ~f:f acc = function
	| Leaf -> acc
	| Node (a, b, c) -> f a (fold ~f:f acc b) (fold ~f:f acc c)
```

This is going to recursively fold over the left and the right subtrees. You can now like, sum up all the elements of the tree if you want:

```ocaml
(*Note how this needs to be taking in 3 params*)
let sum x y z = x + y + z;;
let a= fold ~f:sum 0 t;;
```

Now we're going to dive into software dev in OCaml!