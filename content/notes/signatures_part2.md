+++
title = ".mli files and includes"
date = 2026-04-23
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

## .mli files

So we looked at implemeting signatures using the `module type` keyword, in the same file itself. But there is another way of doing this (which I hinted at before) which is to define a `.mli` file. This is an **interface** file which holds all your definitions so that you can decide what to keep public and what to keep private.

To give an example, let's bring out the stack code we had and define its type interface separately:

```ocaml
type 'a stack = 'a list		

let empty = []

let push elem s = elem :: s

let pop = function
	| [] -> failwith "Empty"
	| _::b -> b

let peek = function
	| [] -> failwith "Empty"
	| a::_ -> a
```

So the above is the normal .ml file which contains the implementation. Then we can create its **interface** file like this:

```ocaml
(*Note that this is just denoting the type of a stack whose elements are alpha*)
type 'a t

val empty : 'a t

val push : 'a -> 'a t -> 'a t
val pop : 'a t -> 'a t
val peek : 'a t -> 'a
```

And that's what the world will see! (You should add more comments therefore!). This factoring of code into two files makes them into a **compilation unit**.

## Compilation units

A compilation unit is just the `.ml` + `.mli` files together. The reason the are a unit is because there are inherent rules to writing one:

1. The names must match. That is the **strings.ml** file can have ONLY **strings.mli** as its interface file.
2. This is effectively the SAME as what we had done last time.

That is, when we said `module type NAME = sig ... end` and then defined a module like `module MNAME : NAME = struct ... end`, then the `NAME` ensured which functions were public which weren't and on.

This way of writing the compilation unit is effectively the same thing, with the added benefit that we can now work on the exposure separately from the core.

Note that the signature in this case is pretty much anonymous. You can see the above code as well, we **haven't** specifically written this FOR the module we've defined.

## Includes

We've seen in the past how OCaml uses different operators for interger and float arithmetic ("+" vs "+."). In abstract algebra there are `rings` and `fields` which let you abstract away. A ring for example in abstract algebra is an abstraction over **additional** and **multiplication**, but not just for numbers, for any other mathematical object (like polynomials for example).

So, let's define the signature of rings:

```ocaml

module type Rings = sig
	(*This is like saying, some type but I don't know what type, but not ANY type*)
	type t
	val zero : t (*There is a zero value of the same type*)
	val one : t

	(*Defining addition and subtraction*)
	val ( + ) : t -> t -> t
	val ( * ) : t -> t -> t
	val ( ~- ) : t -> t (*This is unary negation*)
	val string : t -> string (*Function to convert to a string*)
end
```

Now we can use these signatures to create a module for say integer arithemtic:

```ocaml
module IntRings : Rings = struct
	type t = int

	let zero = 0
	let one = 1

	let ( + ) = Stdlib.( + ) (*This is basically saying, bind this, to standard lib plus operator*)
	let ( * ) = Stdlib.( * )
	let ( ~- ) = Stdlib.( ~- )

	let string = string_of_int
end
```

Since we have bound the module definition to the interface Rings and Rings doesn't specify the type of `t`, as far as OCaml is concerned it binds all definitions to `t` itself. It doesn't care what exactly you do with the module types then!

We can play around, do something like:

```ocaml
let a = IntRings.(zero + one)
(*a is abstract, no clue about what the answer is until you string it*)
IntRings.string a;;

(*Now I could apply IntRings addition to a*)

let b = IntRings.(a + one);;
```

What if we want to create the successor function with IntRings?

```ocaml
(*successor for IntRings, takes `i`, and adds one to it. Assumes `i` is of type t*)
let succ i = IntRings.(i + one);;

(*or a little more refined*)

let succ2 i = IntRings.(string (i + one));;
(*or*)

let succ3 i = IntRings.(i + one |> string);;
```

The type of this function is going to be: `t -> t = <fun>` or `IntRings.t -> IntRings.t = <fun>`. Now you can see how we would abstract away the dot in floating point operations?

```ocaml

module FloatRing = struct
	type t = float

	let zero = 0.
	let one = 1.

	let ( + ) = Stdlib.( +. )
	let ( *) = Stdlib.( *. )
	let ( ~- ) = Stdlib.( ~-. )
	
	let string = string_of_float
end
```

And we won't have to change our programs one bit, since succ3 for example can be defined using the same operations:

```ocaml
let succ3 i = FloatRing.(i + one |> string);;
```

And this will work for floats! Interesting right. So, what if we wanted to say have division as well? Rings in general don't do divisons so we'll have to go for fields. 

```ocaml
module type Field = sig
	type t
	val one : t
	val zero : t

	val ( + ) : t -> t -> t
	val ( * ) : t -> t -> t
	val ( ~- ) : t -> t
	val ( / ) : t -> t -> t

	val string : t -> string
end
```

Notice the massive code duplication here! We as programmers hate that (You better hate it too!). That's where the idea behind `includes` comes into picture! 

> You can just include from any signature or module into any other signature or module and avoid code duplications

So the above `Field`, reduces to:

```ocaml
module type Field = sig
	include Rings
	val ( / ) : t -> t -> t
end

(*and we can define say IntFloat for div as well*)

module IntFields = struct
	include IntRings
	val ( / ) = Stdlib.( / )
end
```

So much cleaner isn't it!

## Include vs Open

These both can seem very similar, but they have some differences (both open modules for instance):

```ocaml

module M = struct
	let a = "string"
end

module N = struct
	include M
	let b = a ^ " string2" 
end

module O = struct
	open M
	let b = a ^ " string2" 
end
```

The difference will be obvious if you LOOK closely at UTOP:

```ocaml
module M : sig val a : string end
module N : sig val a : string val b : string end
module O : sig val b : string end
```

This means that the module N ended up "redefining" or "re-providing" the definitions and values in `M`. This is obviosuly as the name suggests!

So, you should use include, if you want to have your new module re-provide all those instances, otherwise use open if you just want to "use" the definitions in a module.
