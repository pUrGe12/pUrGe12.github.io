+++
title = "Introduction to variants"
date = 2026-04-01
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

# Variants

[The Real World OCaml part for variants](https://dev.realworldocaml.org/variants.html).

Variants are type definitions. The basic syntax of a variant type declaration is as follows:  

```ocaml
type <variant> =
  | <Tag> [ of <type> [* <type>]... ]
  | <Tag> [ of <type> [* <type>]... ]
  | ...
```

All variant tags are capitalized. So, you can have something like this:

```ocaml
type basic_color =
  | Black | Red | Green | Yellow | Blue | Magenta | Cyan | White
```

Now I can say something like:

```ocaml
let r = Red;;
```

And that's the simplest kind of variant. But there are more nuances to this. Let's try to create a variant for shapes:

```ocaml
type point = float * float;;

(*We can pass in addiitional information along with the just the name*)
type shape =
	| Circle of {center : point; radius : float} (*Here we're saying, we're not just talking about Circles in general, there is more data with it*)
	| Rectangle of {lower_left_coord : point; upper_right_coord : point};;

let circle1 = Circle {center=(1.0, 2.0); radius=4.3};;
let rectangle1 = Rectangle {lower_left_coord=(1.0, 2.0);upper_right_coord=(3.0, 4.0)};;

(*Now circle1 and rectangle1 are of type shape*)
```

Okay so all that is good, but what can I do with them? What if I want to compute their center? To do that I need to know whether the shape being passed in is a rectangle or a circle.

```ocaml

let avg p1 p2 = 
	let (x1, y1) = p1 in
	let (x2, y2) = p2 in
	((x1 +. x2)/. 2., (y1 +. y2)/.2.);;

let compute_center (s:shape) = match s with
	| Circle {center;radius} -> center
	| Rectangle {lower_left_coord;upper_right_coord} -> avg lower_left_coord upper_right_coord;;
```

The `Circle` and `Rectangle` there are called **constructors**. We're essentially saying that __see if you can get the center and radius from the Circle constructor or the coords from the Rectangle, depending on what you get compute something__.

Subtle point: if you do `let compute_center s : shape` you are **not** annotating `s` but rather then entire return type. Which will then fuck your code up.

### Nested pattern matching

The code could've been written as this:

```ocaml
let avg x1 x2 = (x1 +. x2) /. 2.;;

let center (s:shape) = match s with
	| Circle {center; radius} -> center
	| Rectangle {lower_left_coord; upper_right_coord} ->
		(*Now here I would have to pattern match again to extract the coordinates*)
		let (x1, y1) = lower_left_coord in
		let (x2, y2) = upper_right_coord in
			(avg x1 y1, avg x2 y2);;
```

That's kinda ugly right, so we can do something better. We can do pattern matching inside the
`Rectangle` match itself:

```ocaml
let center (s:shape) = match s with
	| Circle {center; radius} -> center
	| Rectangle {lower_left_coord = (x1, y1); upper_right_coord = (x2, y2)} ->
			(avg x1 y1, avg x2 y2);;
```

That's kinda cool now! Notice how the order for the match has fliped. That's why its not merely **unpacking** a tuple, its a **pattern match**. They are different things.

Let's add a shape:

```ocaml
type point = float * float;;

type shape =
	| Circle of {center : point; radius : float}
	| Rectangle of {lower_left_coord : point; upper_right_coord : point}
	| Point of point;;

let a = Point (31., 10.);;
```

This is just holding a single point information. Now we'll have to change our patter matching cases we were only matching against `Circle` and `Rectangle`.

```ocaml
let center s = match s with
	| Circle {center; radius} -> center
	| Rectangle {lower_left_coord = (x1, y1); upper_right_coord = (x2, y2)} ->
		(avg x1 y1, avg x2 y2)
	| Point (x, y) -> (x, y);;
```

## Some theory on variants

The syntax:

```ocaml
type t =
	| c1 of t1
	| c2 of t2
	...
	| cn of tn
```

- `c1` is what is called a constructor (we typically write that with a capital letter). It's also called a `tag`.
- `t1` is any additional data that is used to define a constructor more specifically. Its **not** a required field. We say the tag `t1` is carried allowed with `c1`.

- A tag is constant when it carries no data, and non-constant when it carries some data along with it.
- We already how how pattern matching for non-constant tags works, for constant, we simply match against the constructor name only.

## Deciding between a record and a variant

1. `coin`: Which can be a penny, nickle, dime of a quarter -> Better to use a **variant**
2. `student`: Who has a name and an ID number. -> Better to use a **record**
3. `dessert`: Which has a sauce, a creamy component and a crunchy component. -> Better to use a **record**

when we use the conjunction `or` to describe the data you want to store, you should prefer a variant. Because a variant lets you choose one of many. Whereas when you say `and`, you should go for a `record` as it lets you store all that you need in one shot.

> Records (and tuples) are product types

- They are kind of like the cartesian product stuff, they hold "each of" the value.

> Variants are sum types

- They are less familiar, but they hold one of many values.
- This is kind of like taking a union of the values. A variant type **can** represent every single value inside it, but at a time, it does only one.

But they aren't just a normal union, because we **know** from which `set` a value came from. The value is `tagged`. In math, this is called a `tagged union`.

- Variants are also know as `algebraic data types` (ADT) as they allow the combinator of each of types and one of types.

## Modelling pokemons

1. Build the types for the pokemons

```ocaml
type stats = {health: string; attack: int}

type pokemon = 
	| TWater of stats
	| TFire of stats
	| TNormal of stats
```

But this is how the professor did it:

```ocaml
type ptype = Normal | Fire | Water
(*But wrt. point 2, we should really do*)

type ptype = TNormal | TFire | TWater (*This is the ideal way of defining constructors*)
```

2. Define their attack effectiveness

```ocaml
type peff = ENormal | ENotVery | ESuper

(*If you JUST use Normal here, this definition will shadow the first
definition of Normal which was ptype or pokemon, so you don't want that*)
```

3. Create a function which gives the multiplier for damage based on effectiveness

We're saying that a normal attack has a multiplier of 1, not very effective is 1/2 and super effective is 2. (These are **multipliers**)

```ocaml
let mult_of_eff = function
	| ENormal -> 1.
	| ENotVery -> 0.5
	| ESuper -> 2.

(* This is the same as saying:

let mult_of_eff (x:peff) = 
	match x with
	| ENormal -> 1.
	| ENotVery -> 0.5
	| ESuper -> 2.
*)
```

Usually in OCaml we write `of` as in "a_of_b" rather than "b_to_a". I don't know why.

4. Now create the effectiveness function. That is, given two types, determine if the attack will be effective or not.

```ocaml
let eff_of_attack = function
	| (TFire, TNormal) -> ESuper
	| (TWater, TFire) -> ESuper
	| (TNormal, TWater) -> ESuper
	| (TFire, TWater) -> ENotVery
	| (TWater, TNormal) -> ENotVery
	| _ -> ENormal
```

This is just an example encoding, of course we can add more cases here. But now we should be able to pass in a simple **tuple** of types and get whether the attack will be effective or not.

We can do some more advance pattern matching here, by using the `|` (or) operator:

```ocaml
let eff_of_attack = function
	| (TFire, TNormal) | (TWater, TFire) | (TNormal, TWater) -> ESuper
	| (TFire, TWater) | (TWater, TNormal) -> ENotVery
	| _ -> ENormal
```

but what if we don't want to take in a tuple, and rather two separate arguments? We'll have to match against them simultaneously.

```ocaml
let eff_of_attack t1 t2 = match t1, t2 with
	| TFire, TNormal | TWater, TFire	| TNormal, TWater -> ESuper
	| TFire, TWater | TWater, TNormal -> ENotVery
	| _ -> ENormal
```

They look the same (well almost). Read up on something called `currying`.

5. Create a record type for pokemon

```ocaml
type pokemon = {
	name: string;
	health: int;
	ptype : ptype;
}
```

Now we can model an actual pokemon!

```ocaml
let charmander = {
	name = "Charmander";
	health = 10;
	ptype = TFire;
}
```

Crazy.