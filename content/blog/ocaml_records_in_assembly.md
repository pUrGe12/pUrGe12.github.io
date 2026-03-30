+++
title = "OCaml records in assembly"
date = 2026-03-30
draft = false

[taxonomies]
categories = ["OCaml", "compilers"]
tags = ["functional-programming", "blog", "assembly"]

[extra]
lang = "en"
+++

## What's a record

A `record` is a data strcuture in OCaml. In its core, its a type definition which goes like this:

```ocaml
type books = {
	author: string;
	num_pages: int;
	publisher: string;
};;
```

Now this is a new `type` in OCaml, so you are allowed to do something like this:

```ocaml
let book : books = {
	author : string = "Chris Gardner";
	num_pages : int = 400;
	publisher : string = "I don't remember";
};;
(* val book : books = {author="chris Gardner"; num_pages=400; publisher="I don't remember"}*)
```

OCaml will **infer** that book is of type books even if we don't pass in the type explicitly. Well if I just did:

```ocaml
let something = {
	name = "Mine";
	age = 20;	
};;
```

Well, OCaml has no idea what this is! It cannot work this way, we must define a `type` for such a thing to exist. You'll get that the field `name` is unbound which is true.

### How do I use it?

Well, the idea is that you can pull invidual elements from this record. So, if you want say the author, you can do:

```ocaml
let a = book.author;;
(*val a : string = "Chris Gardner"*)
```

Nice and beautiful. You can then, define some anonymous functions, push all authors to a list using maps and do what not. Its a clean way to hold data.

## In assembly

Now, what does this look like in assembly? Let's write up a simple file called `main.ml` and compile it with all debugging flags to see what's going on under the hood

> main.ml
```ocaml
type coords = {
	x_coord : float;
	y_coord : float;
	z_coord : float;
};;

let dist ~a:(x:coords) ~b:(y:coords) = 
	((x.x_coord -. y.x_coord)**2. +. (x.y_coord -. y.y_coord)**2. +. (x.z_coord -. y.z_coord)**2.)**0.5;;


let point_1 : coords = {
	x_coord = 2.1;
	y_coord = -1.8;
	z_coord = -5.2;
};;

let point_2 : coords = {
	x_coord = 3.2;
	y_coord = -3.1;
	z_coord = -4.1;
};;

let distance = dist ~a:point_1 ~b:point_2;;
print_endline @@ string_of_float distance;;
```

This is a simple program, which is defining a coordinate type called `coords` and a function for the computing the distance between two points in 3D space called `dist`. 

Then we define two points `point_1` and `point_2` and compute their distance and print it. So, let's compile this using:

```sh
ocamlopt -o main main.ml -g
```

### Inspections

Let's look at the objdump and understand how the relevant parts of the code come about. Look for the entry point:

