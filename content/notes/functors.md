+++
title = "Functors"
date = 2026-05-01
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## Functors

We know that module values and function values are distinct in OCaml => No mixing between them. (this is in contrary to say normal let definitions, function applications and many many other things that OCaml lets you mix and match between).

So, this means we can't perform functions on modules... Or can we? (enter vsauce music here)

Introducing **Functors**!

> A functor really is, just a, module, level, function

It takes in a module, and spits out a module (note -> No mix and match!) and is a little syntactically different from whatever we've seen so far, so lets get on with it.

Let's start by writing a simple module:

```ocaml
module type X = sig
	val x : int
end

module A : X = struct
	let x = 0
end
```

Suppose that I wanted to create another module, whose x is 1. Well, I **COULD** just go ahead and write it, BUT what if I need it all the way to 100? Would be nice to have a function that can take in this module as input, and add 1 to the x to it and give me a new module innit?

We could do that with a `functor`:

```ocaml
module IncX = functor (M : X) -> struct
	let x = M.x + 1
end
```

- We define a module `IncX` to be the output of a `functor`
- The functor takes in a module M, which is type bound to `X` (which we have defined before). So, only those signatures can make through to this **functor**.
- It returns a struct which defines a new x, that takes the module M's x and adds 1 to it (exactly what we wanted)

To use it, we need to call it on a module with brakets!

```ocaml
module B = IncX(A);;
B.x
```

Now this way of defining a functor is analogous to saying `fun x -> x + 1` which means anonymous functions. But we can do better and use syntactic sugar!

```ocaml
module IncX (M:X) = struct
	let x = M.x + 1 
end
```

Pretty neat man. One thing to note is that:

> With functors you MUST specify the module type of the input

## Standard library map

