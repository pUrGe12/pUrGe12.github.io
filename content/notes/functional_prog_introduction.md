+++
title = "Introduction to functional programming in OCaml"
date = 2026-03-29
draft = false

[taxonomies]
categories = ["CS3110", "OCaml"]
tags = ["programming", "Functional-programming"]

[extra]
lang = "en"
+++

# Generics

CS3110 @ Cornell University

> What is functional programming?

1. Where all computations are defined as functions
2. Where every state is immutable

A computation is more like an expression in mathematics, and a state is any variable. No mutable variables in functional programming.

> A language that doesn't affect the way you think about programming, is not worth knowing - Alan J. Perlis

Features of functional programming languages:

1. Garbage collector -> Free used memory when you don't need it
2. Generics -> Type parametrization basically (parametric polymorphism)
3. Higher order functions
4. Type inferences

> How to learn a new language?

1. Learn the syntax
2. Learn the symantics -> What does the program mean and how does the computer understand it
(Ocaml -> Type checking and evaluation rules)
3. idioms -> What are the typical patterns for the language (how to write like a native)
4. libraries -> What have been given, what needs to be imported
5. tools -> Is there a GUI? Utop? REPL? 

> Expressions

- We talk about expressions in OCaml. An expression has:

1. `syntax`: The style
2. `semantics`: The meaning

Semantics can be:

a. `type-checking` also called **static semantics**. Why static? Because this is performed by the compiler before the program exectues. So its static.
b. `evaluations tules` also called **dynamic semantics**, which is what happens when we run the program. So, all value evals, exceptions or infinite loops happen here.

- A value is an expression that doesn't need any further evaluations. Something which is DONE.

> Reading OCaml top level (Utop) go from right to left! Damn, that actually makes more sense.

- OCaml does type inference (so its not AS much of a pain in the ass as C/C++) but its `type strict`!

```ocaml
let func x = x ^ x;;
```

In this case, the ocaml compiler will **infer** that the return type for this program is a "string" and hence the input type is also a "string". We didn't write it that way!

What about

```ocaml
let func x = x;;
```

Here the compiler has no idea what the type of `x` and hence the return type is, so its gonna say, put anything. All types work in this case.

- OCaml does let you annotate types by yourself. You can do `expression : type` like:

```ocaml
let func (x:float) (y:float) = x +. y;;
```

Now we have explicitly said that `x` and `y` must be floats. Note that this is not a **type casting** like in python, THIS IS AN ADDITIONAL CONSTRAINT. The compiler will `verify` if the type I am trying to assign to an identifier is correct or not!

## Conditions

- Simple if statments go like `if ... then ... else`. So you can write something like:

```ocaml
if "batman" > "superman" then 0 else 1;;
```

BUT at the same time you **cannot** write:

```ocaml
if "batman" > "superman" then 0 else "boo";;
```

This is because both the return types for an expression must be the same. This is a necessity in OCaml! So, this is very much unlike python!

- Syntax: `if e1 then e2 else e3`
- Semantics:

> if e1 evaluates to true and e2 evaluates to v, then the entire expression must evaluate to v

and 

> if e1 evaluates to false and e3 evaluates to v', then the entire expression must evaluate to v'

- Type checking rules:

> if e1 has type bool (which it must) and e2 has type t, and e3 also has type t, then the expression has type t.

and

> e2 and e3 must have the same types t

We can write the above checks in the notation with the following mapping:

- `==>` -> "evaluates to"
- `:` -> "has type"

- Semantics:

> if e1 ==> true and e2 ==> v, then (if e1 then e2 else e3) ==> v

and

> if e1:bool and e2:t and e3:t then (if e1 then e2 else e3):t

That's awesome!

## Let definitions

First lets talk about a let definition. They are not "expressions" or "values" per se. Completely different syntax class.

A definition, **gives a name to a value**. Definitions do "contain" expressions.

- syntax: `let x = e` where `x` is the identifier and `e` is any expression.
- semantics:

> let x = e means, evaluate e to v, then bind v to x

Think of this as a memory location named `x`, which now contains `v`. And this is "immutable".

