+++
title = "Pattern matching: An Introduction"
date = 2026-03-31
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

# Pattern matching

This is a powerful feature of OCaml. The idea is to break apart everything we have been building to see what all we have access to. The syntax is very simple:

```ocaml
let x = match not true with
	| true -> "nope"
	| false -> "yep";;
```

This is kind of a **switch** statement in C, but much more powerful as we'll soon see.

## Matching itself

This is an example of using a random pattern like "foooo" and seeing what happens:

```ocaml
let x = match 42 with 
	| foooo -> foooo;;
```

This gives us `42`. Here's what's happening:

1. The `foooo` is a **pattern variable**. This matches **anything**! Is there something special about `foooo`? No! You could very well write your name in there. Doesn't matter.
2. As long as the value you're binding to is the same as the pattern variable, you're good to go.

So, this works:

```ocaml
let x = match 42 with
	| yourname -> yourname
```

but this doesn't:

```ocaml
let x = match 42 with
	| yourname -> foooo
```

The valid example is effectively the same as:

```ocaml
let yourname = 42 in yourname
```

## Matching anything

To match anything (usually used as the **final conditional** check, think of it like an `else` part of an `if` statement), we use the special pattern `_`.

```ocaml
let x = match "foo" with
	| "bar" -> 0
	| _ -> 1
```

## Matching lists and tuples

These follow more or less the same rules:

```ocaml
let x = match [] with
	| [] -> "empty"
	| _ -> "not empty"
```

As with any ocaml expression, you cannot have two different return types for the match statement! So, if in the above you returned `0` instead of `not empty`, you'd get an error. (even though the code doesn't go there, the type checking rules are enforced at compile time)

We can do something cool now, check this out:

```ocaml
let x = match ["hello";"world"] with
	| [] -> []
	| head :: tail -> head :: ["unworld"]
```

Recall how we said building a list is sugar for writing `e1 :: e2 :: e3 ...`, this leverages that and extracts the first element of that list. This is what I am calling the `head`. There is nothing special about this name, you can call it whatever you want.

The remaining list gets absorbed into `tail`. So, now I return head but with `["unworld"]`. Cool right!

> What if you want to extract the second component of a list?

```ocaml
let snd3 ls = match ls with
	| a::b::c -> b
	| [] -> ""
	| _ -> "cooked"
```

What about extracting from tuples? We `unpack` it:

```ocaml
let fst3 tu = match tu with
	| (a,b,c) -> b
```

You can see, this is not very robust! Its going to only handle the case where we have 3 inputs in the tuple. And give us the second element in it.

## Matching records

Let's try out the following example:

```ocaml

type student = {
	name : string;
	grad : int;
};;

let me : student = {
	name = "Achintya";
	grad = 2027;
};;

(*To match records, we just write the field names in there*)
let name_with_year s = match s with
	| {name; grad} -> grad;;

name_with_year me;;
```

We can also say something like:

```ocaml
let name s = match s with
	| {name; _} -> name;;
```

As in, I know a `name` field should be there, just gimme the name and I will be happy. Notice how we're matching the fields, but getting the values? Yeah, that's important to keep in mind. Kinda intuitive too right.

## Some more pattern matching for lists

A list can either be:

1. nil -> []
2. Cons of elements onto another list

These are the only two possibilities. 

### Check if a list is empty

```ocaml
let is_empty lst = match lst with
	| [] -> true
	| _ -> false
```

Let's take a short detour to what this function's type looks like:

```ocaml
(*val is_empty : 'a list -> bool = <fun>*)
```

So, in this case:

1. `val is_empty` = That's the name of the function in the environment, OCaml's telling us its a bound value.
2. `'a list` = it takes a list which can be a list holding any type as its polymorphic
3. `-> bool` = returns a boolean
4. `<fun>` = `is_empty` is a function

Nice and easy.

### Sum the elements of a list

