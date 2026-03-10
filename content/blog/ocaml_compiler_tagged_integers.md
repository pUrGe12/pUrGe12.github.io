+++
title = "Tagged integer representation in OCaml"
date = 2026-03-09
draft = false

[taxonomies]
categories = ["OCaml", "compilers"]
tags = ["functional-programming", "blog", "assembly"]

[extra]
lang = "en"
+++

OCaml uses what is called `tagged integers` for optimised arithmetic but the reasons extend beyond that. For OCaml's actual documentation, refer [this post](https://ocaml.org/docs/memory-representation), or you can always read `real world OCaml`.

## Understanding memory allocation

In OCaml, memory allocation happens via the `let` binding and it uses a uniform memory representation in which every OCaml variable is stored as a **value**. Let's look at that in action.

This is a little more involved and I am not there yet. Let's take this slow.