This is a great example of how **functors** can be used in OCaml. This uses a balanced binary tree (not a hashmap -> though we'll see that later as well). Note that this `map` is a set of key-value pairs. It is sometimes called a dictionary or an association table. Its different from the `map` we've seen before (that's the reason for having modules!).

The map module has a functor inside it called `Make`. In fact if we look at the official documentation for this [here](https://ocaml.org/docs/maps), we can see that they say:

> To use Map, we first have to use the Map.Make functor to create our custom map module. 

[This is the docs](https://ocaml.org/manual/5.4/api/Map.html) for the implementation. Here we can see the functor in clear display:

```ocaml
(*Output signature of the functor Map.Make.*)

module Make: 
functor (Ord : OrderedType) -> S  with type key = Ord.t
```

Recall that in functors we HAD to specify the signature of the input module, and in this case, that signature is `OrderedType`. So, let's see what that gives us:

```ocaml
module type OrderedType = sig 
	type t 

	(**A total ordering function over the keys. This is a two-argument function f such that f e1 e2 is zero if the keys e1 and e2 are equal, f e1 e2 is strictly negative if e1 is smaller than e2, and f e1 e2 is strictly positive if e1 is greater than e2. Example: a suitable ordering function is the generic structural comparison function compare.*)
	val compare : t -> t -> int
end
```

You can find this signature [in here](https://github.com/ocaml/ocaml/blob/8cad7474b341dca46c56daf68108ce3949028951/stdlib/pqueue.ml#L221) as well.

- Basically to **make** a map, you need to pass in a module which has two things in it, a type (for the keys) and a comparision function (for the keys).

- The comparision function is needed due to its implementation as a balanced binary tree, so it needs to be able to compare the keys at every node.

The output of the functor is `S`. The output signature look likes:

```ocaml
module type S = sig
	type key
	type !+'a t 
	(*This line will be explained later*)
	val empty : 'a t
	...
	...
end
```

The full signature is [here](https://ocaml.org/manual/5.4/api/Map.S.html).

### Example

Let's create a map for the days in a week. Let's start with a type for the days:

```ocaml
type day =
	| Monday
	| Tuesday
	| Wednesday
	| Thursday
	| Friday
	| Saturday
	| Sunday
```

and we can have a function that will take the day and map it to an integer:

```ocaml
let day_to_int = function
	| Monday -> 1
	| Tuesday -> 2
	| Wednesday -> 3
	| Thursday -> 4
	| Friday -> 5
	| Saturday -> 6
	| Sunday -> 7
```

Now suppose we want to create a map whose keys are days. So we'll have to create a module that specifies what the key type is, and how to compare them:

```ocaml
module type A = sig
	type t
	val compare : t -> t -> int
end

module DayKey = struct
	type t = day
	let compare day1 day2 = day_to_int day1 - day_to_int day2
end
```

How did I come up with this compare function? Because if you see the specification for the compare function, there are only a few things we need to keep in mind:

1. `compare e1 e2 = 0 if e1 = e2`
2. `compare e1 e2 > 0 if e1 > e2`
3. `compare e1 e2 < 0 if e1 < e2`

Our function does that cleanly. Now, we come to the functor part.

```ocaml
module DayMap = Map.Make(DayKey)

(**
module DayMap :
  sigwas
    type key = DayKey.t
    type 'a t = 'a Map.Make(DayKey).t
    val empty : 'a t
    val add : key -> 'a -> 'a t -> 'a t
    val add_to_list : key -> 'a -> 'a list t -> 'a list t
    val update : key -> ('a option -> 'a option) -> 'a t -> 'a t
    val singleton : key -> 'a -> 'a t
    val remove : key -> 'a t -> 'a t
    val merge :
      (key -> 'a option -> 'b option -> 'c option) -> 'a t -> 'b t -> 'c t
    val union : (key -> 'a -> 'a -> 'a option) -> 'a t -> 'a t -> 'a t
    val cardinal : 'a t -> int
    val bindings : 'a t -> (key * 'a) list
    val min_binding : 'a t -> key * 'a
    val min_binding_opt : 'a t -> (key * 'a) option
    val max_binding : 'a t -> key * 'a
    val max_binding_opt : 'a t -> (key * 'a) option
    val choose : 'a t -> key * 'a
    val choose_opt : 'a t -> (key * 'a) option
    val find : key -> 'a t -> 'a
    val find_opt : key -> 'a t -> 'a option
    val find_first : (key -> bool) -> 'a t -> key * 'a
    val find_first_opt : (key -> bool) -> 'a t -> (key * 'a) option
    val find_last : (key -> bool) -> 'a t -> key * 'a
    val find_last_opt : (key -> bool) -> 'a t -> (key * 'a) option
    val iter : (key -> 'a -> unit) -> 'a t -> unit
    val fold : (key -> 'a -> 'acc -> 'acc) -> 'a t -> 'acc -> 'acc
    val map : ('a -> 'b) -> 'a t -> 'b t
    val mapi : (key -> 'a -> 'b) -> 'a t -> 'b t
    val filter : (key -> 'a -> bool) -> 'a t -> 'a t
    val filter_map : (key -> 'a -> 'b option) -> 'a t -> 'b t
    val partition : (key -> 'a -> bool) -> 'a t -> 'a t * 'a t
    val split : key -> 'a t -> 'a t * 'a option * 'a t
    val is_empty : 'a t -> bool
    val mem : key -> 'a t -> bool
    val equal : ('a -> 'a -> bool) -> 'a t -> 'a t -> bool
    val compare : ('a -> 'a -> int) -> 'a t -> 'a t -> int
    val for_all : (key -> 'a -> bool) -> 'a t -> bool
    val exists : (key -> 'a -> bool) -> 'a t -> bool
    val to_list : 'a t -> (key * 'a) list
    val of_list : (key * 'a) list -> 'a t
    val to_seq : 'a t -> (key * 'a) Seq.t
    val to_rev_seq : 'a t -> (key * 'a) Seq.t
    val to_seq_from : key -> 'a t -> (key * 'a) Seq.t
    val add_seq : (key * 'a) Seq.t -> 'a t -> 'a t
    val of_seq : (key * 'a) Seq.t -> 'a t
  end
*)
```

- Now we can do all sorts of things! What? For example, we can "map" the name to a string for example:

```ocaml
let map_to_string = 
	let open DayMap in
		empty |> add Monday "Mon" |> add Tuesday "Tue"

(*Note that this is the same as saying:

let map_to_string =
	let open DayMap in
		add Tuesday "Tue" (add Monday "Mon" empty)

But the above is much cleaner.
*)
```

### Some functions

Let's look at some functions (methods?) inside:

- To check if a key is a member of the map -> `mem Monday map_to_string`
- To find the value of a key -> `find Tuesday map_to_string` (if key doesn't exist, it raises an exception)

```ocaml
type +'a t
```

- This means the type of maps from type `keys` to type `alpha`. We'll probably not have to worry about this too much.

- To add a new value in there: `let m' = add Sunday "Sun" map_to_string`
- To view the entire thing: `bindings map_to_string` (This gives a list of pairs, first element of which is the key and the second is its value)