```ocaml
let rec list_sum int_list = match int_list with
	| [] -> 0
	| a::t -> a + list_sum t;;
```

This is a `recursive` function which basically takes the first element of each list and adds it to the first element of the remaning list, until we have an empty list.

The `rec` keyword just defines a recursive function. Its to avoid any unambiguity of which function is recursive and which isn't. I have done a deep dive on Tail call optimisations in recursive functions in OCaml in a [blog post](https://purge12.github.io/blog/tco-ocaml/). You can check it out!

We can trace the output of the `list_sum` function in **utop** and get a nice little depection of what is going on:

```ocaml
utop # #trace list_sum;;

utop # list_sum [1;2;3;4];;
list_sum <-- [1; 2; 3; 4]
list_sum <-- [2; 3; 4]
list_sum <-- [3; 4]
list_sum <-- [4]
list_sum <-- []
list_sum --> 0
list_sum --> 4
list_sum --> 7
list_sum --> 9
list_sum --> 10
- : int = 10

utop # #untrace list_sum;;
```

### Length of a list

```ocaml
let rec lst_len lst = match lst with
	| [] -> 0
	| a::b -> 1 + lst_len b;;
```

If you've read my blog you'll realize this this program is **NOT** the best way to write this recursive function and we should ideally use an accumulator for TCO to happen, but for these notes, this is good enough.

### Append to a list

```ocaml
let append value lst =
	match lst with
	| [] -> value :: []
	| _ -> lst @ [value];;
```

The `@` operator is a list concatention operator. Note that we can also do this with a recursive function:

```ocaml
let rec append value lst =
	match lst with
	| [] -> [value]
	| a::b -> a :: append value b;;
```

Now if you're wondering which is a better approach, trace out the function! This is the recursive one:

```ocaml
utop # append "a" ["b";"c";"f";"o"];;
append <-- <poly>
append --> <fun>
append* <-- [<poly>; <poly>; <poly>; <poly>]
append <-- <poly>
append --> <fun>
append* <-- [<poly>; <poly>; <poly>]
append <-- <poly>
append --> <fun>
append* <-- [<poly>; <poly>]
append <-- <poly>
append --> <fun>
append* <-- [<poly>]
append <-- <poly>
append --> <fun>
append* <-- []
append* --> [<poly>]
append* --> [<poly>; <poly>]
append* --> [<poly>; <poly>; <poly>]
append* --> [<poly>; <poly>; <poly>; <poly>]
append* --> [<poly>; <poly>; <poly>; <poly>; <poly>]
- : string list = ["b"; "c"; "f"; "o"; "a"]
```

And this is the normal one:

```ocaml
utop # append "a" ["b";"c";"f";"o"];;
append <-- <poly>
append --> <fun>
append* <-- [<poly>; <poly>; <poly>; <poly>]
append* --> [<poly>; <poly>; <poly>; <poly>; <poly>]
- : string list = ["b"; "c"; "f"; "o"; "a"]
```

## Sugar for pattern matching

OCaml provides us a sugar for pattern matching using the `function` keyword. Check this out:

This in OCaml:

```ocaml
let f x y z = 
	match z with
	| p1 -> e1
	| p2 -> e2
```

is the same as writing this:

```ocaml
let f x y = function
	| p1 -> e1
	| p2 -> e2
```

> The last argument is being pattern matched and in the sugar, its assumed implicit to the function, we don't have to write it out!

For example:

```ocaml
let rec lst_len = function
	| [] -> 0
	| a::b -> 1 + lst_len b;;
```

or

```ocaml
let rec lst_sum = function
	| [] -> 0
	| a :: t -> a + lst_sum t;;
```

Pretty neat. Note that we only use it when we want to pattern match the `last argument`. Don't just go around writing it for fun.


## Cons vs Append operator

`::` -> prepends an element to a list -> **O(1)** in time complexity
`@` -> Concatenates two lists together -> **O(n)** in time compleixity (n is the length of the first list)