Note: a let definition is by itself NOT AN EXPRESSION. So you cannot use it as a subexpression anywhere in OCaml.

## Let expressions

But we do have let expressions, which are not definitions but are **syntactically** expressions.

```ocaml
let a = 0 in a;; (*This evaluates to 0*)
let a = 1 in a * 2;; (*This evaluates to 2*)
```

This looks like a substitution now! These let expressions are not definitions, as in the "scope" where `a` is defined has changed. In both these cases, `a` is only defined inside the expression that follows its definition after `in`!

So if we try to see what `a` is outside of that expression, its not defined yet so its an unbound value.

what about:

```ocaml
let e = 3 in (let e = 4 in e);; (*we get 4 with a warning*)
```

That warning is telling us that we have an unused variable! That's pretty cause as we said, there is no mutation for a "variable" once it is bound, and we can see that in action now. We tried to mutate the variable using the same "identifier" but we ended up with `2 different identifiers` of which ocaml is complaining that we used only the last one.

## Mutations and scope

What happens when we write:

```ocaml
let x = 1;;
let x = 2;;
x;;
```

We get 2. Does this mean we have mutated our variable x which we said we can't ever do in functional programming? Actually no...

The above is equivalent to saying:

```ocaml
let x = 1 in
let x = 2 in
x
```

and when we evaluate the inner expression we get `x` bound to 2, hence `x` is 2. But what happens to the first `x`? Its an **unused** variable! Yeahhh

We basically allocated 2 memory locations, called it x, but they are different memory locations. And we used only one.

But if that is the case, can I **go back to the first x defintion and get 1 from that memory location**? Uhh.. in the top level, you can't, but in normal files, yes def. We'll see.

## Anonymous functions

We define anonymous functions using the `fun` keyword. This goes like:

```ocaml
fun x -> x+1;;
```

We can use it as:

```ocaml
(fun x->x*.2) 2.4;; (*evaluates to 4.8*)
```
These are the inline lambda functions that we use in other languages too like python!

All these anonymous functions are values. This means, functions can take functions as arguments and even spit out functions as the return value. Neat.

Another thing is that, in general `fun x1 x2 ... xn -> e` does **NOT** evaluate `e` at runtime, UNLESS the function is `applied` to an argument. Why? Because its a value. Remember.

`Semantics`: Application of `fun x1 x2 ... xn -> e` goes as follows:

> fun ==> v0, x1 ==> v1, x2 ==> v2 ... xn ==> vn. Now v0 must be a function say, `fun x1 .. xn -> e`, now in THIS function, we can substitute the values of vi for xi and evalute an e. Then e ==> v. And v is the final output.

Pretty interesting way of putting this. Intutively it may make sense much easier than this but yep. This is the formal way of how this expression evaluation works semantically.

```ocaml
(fun x -> x+1) (3+4);;
```

First we evaluate all subexpressions so we get

```ocaml
fun x -> x+1;; (*subexpression e0==>v0*)
5;; (*subexpression (3+4) ==> 5, x1 = (3+4), v1 = 5*)
```

Then we apply the function `v0` to the arguments by substituting `xi` for `vi`

```ocaml
(fun x->x+1) (5);; (*This gives us a 6*)
```

Why is `v0` the same function? Because an anonymous function is already a value. AHHH. Makes sense.

## Giving names to functions

We can give names to anonymous functions (that sounds kinda dumb but we can!):

```ocaml
let inc = fun x -> x + 1;;
```

And we can apply it normally:

```ocaml
inc 2;; (*gives 3*)
```

But there is some **syntactical sugar** here. We can just write the same function as:

```ocaml
let inc x = x+1;;
```

This is understood by the compiler as a function and it makes the code more readable (plus we aren't doing the dumb thing of giving a name to an anonymous function).

Note that they share the same semantics. For example, this as well is semantically similar but syntactically different:

```ocaml
(fun x -> x*2) 2;;
let x = 2 in x * 2;;
```

Because recall that an anonymous function is a value only!

## Recursive functions

```ocaml
let rec fact x =
	match x with
	| 0 -> 1
	| x -> x * fact (x-1)
```

We'll see about the match syntax soon. But remember to explicitly add the rec keyword for the compiler!