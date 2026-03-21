+++
title = "Tagged integer multiplication in OCaml"
date = 2026-03-22
draft = false

[taxonomies]
categories = ["OCaml", "compilers"]
tags = ["functional-programming", "blog", "assembly"]

[extra]
lang = "en"
+++

We're going to compare `OCaml` with `C` as we do. Both are trying to multiple two integers `a` and `b` and return the value. All of this is AT&T syntax and I hate it (because I like intel's) and it feels reversed to me (**it is**).

## C version:

The following code snippet have been used:

```c
#include <stdio.h>

int multiply(int a, int b) {
	int c = a * b;
	return c;
}

int main() {
	int c = multiply(10, 20);
	printf("%d", c);
}
```

And this is the `assembly`:

```x86asm
0000000000001149 <multiply>:
    1149:	f3 0f 1e fa          	endbr64 
    114d:	55                   	push   %rbp
    114e:	48 89 e5             	mov    %rsp,%rbp
    1151:	89 7d ec             	mov    %edi,-0x14(%rbp) 
    1154:	89 75 e8             	mov    %esi,-0x18(%rbp)	
    1157:	8b 45 ec             	mov    -0x14(%rbp),%eax
    115a:	0f af 45 e8          	imul   -0x18(%rbp),%eax
    115e:	89 45 fc             	mov    %eax,-0x4(%rbp)
    1161:	8b 45 fc             	mov    -0x4(%rbp),%eax
    1164:	5d                   	pop    %rbp
    1165:	c3                   	ret    
```

## C compiler optimisation (`-O3`):

```x86asm
0000000000001180 <multiply>:
    1180:	f3 0f 1e fa          	endbr64 
    1184:	89 f8                	mov    %edi,%eax
    1186:	0f af c6             	imul   %esi,%eax
    1189:	c3                   	ret    
```

This is the heavily optimized multiplication. Simply enough. We get the values `a` and `b` inside `edi` and `esi` so simply call `imul` on them (`imul` is a variant of `mul` which calls for signed or negative numbers as well).

Let's first understand what the C compiler did for the function without optimization flags:

1. It stored the values of `edi` and `esi` into the stack frame.
2. Then it would call the stack-frame and get the first value into `rax` from there.
3. Then multiple and store the value in `rax` back to the stack-frame!

This is cooked only. We don't need to do all that management if we don't care about debuggability or reverse-engineering the binary later! Which is why the optimized version is the way it is.

## OCaml version:

The following code snippet has been used:

```ocaml
let multiply_func x y = x * y;;

print_endline @@ string_of_int @@ multiply_func 10 20
```

And this is the `assembly`:

```x86asm
0000000000018dd0 <camlMain.multiply_func_274>:
   18dd0:	48 d1 fb             	sar    %rbx		// This is a bit shift by 1
   18dd3:	48 ff c8             	dec    %rax		// Decrement by 1
   18dd6:	48 0f af c3          	imul   %rbx,%rax	// multiply
   18dda:	48 ff c0             	inc    %rax		// Increment by 1
   18ddd:	c3                   	ret
   18dde:	66 90                	xchg   %ax,%ax 	// This is a 2 byte NOP code
```

Damn, these are objectively different (pun intended). Both of them were compiled without any optimisations. Actually, if we do optimize the C code:

So what happens for the OCaml case? Let's go over it one step at a time:

> sar    %rbx

This is effectively: `%rbx >> 1`, see [this stack overflow](https://stackoverflow.com/questions/12813962/sar-command-in-x86-assembly-with-one-parameter) answer for more details. So when we do this on a tagged integer:

1. `sar` when applied to an odd number is equivalent to a `floor` division by 2.
2. `sar` on an even number is normal division.

Thus, in our tagged integer case (2x+1), we effectively get `(2x+1)//2`, which is `x`.

> dec    %rax

This gives us `2y`. Note that we are assuming that `rax` and `rbx` hold the two integers we want to play around with.

> imul   %rbx,%rax

Performs an sign preserving multiplication on the two integers (stores the result in `rax`). So, `rax = 2yx`

> inc    %rax

Now `rax = 2xy+1` and that's exactly the result we were expecting for tagged multiplication!

## Conclusion

Is this better than C? To be honest, this example was not complex enough to give out a good answer to this question! Maybe in the future...