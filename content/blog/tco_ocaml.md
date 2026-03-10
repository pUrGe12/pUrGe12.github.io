+++
title = "TCO in recursive functions in OCaml in assembly, an analysis"
date = 2026-03-09
draft = false

[taxonomies]
categories = ["OCaml", "compilers"]
tags = ["functional-programming", "blog", "assembly"]

[extra]
lang = "en"
+++

# Introduction
There is a class of optimisations called the `Tail-call optimisations`. These come into picture usually for recursive functions (though they can be defined for general statements as well but then the **optimisation** has no meaning. See the [wikipedia page](https://en.wikipedia.org/wiki/Tail_call#Syntactic_form)) and tail-recursive functions are a special case of the same. To understand what `tail-calls` are let's look at an example. 

Consider the following definitions of the **factorial of a number**:

### Definition 1: non-tail recursive
```ocaml
let rec factorial ~n:n = 
	match n with
	| 0 -> 1
	| n -> n*factorial ~n:(n-1)
```

or

```ocaml
let rec fib n =
	match n with
	| 1 -> 1
	| 2 -> 1
	| n -> fib (n-1) + fib (n-2)
```

### Definition 2: tail-recursive

```ocaml
let fact ~n:n =
  let rec aux n acc =
    if n = 0 then acc
    else aux (n - 1) (n * acc)
  in
  aux n 1
```

or

```ocaml
let fib n =
  let rec aux n a b =
    if n = 0 then a
    else aux (n - 1) b (a + b)
  in
  aux n 1 1
```

Both of them perform the same operation, in-fact they look like they're doing the exact same thing in code as well, but there is a subtle difference:

> The second definition ensures that the recursion is in the tail-position!

## What is the tail-position?

From the book `real world OCaml`: Let's think about the situation where one function (the caller) invokes another (the callee). The invocation is considered a tail call **when the caller doesn't do anything with the value returned by the callee** except to return it.

In the second example, the function `fact` is by itself not recursive, but it invokes another function called `aux` which is. Now the `fact` function simply returns the output given by aux doesn't it! So, this makes it a `tail-call`.

Some functions are deliberately made a little messier as in the second case to allow the compiler to perform the tail-call optimisations. This messiness comes from the use of the `accumulator`, this holds the value of individual calls in a **single stack frame** (we'll discuss that in a few minutes) and allows the main function to return just the output of inner recursive function.

So what is a tail-call `optimisation`?

## Tail call optimisation

To understand this in a deeper level, let's analyze the assembly output for the non-tail recursive case. For compiling, save the first definition in a file named `main.ml`, then run:

```sh
# Assuming main.ml has the following code:
# let rec fib n =
# 	match n with
# 	| 1 -> 1
# 	| 2 -> 1
# 	| n -> fib (n-1) + fib (n-2);;

# let a = fib 10;;
# print_endline @@ string_of_int a;;

ocamlopt -o main main.ml -g # -g -> Ensure that symbols are present for debugging
```
Then do an objdump and save it to a file for analysis:
```sh
objdump -d main > objdump.txt
```

This is the `main` and the `_start` section:

```x86asm

0000000000018890 <main>:
   18890:	f3 0f 1e fa          	endbr64 
   18894:	50                   	push   %rax
   18895:	58                   	pop    %rax
   18896:	48 89 f7             	mov    %rsi,%rdi
   18899:	48 83 ec 08          	sub    $0x8,%rsp
   1889d:	e8 de b1 02 00       	call   43a80 <caml_main>
   188a2:	31 ff                	xor    %edi,%edi
   188a4:	e8 17 64 02 00       	call   3ecc0 <caml_do_exit>
   188a9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000000188b0 <_start>:
   188b0:	f3 0f 1e fa          	endbr64 
   188b4:	31 ed                	xor    %ebp,%ebp
   188b6:	49 89 d1             	mov    %rdx,%r9
   188b9:	5e                   	pop    %rsi
   188ba:	48 89 e2             	mov    %rsp,%rdx
   188bd:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
   188c1:	50                   	push   %rax
   188c2:	54                   	push   %rsp
   188c3:	45 31 c0             	xor    %r8d,%r8d
   188c6:	31 c9                	xor    %ecx,%ecx
   188c8:	48 8d 3d c1 ff ff ff 	lea    -0x3f(%rip),%rdi        # 18890 <main>
   188cf:	ff 15 23 87 04 00    	call   *0x48723(%rip)        # 60ff8 <__libc_start_main@GLIBC_2.34>
   188d5:	f4                   	hlt    
   188d6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   188dd:	00 00 00 
```

A few glossary terms:

- `caml_main`: This is a C runtime interface function for OCaml. The call to **caml_main** initializes the OCaml runtime system, loads the bytecode (in the case of the bytecode compiler), and executes the initialization code of the OCaml program. Read the [intfc documentation](https://ocaml.org/manual/5.4/intfc.html) for details.

- `caml_do_exit`: This is another C runtime interface function. They are actually typically used like this:

```c
#include <stdio.h>

#define CAML_INTERNALS
#include "caml/misc.h"
#include "caml/mlvalues.h"
#include "caml/sys.h"
#include "caml/callback.h"

/* This is the new entry point */
int main(int argc, char_os **argv)
{
    /* Here, we just print a statement */
    printf("Doing stuff before calling the OCaml runtime\n");

    /* Before calling the OCaml runtime */
    caml_main(argv);
    caml_do_exit(0);
    return 0;
}
```

You might wonder why we're even seeing these in the assembly if we simply compiled some OCaml source code and never touched C. Few points:

1. OCaml is a high-level language after all, which means it cannot just directly talk to the OS like that. It uses the standard `_start` entrypoint and `main` definitions (like in C) to match the OS specification.

2. It uses `libc` (see the libc call in `_start`) to define memory allocation, syscalls and more.

3. The function we call forth in libc is `__libc_start_main` which basically initializes the C runtime environment and then calls the `main` function.

This should answer your question. It calls `caml_main` in the actual `main` definition because it needs to initialize the OCaml garbage collector, the heap and all.

All this happens **before** our code is even touched. So, where is our code? If you scroll a little deeper you'll see this bit:

```x86asm

0000000000018dc0 <camlMain.fib_274>:
   18dc0:	4c 8d 94 24 b0 fe ff 	lea    -0x150(%rsp),%r10
   18dc7:	ff 
   18dc8:	4d 3b 56 28          	cmp    0x28(%r14),%r10
   ...
   ...
   18e23:	eb a9                	jmp    18dce <camlMain.fib_274+0xe>
   18e25:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   18e2c:	00 00 00 00 

0000000000018e30 <camlMain.entry>:
   18e30:	4c 8d 94 24 c0 fe ff 	lea    -0x140(%rsp),%r10
   ...
   ...
   18e9f:	e8 4c ac 02 00       	call   43af0 <caml_call_realloc_stack>
   18ea4:	41 5a                	pop    %r10
   18ea6:	eb 96                	jmp    18e3e <camlMain.entry+0xe>
```

The actual code that we __wrote__ is inside `camlMain.entry` and our function lives in `camlMain.fib_274`. This is just OCaml's way of keeping a nice and separate namespace. Now, let's go over the code in `camlMain.entry`

```x86asm
   18e30:	4c 8d 94 24 c0 fe ff 	lea    -0x140(%rsp),%r10
   18e37:	ff 
   18e38:	4d 3b 56 28          	cmp    0x28(%r14),%r10
   18e3c:	72 5f                	jb     18e9d <camlMain.entry+0x6d>
   18e3e:	48 8d 35 63 8d 04 00 	lea    0x48d63(%rip),%rsi        # 61ba8 <camlMain.1>
   18e45:	48 8d 3d 74 8d 04 00 	lea    0x48d74(%rip),%rdi        # 61bc0 <camlMain>
   18e4c:	48 89 e3             	mov    %rsp,%rbx
   18e4f:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e53:	e8 18 94 01 00       	call   32270 <caml_initialize>
   18e58:	48 89 dc             	mov    %rbx,%rsp
   18e5b:	b8 15 00 00 00       	mov    $0x15,%eax
   18e60:	e8 5b ff ff ff       	call   18dc0 <camlMain.fib_274>
   18e65:	48 8d 3d 54 8d 04 00 	lea    0x48d54(%rip),%rdi        # 61bc0 <camlMain>
   18e6c:	48 83 c7 08          	add    $0x8,%rdi
   18e70:	48 89 c6             	mov    %rax,%rsi
   18e73:	48 89 e3             	mov    %rsp,%rbx
   18e76:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e7a:	e8 f1 93 01 00       	call   32270 <caml_initialize>
   18e7f:	48 89 dc             	mov    %rbx,%rsp
   18e82:	48 8d 05 37 8d 04 00 	lea    0x48d37(%rip),%rax        # 61bc0 <camlMain>
   18e89:	48 8b 40 08          	mov    0x8(%rax),%rax
   18e8d:	e8 5e 1a 00 00       	call   1a8f0 <camlStdlib.string_of_int_175>
   18e92:	e8 d9 28 00 00       	call   1b770 <camlStdlib.print_endline_369>
   18e97:	b8 01 00 00 00       	mov    $0x1,%eax
   18e9c:	c3                   	ret    
   18e9d:	6a 21                	push   $0x21
   18e9f:	e8 4c ac 02 00       	call   43af0 <caml_call_realloc_stack>
   18ea4:	41 5a                	pop    %r10
   18ea6:	eb 96                	jmp    18e3e <camlMain.entry+0xe>
```

The lines to focus on are:

```x86asm
   18e5b:	b8 15 00 00 00       	mov    $0x15,%eax
   18e60:	e8 5b ff ff ff       	call   18dc0 <camlMain.fib_274>
```

We're moving **0x15** (21 in decimal) to the first 4 bytes of `rax` and calling `camlMain.fib_274` on that. I know you are burning to ask why 21 and not 10. We'll get into that, but first, let's trace the logic in `camlMain.fib_274`:

```x86asm
0000000000018dc0 <camlMain.fib_274>:
   18dc0:	4c 8d 94 24 b0 fe ff 	lea    -0x150(%rsp),%r10
   18dc7:	ff 
   18dc8:	4d 3b 56 28          	cmp    0x28(%r14),%r10
   18dcc:	72 4c                	jb     18e1a <camlMain.fib_274+0x5a>
   18dce:	48 83 ec 10          	sub    $0x10,%rsp
   18dd2:	48 89 c3             	mov    %rax,%rbx
   18dd5:	48 83 c3 fe          	add    $0xfffffffffffffffe,%rbx
   18dd9:	48 83 fb 03          	cmp    $0x3,%rbx
   18ddd:	76 31                	jbe    18e10 <camlMain.fib_274+0x50>
   18ddf:	48 89 04 24          	mov    %rax,(%rsp)
   18de3:	48 83 c0 fc          	add    $0xfffffffffffffffc,%rax
   18de7:	e8 d4 ff ff ff       	call   18dc0 <camlMain.fib_274>
   18dec:	48 89 44 24 08       	mov    %rax,0x8(%rsp)
   18df1:	48 8b 04 24          	mov    (%rsp),%rax
   18df5:	48 83 c0 fe          	add    $0xfffffffffffffffe,%rax
   18df9:	e8 c2 ff ff ff       	call   18dc0 <camlMain.fib_274>
   18dfe:	48 8b 5c 24 08       	mov    0x8(%rsp),%rbx
   18e03:	48 01 d8             	add    %rbx,%rax
   18e06:	48 ff c8             	dec    %rax
   18e09:	48 83 c4 10          	add    $0x10,%rsp
   18e0d:	c3                   	ret    
   18e0e:	66 90                	xchg   %ax,%ax
   18e10:	b8 03 00 00 00       	mov    $0x3,%eax
   18e15:	48 83 c4 10          	add    $0x10,%rsp
   18e19:	c3                   	ret    
   18e1a:	6a 23                	push   $0x23
   18e1c:	e8 cf ac 02 00       	call   43af0 <caml_call_realloc_stack>
   18e21:	41 5a                	pop    %r10
   18e23:	eb a9                	jmp    18dce <camlMain.fib_274+0xe>
   18e25:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   18e2c:	00 00 00 00 
```

What are we looking for here:

1. Convince yourself that this is a recursive function. Look at instruction `18e23`, this is the recursive part. 

2. If you look at the code leading up to the recursive bit:

```x86asm
   18dfe:	48 8b 5c 24 08       	mov    0x8(%rsp),%rbx
   18e03:	48 01 d8             	add    %rbx,%rax
   18e06:	48 ff c8             	dec    %rax
   18e09:	48 83 c4 10          	add    $0x10,%rsp
   18e0d:	c3                   	ret    
   18e0e:	66 90                	xchg   %ax,%ax
   18e10:	b8 03 00 00 00       	mov    $0x3,%eax
   18e15:	48 83 c4 10          	add    $0x10,%rsp
   18e19:	c3                   	ret    
```

These are our base cases. Again you'll be screaming that the numbers don't match. We'll get to that! How am I saying that this is a base case?

```x86asm
   18dd9:	48 83 fb 03          	cmp    $0x3,%rbx
   18ddd:	76 31                	jbe    18e10 <camlMain.fib_274+0x50>
```

Because our smart compiler had figured out that if we're talking about numbers less than 3 (that is, 1 or 2), then we can simply jump to `18e0e`, even though we explictly told it to handle 1 and 2.

3. Then look at the function calls itself:

```x86asm
   18ddf:	48 89 04 24          	mov    %rax,(%rsp)
   18de3:	48 83 c0 fc          	add    $0xfffffffffffffffc,%rax
   18de7:	e8 d4 ff ff ff       	call   18dc0 <camlMain.fib_274>
   18dec:	48 89 44 24 08       	mov    %rax,0x8(%rsp)
   18df1:	48 8b 04 24          	mov    (%rsp),%rax
   18df5:	48 83 c0 fe          	add    $0xfffffffffffffffe,%rax
   18df9:	e8 c2 ff ff ff       	call   18dc0 <camlMain.fib_274>
```

- The numbers `0xfffffffffffffffc` and `0xfffffffffffffffe` probably don't make sense to you (I know no numbers are making sense in this assembly and that's the magic!) but this is what is doing **(n-1)** and **(n-2)** in our code.

- Notice that we're calling the function twice, just like in the code, locations `18de7` and `18df5`.

---

Now we're at the heart of what tail-call optimisations are. This function we used was **not** tail-recursive, and hence the OCaml compiler couldn't optimize it using tail-call optimisation. What this means is:

1. Each function call to the recursive function is can actual `call` opcode in assembly.
2. A `call` instruction is operationally very heavy. It needs to remember a lot of things, intialize a bunch of pointers in memory etc.
3. The program needs to save every frame (every `fib i` operation it performs for `i = 1->n`) in the stack. If the value of `n` is large, this will 100% lead to a stack overflow!

So, a non-tail-recursive function is a curse because its slow, can't be optimized and may lead to memory overflows! Before we go ahead, let's think about what optmisation even means here!

> Tail-call optimisation is when a tail-recursive function is replaced by a loop in assembly.

A loop doesn't need to allocate a frame for each value it computes, its faster to `jmp` than `call` because of less overhead, and hence, its a beautiful optimisation!

Let's look at the second case, compile the second implementation in the same manner as the first one. Let's observe the `camlMain.fib` implementation in assembly:

```x86asm
0000000000018dc0 <camlMain.fibonacci_274>:
   18dc0:	4d 3b 3e             	cmp    (%r14),%r15
   18dc3:	76 0f                	jbe    18dd4 <camlMain.fibonacci_274+0x14>
   18dc5:	bf 03 00 00 00       	mov    $0x3,%edi
   18dca:	bb 03 00 00 00       	mov    $0x3,%ebx
   18dcf:	e9 0c 00 00 00       	jmp    18de0 <camlMain.aux_277>
   18dd4:	e8 93 af 02 00       	call   43d6c <caml_call_gc>
   18dd9:	eb ea                	jmp    18dc5 <camlMain.fibonacci_274+0x5>
   18ddb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000018de0 <camlMain.aux_277>:
   18de0:	4d 3b 3e             	cmp    (%r14),%r15
   18de3:	76 1c                	jbe    18e01 <camlMain.aux_277+0x21>
   18de5:	48 83 f8 03          	cmp    $0x3,%rax
   18de9:	75 05                	jne    18df0 <camlMain.aux_277+0x10>
   18deb:	48 89 d8             	mov    %rbx,%rax
   18dee:	c3                   	ret    
   18def:	90                   	nop
   18df0:	48 8d 74 3b ff       	lea    -0x1(%rbx,%rdi,1),%rsi
   18df5:	48 83 c0 fe          	add    $0xfffffffffffffffe,%rax
   18df9:	48 89 fb             	mov    %rdi,%rbx
   18dfc:	48 89 f7             	mov    %rsi,%rdi
   18dff:	eb df                	jmp    18de0 <camlMain.aux_277>
   18e01:	e8 66 af 02 00       	call   43d6c <caml_call_gc>
   18e06:	eb dd                	jmp    18de5 <camlMain.aux_277+0x5>
   18e08:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   18e0f:	00 
```

Notice the magic here! No, `call` instructions, only conditional jumps. If you just take a look at the assembly, you'll never realize that this was actually a recursive function. Which is the point. `Tail-call optimisations` covert a recursive function to its fastest counterpart which is a loop.

1. This function doesn't allocate a new frame in the stack for each value computed, so we don't have memory issues anymore.

2. We went from **not** being able to compute the `100th` fibonnaci number (true, try definition 1 for the 100th number!) to computing `10^6th` fibonnaci number in a matter of seconds, **without memoization** of dynamic programming!

This it the compiler magic!

I will not go into details of **exactly** what is happening in the above assembly, because there are so many more optimisations there as well and some beautiful math (which I am still learning).

## What those weird numbers mean

These numbers are specially tagged, they are called `tagged integers`. OCaml uses these tagged versions to help the garbage collector. How exactly? I think I will move this to a separate post. Checkout [this blog](https://purge12.github.io/blog/ocaml_compiler_tagged_integers).

## Ending note

Functional-programming languages love implementing recursive functions, so its very important that any such function which you write, is tail-optimised. The OCaml compiler by itself won't optimise it for you (we already saw that, a non-tail recursive function, stays that way), because to do that, it would have to change the logic of the code. 

You can still have the compiler throw a warning using the `[@tailcall]` attribute. See [this manual](https://github.com/ocaml/ocaml/blob/a0ab87686082bc2ca4bebac04ce9315fe53eff88/manual/src/refman/extensions/attributes.etex#L246) in OCaml's repo.

# Thanks for reading!