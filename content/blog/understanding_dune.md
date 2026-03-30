+++
title = "Understanding the Dune build system"
date = 2026-03-29
draft = false

[taxonomies]
categories = ["OCaml", "build-system"]
tags = ["functional-programming", "blog"]

[extra]
lang = "en"
+++

## Introduction

This is [dune](http://github.com/ocaml/dune/). It is a build-system for OCaml written by Jane Street and now a part of the OCaml community. This blog post is to do a deep dive into Dune and understand two things:

1. What does it do?
2. How does it work?

This was written in a span of a few days with a lot of research time (I actually lost track of how much time). So, hope it helps!

## What is dune

`Dune` does for OCaml what `Make` and `Makefile` does for C (with a few important differences which will become apparent), albeit at a much higher level. The best place to start is always the [manual](https://dune.readthedocs.io/en/latest/). I will be summarizing some of the more important aspects below but if you want to take a read, do so.

The most important line:

>When using Dune, you give very little, high-level information to the build system, which in turn takes care of all the low-level details from the compilation of your libraries, executables, and documentation to the installation, setting up of tests, and setting up development tools such as Merlin, etc.

So basically when you make an OCaml project, it typically follows this structure:

```
project_name/
├── test
│   └── test_project_name.ml
├── lib
│   └── lib.ml
│   └── lib.mli
├── bin
│   └── main.ml
└── project_name.opam
```

You write your main source code inside `bin/`, and libraries inside `lib/`, but of-course this is not mandated! You are free to do whatever you like, BUT think about how you would then compile your `main.ml` code.

```sh
# First compile your libraries
ocamlopt -c lib/lib.mli # This produces lib/lib.cmi
ocamlopt -c lib/lib.ml # This produces lib/lib.cmx and lib/lib.o
# Then compile main
ocamlopt -I lib lib/lib.cmx bin/main.ml -o main
```

or you can do it in one step with:

```sh
ocamlopt -I lib lib/lib.mli lib/lib.ml bin/main.ml -o main
```

But you see the problem here? If you have more libraries, more inter-dependencies, then you're cooked because you must not mess up the compile order! So, that's where dune comes in. If we used `dune`, this is how the structure would look like:

```
project_name/
├── dune-project
├── test
│   ├── dune
│   └── test_project_name.ml
├── lib
│   └── dune
├── bin
│   ├── dune
│   └── main.ml
└── project_name.opam
```

Then assuming that you have the **right** stuff inside the `dune` files in `lib/` and `bin/`, you can simply do:

```sh
dune build  # Build
dune exec ./bin/main.exe # Run
dune runtest # Run tests
```

And that's all it takes. Now the question is, how do we know what to put inside the `dune` files in each directory? Let's see about that.


## How dune does what it does (high-level)

## How dune does what it does (slight-lower-level)