```nasm
0000000000018ea0 <camlMain.entry>:
   18ea0:	4c 8d 94 24 c0 fe ff 	lea    -0x140(%rsp),%r10
   18ea7:	ff 
   18ea8:	4d 3b 56 28          	cmp    0x28(%r14),%r10
   18eac:	0f 82 aa 00 00 00    	jb     18f5c <camlMain.entry+0xbc>
   18eb2:	48 8d 35 ef ac 04 00 	lea    0x4acef(%rip),%rsi        # 63ba8 <camlMain.5>
   18eb9:	48 8d 3d 08 ad 04 00 	lea    0x4ad08(%rip),%rdi        # 63bc8 <camlMain>
   18ec0:	48 89 e3             	mov    %rsp,%rbx
   18ec3:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18ec7:	e8 f4 95 01 00       	call   324c0 <caml_initialize>
   18ecc:	48 89 dc             	mov    %rbx,%rsp
   18ecf:	48 8d 35 4a ad 04 00 	lea    0x4ad4a(%rip),%rsi        # 63c20 <camlMain.3>
   18ed6:	48 8d 3d eb ac 04 00 	lea    0x4aceb(%rip),%rdi        # 63bc8 <camlMain>
   18edd:	48 83 c7 08          	add    $0x8,%rdi
   18ee1:	48 89 e3             	mov    %rsp,%rbx
   18ee4:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18ee8:	e8 d3 95 01 00       	call   324c0 <caml_initialize>
   18eed:	48 89 dc             	mov    %rbx,%rsp
   18ef0:	48 8d 35 09 ad 04 00 	lea    0x4ad09(%rip),%rsi        # 63c00 <camlMain.4>
   18ef7:	48 8d 3d ca ac 04 00 	lea    0x4acca(%rip),%rdi        # 63bc8 <camlMain>
   18efe:	48 83 c7 10          	add    $0x10,%rdi
   18f02:	48 89 e3             	mov    %rsp,%rbx
   18f05:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18f09:	e8 b2 95 01 00       	call   324c0 <caml_initialize>
   18f0e:	48 89 dc             	mov    %rbx,%rsp
   18f11:	48 8d 1d e8 ac 04 00 	lea    0x4ace8(%rip),%rbx        # 63c00 <camlMain.4>
   18f18:	48 8d 05 01 ad 04 00 	lea    0x4ad01(%rip),%rax        # 63c20 <camlMain.3>
   18f1f:	e8 ac fe ff ff       	call   18dd0 <camlMain.dist_278>
   18f24:	48 8d 3d 9d ac 04 00 	lea    0x4ac9d(%rip),%rdi        # 63bc8 <camlMain>
   18f2b:	48 83 c7 18          	add    $0x18,%rdi
   18f2f:	48 89 c6             	mov    %rax,%rsi
   18f32:	48 89 e3             	mov    %rsp,%rbx
   18f35:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18f39:	e8 82 95 01 00       	call   324c0 <caml_initialize>
   18f3e:	48 89 dc             	mov    %rbx,%rsp
   18f41:	48 8d 05 80 ac 04 00 	lea    0x4ac80(%rip),%rax        # 63bc8 <camlMain>
   18f48:	48 8b 40 18          	mov    0x18(%rax),%rax
   18f4c:	e8 ff 1b 00 00       	call   1ab50 <camlStdlib.string_of_float_189>
   18f51:	e8 da 28 00 00       	call   1b830 <camlStdlib.print_endline_369>
   18f56:	b8 01 00 00 00       	mov    $0x1,%eax
   18f5b:	c3                   	ret    
   18f5c:	6a 21                	push   $0x21
   18f5e:	e8 dd ad 02 00       	call   43d40 <caml_call_realloc_stack>
   18f63:	41 5a                	pop    %r10
   18f65:	e9 48 ff ff ff       	jmp    18eb2 <camlMain.entry+0x12>
```

Few things before I dump more assembly on you:

1. The `camlMain.dist_278` reference at `18f1f`, that is our function for computing the distance.

2. `string_of_float` and `print_endline` are also visible, being called from the standard library.

