+++
title = "Queues and dealing with options"
date = 2026-04-23
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## Implementing queues as a list

Lets start by defining our queue as a list

```ocaml
type 'a MyQueue = 
	| Nil
	| Cons of 'a * 'a MyQueue
```

But we ofcourse want to wrap this around a module:

```ocaml
module MyQueue = struct	
	type 'a queue = 'a list;; (*just another name for alpha list*) 
	let empty_queue = [];; (*This is what we'll use to build our queue*)
	
	let enqueue v q = q @ [v];; (*This is a linear time operation*)

	(*gets the first element of the list*)
	let peek = function
		| [] -> None
		| a::_ -> Some a;;

	(*Gets the rest of the list*)
	let dequeue = function
		| [] -> None
		| _::a -> Some a;;
end
```

Is the more efficient way of adding an element at the end of the list is to reverse it first?

```ocaml
let enqueue val q = List.rev (val::List.rev q);;
```

100% **not**! Because firstly, we're traversig the list twice, so its twice as bad as `q @ [val]`. Secondly, They are equivalent in terms of time complexity O(n). We have a much sleeker solution. Let's look at it.

1. We'll represent the queue as two lists, front and the back of the queue

```ocaml
(*queue is a record with an arbitrary dividing line in between*)
type 'a queue = {
	front: 'a list;
	back: 'a list;
}

(**E.g. front = [1;2;3] and back = [0;9;8;7] represents the queue = [1;2;3;7;8;9;0]
so, we'll be having the `back` of the queue in the reversed order*)
```

2. Implement the `peek`

```ocaml

let empty = {
	front = [];
	back = [];
}

(*If we think about it, if the front is empty, then back must also be empty
This is a design decision we're making. This means I don't have to match anything
for the back*)
let peek = function 
	| {front = []} -> None
	| {front = a::_} -> Some a
```

3. Implement the `enqueue`

```ocaml
let enqueue v = function
	| {front = []} -> {front=v; back =[]}
	| q -> {q with back = v :: q.back}

(*Pretty darn interesting. So we're saying if the queue is non empty, then we return
q but we cons the value to the back. Since that will later get reversed anyway, we're
good to go

Do note the syntax here
*)
```


3. Implement the `dequeue`

```ocaml
let dequeue = function
	| {front = []} -> None
	| {front = _::b; back} -> Some {front=b;back}
```

Note that this implementation is not quite complete, because I haven't handled my own requirement that when the front (b) is empty then the back must also be empty.

```ocaml
let dequeue = function
	| {front =[]} -> None
	(*Now there might still be some elements in the back, we just need to move them
	to the front of the queue*)
	| {front = _::[]; back} -> {front=List.rev back; back=[]}
	| {front = _::b}; back} -> {front=b;back=back}
(*Now this is constant time except in that rare case where we hit the empty tail*)
```

Very neat!


## Exceptions vs options

Options as you should recall are `Some` and `None`. The good thing baout exceptions is that we don't have to worry about options! As in we can simply chain together multiple operations without have to "optionally" get a response from a function.

Because if we're optionally getting a response we'll have to handle the complementary as well. For example:

```ocaml
open MyQueue
let q : int list = empty_queue |> enqueue 1 |> enqueue 2 |> dequeue |> peek
```

This gives me a type error saying that it expected an optional queue but it got a real queue. So what if we could make a pipeline operator that handles this for us?

Recall how the original pipeline operator was defined as:

```ocaml
let (|>) x f =
	f x
```

Takes an argument and a function and applies that function to the argument (passes in the argument to the function). Now we can have the argument as an option, so let's do this:

```ocaml
let (>>|) opt f = match opt with
	| None -> None
	| Some x -> Some (f x)
```

This works (also available in the standard library as `Option.map`), so now we can write this:

```ocaml
open MyQueue
let q : int list = empty_queue |> enqueue 1 |> enqueue 2 |> dequeue >>| peek
```

but what if I want to dequeue again? I can't do that because the new operator gives out an option response but the dequeue accepts only normal queues! And the normal pipeline also won't work because that will raise a type error.

So, we'll have to come up with a new operator, that will let me return a non-option too:

```ocaml
let (>>=) opt f = match opt with
	| None -> None
	| Some x -> f x
```

using this towards the end, we'll be golden. This operator is present as `Option.bind`.

```ocaml
open MyQueue
let q : int list = empty_queue |> enqueue 1 |> enqueue 2 |> dequeue >>| enqueue 42 >>= dequeue >>| peek
```
