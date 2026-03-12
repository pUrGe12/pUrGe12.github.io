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

Let's first understand how ocaml (and other ML-based languages) store data in memory.

## Boxed vs. Unboxed values

From the [OCaml documentation](https://ocaml.org/docs/memory-representation): "Wrapping primitive types (such as integers) inside another data structure that records extra metadata about the value is known as boxing."

From the [Jane Street documentation](https://blog.janestreet.com/what-is-gained-and-lost-with-63-bit-integers/): "If a record’s field is float, record’s data will actually contain the pointer to the float data. The only exceptions are records with only floats and float arrays, whose data instead of pointers contain the values of floats. This representation is called `unboxed`.""

The idea behind boxxed and unboxxed representations is to help the Garbage Collector do its job, but this comes with an extra step to access that boxxed value.

## Why are integer values not boxxed?

Values of type int are never stored as header and data (boxed). This is because we don't need this extra overhead in case of integers, the GC can very easily differentiate between integers and others which look most like it, pointers.

This is because OCaml is storing an integer `x` as `(x << 1) | 1` which translates to an integer value of `2x+1`, meanwhile pointers are always ensured to be word-aligned.

## What does word-aligned mean?!

A `word` is 8 bytes for 64bit machines and 4 bytes for 32 bit machines. When the hardware tries to access the memory, it will do it in contigous sizes of 8 bytes each. So, you can imagine a sliding window for example, with a length of 8, going over the first 8 bytes, then it directly goes over the next 8 bytes and so on.

Word-alignment then means that each contigous memory space is occupied by a single value only. Does that make sense?

So if pointers are always stored word aligned, their values must be multiples of 8 (for a 64 bit machine) i.e. they point to contigous memory addresses. So, 0-7 bytes is one pointer, then 8-15 bytes is the next pointer etc. These bytes of course, can be at a specific offset where the hardware is storing stuff, but they will all be multiples of 8.

Now if you were to actually go ahead and print the value of a pointer, you'll see that it MUST end with the last 3 bits as 0. Let's go ahead and do that in OCaml, we'll assign a heap object using `let` (a good documentation for what this means is [here](https://ocaml.org/docs/memory-representation)), and then inspect the value at runtime.

```ocaml
let () =
  (* allocate a heap object using ref *)
  let x = ref 42 in
  (* reinterpret the pointer as an int *)
  let addr : int = Obj.magic x in

  Printf.printf "Pointer value: %d\n" addr;
  Printf.printf "Pointer hex: 0x%x\n" addr;
  Printf.printf "addr mod 8 = %d\n" (addr mod 8);
  Printf.printf "last 3 bits = %d\n" (addr land 0b111) (* land is the bitwise and operator*)
```

Notice how we have to first reinterpret the pointer as an integer? This is purely for "printing" purposes and a way to circumvent OCaml's strict type checking. There is no "default type" so to speak of a pointer, and you cannot just `printf` it. So, we reinterpret.

If you run this, you'll see something similar to:

```
Pointer value: 65189632277872
Pointer hex: 0x3b4a24dffd70
addr mod 8 = 0
last 3 bits = 0
```

And this will always be true for any pointer. You might ask, why is that? The answer's right there. The address is a multiple of 8,

```ocaml
8 = 0x1000
16 = 0x10000
24 = 0x11000
...
```

All multiples of 8 always end with LS 3 bits as 0.

## How does the specific integer representation help?

Since every integer is stored as `x<<1 | 1` where `<<` is a left bit shift and `|` is the OR operator, we ensure that any integer in memory will be stored with its LSB set. Let's see that in real time as well. The problem is we cannot directly see the immediate values (as OCaml won't expose that), so we'll have to dive into assembly now.

I have compiled the simple program which allocates an integer in the heap:

```ocaml
let double_func x = 
  match x with
  | 0 -> 0
  | x -> x * 2

let a = double_func 4
print_endline @@ string_of_int a
```

Compiled with `ocamlopt` and then dumped:
```sh
ocamlopt -o main main.ml -g # -g adds debugging information
objdump -d main > objdump.txt
```

`caml_main` is the OCaml entrypoint as opposed to `_start` and `main` (below) which are artifacts of the C runtime:

```x86asm
00000000000188a0 <main>:
   188a0:	f3 0f 1e fa          	endbr64 
   188a4:	50                   	push   %rax
   188a5:	58                   	pop    %rax
   188a6:	48 89 f7             	mov    %rsi,%rdi
   188a9:	48 83 ec 08          	sub    $0x8,%rsp
   188ad:	e8 ae b2 02 00       	call   43b60 <caml_main>
   188b2:	31 ff                	xor    %edi,%edi
   188b4:	e8 e7 64 02 00       	call   3eda0 <caml_do_exit>
   188b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000000188c0 <_start>:
   188c0:	f3 0f 1e fa          	endbr64 
   188c4:	31 ed                	xor    %ebp,%ebp
   188c6:	49 89 d1             	mov    %rdx,%r9
   188c9:	5e                   	pop    %rsi
   188ca:	48 89 e2             	mov    %rsp,%rdx
   188cd:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
   188d1:	50                   	push   %rax
   188d2:	54                   	push   %rsp
   188d3:	45 31 c0             	xor    %r8d,%r8d
   188d6:	31 c9                	xor    %ecx,%ecx
   188d8:	48 8d 3d c1 ff ff ff 	lea    -0x3f(%rip),%rdi        # 188a0 <main>
   188df:	ff 15 fb 96 04 00    	call   *0x496fb(%rip)        # 61fe0 <__libc_start_main@GLIBC_2.34>
   188e5:	f4                   	hlt    
   188e6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   188ed:	00 00 00 
```

We can just jump to the ocaml entry and ignore everything else:

```x86asm
0000000000018df0 <camlMain.entry>:
   18df0:	4c 8d 94 24 c0 fe ff 	lea    -0x140(%rsp),%r10
   18df7:	ff 
   18df8:	4d 3b 56 28          	cmp    0x28(%r14),%r10
   18dfc:	72 51                	jb     18e4f <camlMain.entry+0x5f>
   18dfe:	48 8d 35 a3 ad 04 00 	lea    0x4ada3(%rip),%rsi        # 63ba8 <camlMain.1>
   18e05:	48 8d 3d b4 ad 04 00 	lea    0x4adb4(%rip),%rdi        # 63bc0 <camlMain>
   18e0c:	48 89 e3             	mov    %rsp,%rbx
   18e0f:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e13:	e8 98 95 01 00       	call   323b0 <caml_initialize>
   18e18:	48 89 dc             	mov    %rbx,%rsp
   18e1b:	be 11 00 00 00       	mov    $0x11,%esi
   18e20:	48 8d 3d 99 ad 04 00 	lea    0x4ad99(%rip),%rdi        # 63bc0 <camlMain>
   18e27:	48 83 c7 08          	add    $0x8,%rdi
   18e2b:	48 89 e3             	mov    %rsp,%rbx
   18e2e:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e32:	e8 79 95 01 00       	call   323b0 <caml_initialize>
   18e37:	48 89 dc             	mov    %rbx,%rsp
   18e3a:	b8 11 00 00 00       	mov    $0x11,%eax
   18e3f:	e8 5c 1a 00 00       	call   1a8a0 <camlStdlib.string_of_int_175>
   18e44:	e8 d7 28 00 00       	call   1b720 <camlStdlib.print_endline_369>
   18e49:	b8 01 00 00 00       	mov    $0x1,%eax
   18e4e:	c3                   	ret    
   18e4f:	6a 21                	push   $0x21
   18e51:	e8 da ad 02 00       	call   43c30 <caml_call_realloc_stack>
   18e56:	41 5a                	pop    %r10
   18e58:	eb a4                	jmp    18dfe <camlMain.entry+0xe>
```

Look at these lines:

```x86asm
   18e3a:	b8 11 00 00 00       	mov    $0x11,%eax
   18e3f:	e8 5c 1a 00 00       	call   1a8a0 <camlStdlib.string_of_int_175>
   18e44:	e8 d7 28 00 00       	call   1b720 <camlStdlib.print_endline_369>
```

We're calling the `string_of_int` function to the value in the bottom 32 bits of `RAX` which means on `0x11` and that translates to the decimal value of `17`, and according to the assembly, that's what we're printing!

But, you would expect `8` to be printed right? And when you run it, you will see `8` being printed. And, the magic is:

```
0x11 (17) = 8 << 1 | 1
```

## How does it do math then?

Since we are losing one bit precision AND changing the value, how does the compiler even do normal math? Turns out, that this representation allows the compiler to optimize these calculations even better. Let's take a look at addition.

### Addition

```ocaml
let add x y = x+y;;

print_endline @@ string_of_int @@ add 4 5
```

Compiling it and seeing the assembly:

```x86asm
0000000000018dd0 <camlMain.add_274>:
   18dd0:	48 8d 44 18 ff       	lea    -0x1(%rax,%rbx,1),%rax
   18dd5:	c3                   	ret    
   18dd6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   18ddd:	00 00 00 
```

The addition function is not running any opcode for `add`! If you want to compare this to a normal C function that does addition:

```x86asm

0000000000001149 <add>:
    1149:	f3 0f 1e fa          	endbr64 
    114d:	55                   	push   %rbp
    114e:	48 89 e5             	mov    %rsp,%rbp
    1151:	89 7d fc             	mov    %edi,-0x4(%rbp)
    1154:	89 75 f8             	mov    %esi,-0x8(%rbp)
    1157:	8b 55 fc             	mov    -0x4(%rbp),%edx
    115a:	8b 45 f8             	mov    -0x8(%rbp),%eax
    115d:	01 d0                	add    %edx,%eax
    115f:	5d                   	pop    %rbp
    1160:	c3                   	ret    


<main>: // Some relevant parts from main
    116d:	be 05 00 00 00       	mov    $0x5,%esi
    1172:	bf 04 00 00 00       	mov    $0x4,%edi
    1177:	b8 00 00 00 00       	mov    $0x0,%eax
    117c:	e8 c8 ff ff ff       	call   1149 <add>
```

Interesting right? Both do addition, but in pretty different ways. While the C code assembly is pretty easy to understand, let's look at how addition works in OCaml.

## Addition in OCaml

Each integer is stored as `2x+1` which implies, adding two integers should return `2(x+y+1)` where `2x+1` is one integer and `2y+1` is another. But, the real result from the addition should have simply been `(x+y)` which would be stored in memory therefore as `2(x+y)+1`.

Note that there is only 1 bit difference between the result being stored by naive addition of the tagged integers and the actual result.

How does `lea` help us solve this? We'll have to dig deeper into `lea`.

### How lea works

`lea`: Load Effective Address

This is a instruction in `x86` (and others as well), which is used to calculate the memory addresses of pointers. The general `x86` syntax for the operand is `offset(base, index, scale)`:

- **offset**: An offet which is added to the final memory address
- **base**: The base address
- **scale**: This is what is multiplied by the index
- **index**: This is the memory index

And the hardware calculates this as:

```
Address = base + (index * scale) + offset
```

So, writing 

```x86asm
lea    -0x1(%rax,%rbx,1),%rax
```

basically means:

- **offset** = -0x1
- **base** = %rax
- **index** = %rbx
- **scale** = 1

So, the machine is going to compute 
```
%rax + (%rbx * 1) - 0x1 = %rax + %rbx - 0x1
```

The mystery is solved now! It takes our normal two tagged integers, adds them together than subtracts one (so we went up with `2(z+y)+1`) to get the tagged value for the result.

Thus this one uses one fast CPU cycle computes our sum!

## Summary

Here's what this blog post was meant to cover:

1. What is the meaning of tagged integers
2. Why are tagged integers useful
3. Differentiating between pointers and integers using it
4. Show the tagged representation in OCaml vs normal in C
5. Optimisation in OCaml not in C (or other languages which don't have tagged integers)