3. `caml_initialize` is literally called 4 times. What is that about? (we'll see)

4. The references to `camlMain` and its subparts (`camlMain.5` for example) seems quite common, so we should investigate that too.

Let's start with the function actually, cause that's kinda simple enough to find:

```nasm
0000000000018dd0 <camlMain.dist_278>:
   18dd0:	48 83 ec 10          	sub    $0x10,%rsp
   18dd4:	49 89 c4             	mov    %rax,%r12
   18dd7:	49 89 dd             	mov    %rbx,%r13
   18dda:	f2 0f 10 0d 56 52 03 	movsd  0x35256(%rip),%xmm1        # 4e038 <caml_absf_mask+0x18>
   18de1:	00 
   18de2:	f2 41 0f 10 44 24 10 	movsd  0x10(%r12),%xmm0
   18de9:	f2 41 0f 5c 45 10    	subsd  0x10(%r13),%xmm0
   18def:	48 89 e3             	mov    %rsp,%rbx
   18df2:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18df6:	e8 b5 f9 ff ff       	call   187b0 <pow@plt>
   18dfb:	48 89 dc             	mov    %rbx,%rsp
   18dfe:	f2 0f 11 44 24 08    	movsd  %xmm0,0x8(%rsp)
   18e04:	f2 0f 10 0d 2c 52 03 	movsd  0x3522c(%rip),%xmm1        # 4e038 <caml_absf_mask+0x18>
   18e0b:	00 
   18e0c:	f2 41 0f 10 44 24 08 	movsd  0x8(%r12),%xmm0
   18e13:	f2 41 0f 5c 45 08    	subsd  0x8(%r13),%xmm0
   18e19:	48 89 e3             	mov    %rsp,%rbx
   18e1c:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e20:	e8 8b f9 ff ff       	call   187b0 <pow@plt>
   18e25:	48 89 dc             	mov    %rbx,%rsp
   18e28:	f2 0f 11 04 24       	movsd  %xmm0,(%rsp)
   18e2d:	f2 0f 10 0d 03 52 03 	movsd  0x35203(%rip),%xmm1        # 4e038 <caml_absf_mask+0x18>
   18e34:	00 
   18e35:	f2 41 0f 10 04 24    	movsd  (%r12),%xmm0
   18e3b:	f2 41 0f 5c 45 00    	subsd  0x0(%r13),%xmm0
   18e41:	48 89 e3             	mov    %rsp,%rbx
   18e44:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e48:	e8 63 f9 ff ff       	call   187b0 <pow@plt>
   18e4d:	48 89 dc             	mov    %rbx,%rsp
   18e50:	f2 0f 10 0c 24       	movsd  (%rsp),%xmm1
   18e55:	f2 0f 58 c1          	addsd  %xmm1,%xmm0
   18e59:	f2 0f 10 4c 24 08    	movsd  0x8(%rsp),%xmm1
   18e5f:	f2 0f 58 c1          	addsd  %xmm1,%xmm0
   18e63:	f2 0f 10 0d c5 51 03 	movsd  0x351c5(%rip),%xmm1        # 4e030 <caml_absf_mask+0x10>
   18e6a:	00 
   18e6b:	48 89 e3             	mov    %rsp,%rbx
   18e6e:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e72:	e8 39 f9 ff ff       	call   187b0 <pow@plt>
   18e77:	48 89 dc             	mov    %rbx,%rsp
   18e7a:	49 83 ef 10          	sub    $0x10,%r15
   18e7e:	4d 3b 3e             	cmp    (%r14),%r15
   18e81:	72 15                	jb     18e98 <camlMain.dist_278+0xc8>
   18e83:	49 8d 47 08          	lea    0x8(%r15),%rax
   18e87:	48 c7 40 f8 fd 04 00 	movq   $0x4fd,-0x8(%rax)
   18e8e:	00 
   18e8f:	f2 0f 11 00          	movsd  %xmm0,(%rax)
   18e93:	48 83 c4 10          	add    $0x10,%rsp
   18e97:	c3                   	ret    
   18e98:	e8 3f b1 02 00       	call   43fdc <caml_call_gc>
   18e9d:	eb e4                	jmp    18e83 <camlMain.dist_278+0xb3>
   18e9f:	90                   	nop
``` 

Again a few points before we start analyzing this:

1. `MOVSD xmm1, xmm2`: This means "Move scalar double precision floating-point value from xmm2 to xmm1 register". Documentation [here](https://www.felixcloutier.com/x86/movsd).
2. `SUBSD xmm1, xmm2/m64`: This means "Subtract the low double precision floating-point value in xmm2/m64 from xmm1 and store the result in xmm1". Documentation [here](https://www.felixcloutier.com/x86/subsd)
3. `ADDSD xmm1, xmm2/m64`: This means "Add the low double precision floating-point value from xmm2/mem to xmm1 and store the result in xmm1". Documentation [here](https://www.felixcloutier.com/x86/addsd).

Note that this is `intel` syntax, and the one we're seeing, is AT&T syntax, so the `order` of operands will be flipped. Keep that in mind.

You should be able to identify that there are 3 repeating chunks of:

```nasm
   18e35:	f2 41 0f 10 04 24    	movsd  (%r12),%xmm0
   18e3b:	f2 41 0f 5c 45 00    	subsd  0x0(%r13),%xmm0
   18e41:	48 89 e3             	mov    %rsp,%rbx
   18e44:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18e48:	e8 63 f9 ff ff       	call   187b0 <pow@plt>
   18e4d:	48 89 dc             	mov    %rbx,%rsp
   18e50:	f2 0f 10 0c 24       	movsd  (%rsp),%xmm1
```

We also had 3 very similar things right! The "subtract the coordinates and square them" part. First understand what `%xmm0` and `%xmm1` are. Chances are, that you have **never** seen these registers in any assembly before. [This](https://computerscience.chemeketa.edu/CS205/week06/floats.html) is a very helpful blog to understand why these registers came out. Here's a small summary:

- Floating point numbers never used to be a part of x86 architecture. So, no standard register (like `RAX`) can handle floats. We need special registers.
- These special registers are called `XMM` registers, they start from `xmm0` all the way to `xmm15` with each being 128bits.

With that in mind, you can always think of `movsd`, `subsd` and `addsd` as their 64 bit equivalent (`mov`, `sub` and `add`) but for the XMM registers. Now that it is clear, its not very hard to trace the function and see that its exactly doing what we expected. So, we can move on.

## A small picture

What's important to us in this blog is to understand **where** the data for the function comes from!

```nasm
   18f09:	e8 b2 95 01 00       	call   324c0 <caml_initialize>
   18f0e:	48 89 dc             	mov    %rbx,%rsp
   18f11:	48 8d 1d e8 ac 04 00 	lea    0x4ace8(%rip),%rbx        # 63c00 <camlMain.4>
   18f18:	48 8d 05 01 ad 04 00 	lea    0x4ad01(%rip),%rax        # 63c20 <camlMain.3>
   18f1f:	e8 ac fe ff ff       	call   18dd0 <camlMain.dist_278>
```

Let's look over here. I still haven't told you what the `caml_initialize` calls are doing, but if we ignore that bit for now, see what happens below it.

- We call the store the value of the register **rbx** into the **stack pointer (rsp)**. What the fuck you may say. To understand this we'll have to do the whole assembly trace, which we'll do in just a moment.
- Then we populate `rbx` and `rax` with the addresses present in the `rip` shifted by different offsets. `rip` is the instruction pointer, this esentially keeps track of where the CPU is executing code. We're using `RIP` relative adressing here. It's basically saying "The data we want is exactly 0x4ad01 bytes away from where we are right now."
- The difference between the memory locations is `0x19` (or 25). But if you see the comments, the final memory address are actually `0x20` bytes apart (or 32). My claim is that `32` bytes (or 256) is the size of our `record`. We'll verify that later.

Where did this extra 7 bytes come from? That's the `lea` instruction itself. You can count up those bytes (`48 8d 05 01 ad 04 00`). To even begin thinking about what `lea` does, it has to read all 7 bytes of that instruction. By the time it is ready to actually perform the math (adding the offset to the pointer), the "play-head" `%rip` is already sitting at the start of the next instruction.

Hence, we add the 7 bytes to the 25 bytes of offset to get 32 bytes.

- Now we have these **values** stored in `rbx` and `rax`, so we call the `dist` function and we already know what happens in there.

## The big picture

Now its time to answer the question of `caml_initialize`. What the hell is it even doing?

```nasm
00000000000324c0 <caml_initialize>:
   324c0:	f3 0f 1e fa          	endbr64 
   324c4:	55                   	push   %rbp
   324c5:	53                   	push   %rbx
   324c6:	48 89 fb             	mov    %rdi,%rbx
   324c9:	48 83 ec 08          	sub    $0x8,%rsp
   324cd:	48 89 37             	mov    %rsi,(%rdi)
   324d0:	48 8b 05 51 55 03 00 	mov    0x35551(%rip),%rax        # 67a28 <caml_minor_heaps_end>
   324d7:	48 39 f8             	cmp    %rdi,%rax
   324da:	76 14                	jbe    324f0 <caml_initialize+0x30>
   324dc:	48 3b 3d 4d 55 03 00 	cmp    0x3554d(%rip),%rdi        # 67a30 <caml_minor_heaps_start>
   324e3:	76 0b                	jbe    324f0 <caml_initialize+0x30>
   324e5:	48 83 c4 08          	add    $0x8,%rsp
   324e9:	5b                   	pop    %rbx
   324ea:	5d                   	pop    %rbp
   324eb:	c3                   	ret    
   324ec:	0f 1f 40 00          	nopl   0x0(%rax)
   324f0:	40 f6 c6 01          	test   $0x1,%sil
   324f4:	75 ef                	jne    324e5 <caml_initialize+0x25>
   324f6:	48 39 f0             	cmp    %rsi,%rax
   324f9:	76 ea                	jbe    324e5 <caml_initialize+0x25>
   324fb:	48 3b 35 2e 55 03 00 	cmp    0x3552e(%rip),%rsi        # 67a30 <caml_minor_heaps_start>
   32502:	76 e1                	jbe    324e5 <caml_initialize+0x25>
   32504:	48 8b 05 cd 0a 03 00 	mov    0x30acd(%rip),%rax        # 62fd8 <caml_state@@Base+0x62fd0>
   3250b:	64 48 8b 00          	mov    %fs:(%rax),%rax
   3250f:	48 8b 68 60          	mov    0x60(%rax),%rbp
   32513:	48 8b 45 18          	mov    0x18(%rbp),%rax
   32517:	48 3b 45 20          	cmp    0x20(%rbp),%rax
   3251b:	73 13                	jae    32530 <caml_initialize+0x70>
   3251d:	48 8d 50 08          	lea    0x8(%rax),%rdx
   32521:	48 89 55 18          	mov    %rdx,0x18(%rbp)
   32525:	48 89 18             	mov    %rbx,(%rax)
   32528:	eb bb                	jmp    324e5 <caml_initialize+0x25>
   3252a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
   32530:	48 89 ef             	mov    %rbp,%rdi
   32533:	e8 08 50 00 00       	call   37540 <caml_realloc_ref_table>
   32538:	48 8b 45 18          	mov    0x18(%rbp),%rax
   3253c:	eb df                	jmp    3251d <caml_initialize+0x5d>
   3253e:	66 90                	xchg   %ax,%ax
```

If I were to give you a step by step breakdown:

1. It uses `rbx` with a similar grandeur as the base pointer, stores `rdi` into it
2. makes **8 bytes** of space by moving the stack pointer down
3. Moves `rsi` into the value held by `rdi` (now that it's content is safe)
4. Moves a certain value into `rax` by **rip-relative addressing**
5. It then compares `rdi` with `rax` (that is, the value held by `rsi` with the value in that specific memory location)
6. Then check if the **last bit of the esi** register is 1 or 0, if its not set, then we go back, **restore the 8 bytes** by moving the stack pointer up and **clear the stack and return**
7. Else, we compare `rsi` with `rax` (again, since last time we did `rdi` but `rdi` had `rsi`), and if they're equal, we do the same mechanism stated above.
8. If that's also not true, then we compare `rsi` with the value stored **31 bytes** from the previous one we were accessing (from `rip`)
9. if that's true we do the **same cleanup**, else we do a bunch of things, and eventually see again if we can pop the stack in the same way as above.
10. If none of that happens, we do a **no-op** and fuck off. 

I kinda got bored towards the end. But, what we're looking at, is actually something called the `The Write Barrier`. Yeah, we're into crazy territories now.

### The write barrier

The [wikipedia entry](https://en.wikipedia.org/wiki/Write_barrier) for write barrier is pretty sparse. But the garbage collection definition is spot on! The `caml_initialize` function is part of the garbage collection mechanism.

Take a look at this [post](https://discuss.ocaml.org/t/how-to-avoid-write-barrier-slowdown/2124). You might not understand it yet, but after I give you a small heads up, you'll be good to go.

- `mov %rsi, (%rdi)` is the actual work. This puts the value of `rsi` into the record field.
- `cmp %rdi, %rax` is basically asking whether this value is an old value or a new value. This is again for GC and we're NOT gonna go into that today.
- `test $0x1, %sil` is the most beautiful part.

I have already talked about tagged integers before and this is exactly why we tag integers. An integer will always have the lowest bit set, while pointers to memory locations won't. See [this post](https://purge12.github.io/blog/ocaml-compiler-tagged-integers/) to know more about that. So this instruction is checking if we have an **integer** in `sil` or a pointer.

The reason we exit immediately then is because integers don't point to anything, so GC doesn't care about them! The points 7 to 10 are the complex bits because now it means we're actually storing **pointers** and we must do something about that. And the GC handles it in a way.

### The big picture continued

Anyway, so what's the big picture? Why do we call `caml_initialize` so many times? Let me bring up the main sequence again in case we lost track of it:

```nasm
   18ea0:	4c 8d 94 24 c0 fe ff 	lea    -0x140(%rsp),%r10
   18ea7:	ff 
   18ea8:	4d 3b 56 28          	cmp    0x28(%r14),%r10
   18eac:	0f 82 aa 00 00 00    	jb     18f5c <camlMain.entry+0xbc>
   18eb2:	48 8d 35 ef ac 04 00 	lea    0x4acef(%rip),%rsi        # 63ba8 <camlMain.5>
   18eb9:	48 8d 3d 08 ad 04 00 	lea    0x4ad08(%rip),%rdi        # 63bc8 <camlMain>
   18ec0:	48 89 e3             	mov    %rsp,%rbx
   18ec3:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18ec7:	e8 f4 95 01 00       	call   324c0 <caml_initialize>
   18ecc:	48 89 dc             	mov    %rbx,%rsp
   18ecf:	48 8d 35 4a ad 04 00 	lea    0x4ad4a(%rip),%rsi        # 63c20 <camlMain.3>
   18ed6:	48 8d 3d eb ac 04 00 	lea    0x4aceb(%rip),%rdi        # 63bc8 <camlMain>
   18edd:	48 83 c7 08          	add    $0x8,%rdi
   18ee1:	48 89 e3             	mov    %rsp,%rbx
   18ee4:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18ee8:	e8 d3 95 01 00       	call   324c0 <caml_initialize>
   18eed:	48 89 dc             	mov    %rbx,%rsp
   18ef0:	48 8d 35 09 ad 04 00 	lea    0x4ad09(%rip),%rsi        # 63c00 <camlMain.4>
   18ef7:	48 8d 3d ca ac 04 00 	lea    0x4acca(%rip),%rdi        # 63bc8 <camlMain>
   18efe:	48 83 c7 10          	add    $0x10,%rdi
   18f02:	48 89 e3             	mov    %rsp,%rbx
   18f05:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18f09:	e8 b2 95 01 00       	call   324c0 <caml_initialize>
   18f0e:	48 89 dc             	mov    %rbx,%rsp
   18f11:	48 8d 1d e8 ac 04 00 	lea    0x4ace8(%rip),%rbx        # 63c00 <camlMain.4>
   18f18:	48 8d 05 01 ad 04 00 	lea    0x4ad01(%rip),%rax        # 63c20 <camlMain.3>
   18f1f:	e8 ac fe ff ff       	call   18dd0 <camlMain.dist_278>
   18f24:	48 8d 3d 9d ac 04 00 	lea    0x4ac9d(%rip),%rdi        # 63bc8 <camlMain>
   18f2b:	48 83 c7 18          	add    $0x18,%rdi
   18f2f:	48 89 c6             	mov    %rax,%rsi
   18f32:	48 89 e3             	mov    %rsp,%rbx
   18f35:	49 8b 66 40          	mov    0x40(%r14),%rsp
   18f39:	e8 82 95 01 00       	call   324c0 <caml_initialize>
   18f3e:	48 89 dc             	mov    %rbx,%rsp
   18f41:	48 8d 05 80 ac 04 00 	lea    0x4ac80(%rip),%rax        # 63bc8 <camlMain>
   18f48:	48 8b 40 18          	mov    0x18(%rax),%rax
   18f4c:	e8 ff 1b 00 00       	call   1ab50 <camlStdlib.string_of_float_189>
   18f51:	e8 da 28 00 00       	call   1b830 <camlStdlib.print_endline_369>
   18f56:	b8 01 00 00 00       	mov    $0x1,%eax
   18f5b:	c3                   	ret    
   18f5c:	6a 21                	push   $0x21
   18f5e:	e8 dd ad 02 00       	call   43d40 <caml_call_realloc_stack>
   18f63:	41 5a                	pop    %r10
   18f65:	e9 48 ff ff ff       	jmp    18eb2 <camlMain.entry+0x12>
```

This is the final piece of the puzzle isn't it? To understand what caml_initialize and GC means in this context, how this is actually setting up the `record` for us (you can probably see something resembling the setup of `point_1` and `point_2`, maybe?), and how its also setting up the result.

Additionally we would want to know, what `exactly` is an OCaml block in real. (see how OCaml actually represents data in a block [here](https://ocaml.org/docs/memory-representation)). Where is the function call in the entrypoint (looks like `call   1ab50 <camlStdlib.string_of_float_189>` just knows that `rax` is holding the answer somehow).

So, the questions won't end.

The big picture is that, we have a lot to learn, and this post is big enough as it is. I will tackle some ideas on the block representation and metadata of OCaml values in the future. Hopefully, one day, we'll be able to solve this mystery!

Thanks and have a good day!

---
