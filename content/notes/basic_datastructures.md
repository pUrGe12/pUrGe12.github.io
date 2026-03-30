+++
title = "Basic datastructures and their syntax and semantics"
date = 2026-03-31
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

# lists

We can define a list in the following way:

```ocaml
let a = [];;
(* val a : 'a list = []*)
```

Note the **alpha** there? that's because we haven't passed anything inside the list yet. That alpha will take the type of the value present inside the list.

To define a more useful list, we separate the elements out using a ";".

```ocaml
let a = [1;2;3];;
(* val a : int list = [1;2;3]*)
```

Now, here's one thing you cannot do: Add elements to the list with different types! So, `["abcd"; 'a']` is not allowed (yet). 

> We will see later on how to have lists with different types cause that's actually a really important thing to have in any real usecase!

We can have nested lists:

```ocaml
let a = [[1;2];[1;4];[3;2]];;
(*val a : int list list = [[1;2];[1;4];[3;2]]*)
```

Now you can add an element to a list using the `::` operator.

```ocaml
0::[1;2;3];; (*gives [0;1;2;3]*)
```

- OCaml lists are always immuatable, once something goes inside a list, you can't change it
- You will have to redefine a new list if you want to make any changes
- Lists are "singly-linked" => They are ordered, and they work okayish only.

## List syntax and semantics

Syntax:

- `[]` => Is an empty list
- `e1 :: e2` => prepends element `e1` to list `e2`
- `[e1;e2]` is syntactical sugar for `e1::e2::[]`

The `::` operator is called "cons" which comes from LISP.

Semantics:

- To evaluate a list like: `[e1;e2]`, we first evaluate `e1` to `v1` and `e2` to `v2`
- We return `[v1;v2]`

## Records and tuples

`Records` are another basic datatype built into OCaml. To define that we use:

```ocaml
type student = {
	name : string;
	grad_year : int;
}
(*type student = { name : string; grad_year : int; }*)
```

This is a record type and we can create values of it, for example:

```ocaml
let me : student = {
	name = "Something";
	grad_year = 20120;
};;
(*val me : student = {name = "Something"; grad_year = 20120}*)
```

Now I can access individual elements of this record:

```ocaml
print_endline @@ string_of_int me.grad_year;;
print_endline me.name;;
```

Its essentially a dictionary acess if you think about it. But its also a little different.

## Tuples

Tuples are for created grouped data. You can create a type for your tuple as well!

```ocaml
type time = int * int * string;; (*time's gonna have 3 components, an int, another int and a string*)
let t1 : time = (10, 10, "am");;
```

We can also define it for points in a cartesian plane for example:

```ocaml
type points = float * float;;
let p1 : points = (1.2, 2.3);;
```

The real magic for the lists and tuples and records and all, come when we do matching! Which is coming soon. I belive.

Also you can `unpack` the tuple to access individual values:

```ocaml
let (a, b) = p1;;
a;;	(*gives 1.2*)
```

OCaml also has an inbuilt function called `fst` which is the `kestrel` operator from lambda calculus. It takes in two arguments and returns the first one!

```ocaml
fst;;
(** 'a * 'b -> 'a = <fun> *)
let a = fst p1;;
(* a becomes 1.2 *)
```

We can get the second component using `snd` which is like kestrel but reversed. Gives the second component after taking in two. You can clearly see that `fst` and `snd` only work when you have two elements in the tuple. For others, we unpack.

## Deciding datatypes

The question now is, how do you choose between `lists`, `tuples` and `records`? Here's the rule of thumb (not necessary but usually works):

- [x] If you have unbounded data: `lists`
- [x] If you have bounded data but you want to access it by position: `tuples`
- [x] if you have bounded data and you want to access it by name: `records`

Tuples are bounded because while we have ways to "extend" a list due to its "linked" nature. Both lists and tuples are immutable, and extending a list does give us a new list. But the idea is that every extension plays neatly into how the data is arranged.

## Record syntax and semantics

- One cool thing about field names in the type definition is that, we can have upto 4 million of them (I am not sure what's so special about 4 million).

- `e.f` lets you access field `f` of a **record** expression `e`. The `f` is an identifier, not an expression to be computed.

`Type checking`: If `e:t` and if `t` is defined as `{ t1 : v1 ... ti : vi ... }`, then `e.ti = vi`. Which basially means, `e` is a record of type `t`.

- Records and types are both immutable. For example, consider:

```ocaml
type rectangle = {height:int;width:int};;
(*type rectangle = { height : int; width : int; }*)
let square : rectangle = {height=1; width=1};;
(*val square : rectangle = {height = 1; width = 1}*)
{square with height=2};;
(*- : rectangle = {height = 2; width = 1}*)
square;;
(*- : rectangle = {height = 1; width = 1}*)
```

In this case, we have NOT mutated the value of square. We have created a copy of the record `square` with a field changed. You cannot change fields once they are set! This is because the `with` is also syntactical sugar for defining a new record.


## Tuple syntax and semantics

- If `ei ==> vi` then `(e1, ... , en) ==> (vi, ... , vn)`.
- If `ei : ti` then `(e1, ... , en) : t1 * ... * tn`.

Pretty simple this one right. Note that the **order** is very much relevant here!