+++
title = "Understanding Triton kernels and TTIR"
date = 2026-04-26
draft = false

[taxonomies]
categories = ["Triton", "compilers"]
tags = ["blog", "assembly"]

[extra]
lang = "en"
+++

## Triton kernels

I had been trying to see how triton's GPU kernels compile to LLVM IR. Seemed especially interesting given the fact that triton is python written for GPUs! So, let's start with a very very simple example, which I am picking from [this repo](https://github.com/rkinas/triton-resources/blob/main/daily_challange/day0/add_constant.py).

```python3
import time
import torch
import triton
import triton.language as tl

@triton.jit
def constant_add_kernel(
    x_ptr,          # Pointer to the input vector x
    constant,       # The constant value to add
    y_ptr,          # Pointer to the output vector y
    N0: tl.constexpr,      # Total number of elements in vector x (and y)
    BLOCK_SIZE: tl.constexpr  # Block size, set equal to N0
):
    # Each kernel instance processes a block of elements.
    # With BLOCK_SIZE equal to N0, only one instance is launched.
    pid = tl.program_id(0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < N0  # Ensure we don't access out-of-bound indices

    # Load x values, add the constant, and store the result in y
    x = tl.load(x_ptr + offsets, mask=mask)
    y = x + constant
    tl.store(y_ptr + offsets, y, mask=mask)

def constant_add_triton(x: torch.Tensor, constant: float) -> torch.Tensor:
    """
    Adds a constant to each element of the input vector x using a Triton kernel.
    
    The block size is set equal to the vector length (N0), meaning that only one
    kernel instance is launched.
    
    Args:
        x (torch.Tensor): Input vector on CUDA.
        constant (float): The constant to add to each element.
    
    Returns:
        torch.Tensor: Output vector with the constant added.
    """
    N0 = x.numel()
    BLOCK_SIZE = N0  # Block size equals the vector length
    y = torch.empty_like(x)
    
    # With BLOCK_SIZE = N0, our grid consists of a single block.
    grid = lambda meta: (1,)
    
    # Launch the Triton kernel
    constant_add_kernel[grid](x, constant, y, N0, BLOCK_SIZE=BLOCK_SIZE)
    return y
```

You probably can't have a simpler kernel (that's also non-trivial) than this. In the final step of the wrapper function, before calling the kernel, let's print all compilation IRs:

```python3
def constant_add_triton(x: torch.Tensor, constant: float) -> torch.Tensor:
	...    
    # Launch the Triton kernel
    triton_kernel = constant_add_kernel[grid](x, constant, y, N0, BLOCK_SIZE=BLOCK_SIZE)
    
	with open('triton_IR_S.txt', 'w') as f:
	    print(triton_kernel.asm['ttir'], file=f)
	with open('triton_TTGIR_S.txt', 'w') as f:
	    print(triton_kernel.asm['ttgir'], file=f)
	with open('triton_LLVMIR_S.txt', 'w') as f:
	    print(triton_kernel.asm['llir'], file=f)
	with open('triton_PTX_S.ptx', 'w') as f:
	    print(triton_kernel.asm['ptx'], file=f)
	with open('triton_cubin_S.txt', 'w') as f:
	    print(triton_kernel.asm['cubin'], file=f)

    return y
```

So, the normal compilation process goes like:

1. The python code is read by the interpreter and the JIT compiler `"compiles"` the kernel

You see that decorator `@triton.jit`? That's what's telling triton that this is the kernel implementation. This is a JIT (Just-In-Time) compiler because... there really is no other way. You need to run the python code to start the interpreter which means you NEED a JIT and you can't have an AOT (Ahead-of-Time) compiler. This is kind of good too because this means less headaches especially since you specify what to compile.

2. The compilation first creates a `MLIR`. `MLIR` is kind of an umbrella term for:

- Triton-IR (ttir)
- Triton-GPUIR (ttgir)
- LLVM-IR (LLIR)

3. Next the LLVM-IR is used to compile the code into device assembly (PTX) -> This enabled all of LLVM's optimisations
4. And finally this becomes a binary (`cubin` or CUda+BIN)

### Understanding TTIR

Let's first look at TTIR and see what we've got. [This is the right documentation](https://mlir.llvm.org/docs/) if you wish to go through it yourself.

```c
#loc = loc("/tmp/ipykernel_1718/1626969236.py":11:0)
#loc13 = loc("x_ptr"(#loc))
#loc14 = loc("constant"(#loc))
#loc15 = loc("y_ptr"(#loc))
module {
  tt.func public @constant_add_kernel(%x_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("x_ptr"(#loc)), %constant: f32 loc("constant"(#loc)), %y_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("y_ptr"(#loc))) attributes {noinline = false} {
    %mask = arith.constant dense<1024> : tensor<1024xi32> loc(#loc16)
    %c1024_i32 = arith.constant 1024 : i32 loc(#loc2)
    %pid = tt.get_program_id x : i32 loc(#loc17)
    %offsets = arith.muli %pid, %c1024_i32 : i32 loc(#loc18)
    %offsets_0 = tt.make_range {end = 1024 : i32, start = 0 : i32} : tensor<1024xi32> loc(#loc19)
    %offsets_1 = tt.splat %offsets : i32 -> tensor<1024xi32> loc(#loc20)
    %offsets_2 = arith.addi %offsets_1, %offsets_0 : tensor<1024xi32> loc(#loc20)
    %mask_3 = arith.cmpi slt, %offsets_2, %mask : tensor<1024xi32> loc(#loc16)
    %x = tt.splat %x_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc21)
    %x_4 = tt.addptr %x, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc21)
    %x_5 = tt.load %x_4, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc22)
    %y = tt.splat %constant : f32 -> tensor<1024xf32> loc(#loc23)
    %y_6 = arith.addf %x_5, %y : tensor<1024xf32> loc(#loc23)
    %0 = tt.splat %y_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc10)
    %1 = tt.addptr %0, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc10)
    tt.store %1, %y_6, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc11)
    tt.return loc(#loc12)
  } loc(#loc)
} loc(#loc)
#loc1 = loc("/tmp/ipykernel_1718/1626969236.py":22:21)
#loc2 = loc(unknown)
#loc3 = loc("/tmp/ipykernel_1718/1626969236.py":20:24)
#loc4 = loc("/tmp/ipykernel_1718/1626969236.py":21:20)
#loc5 = loc("/tmp/ipykernel_1718/1626969236.py":21:46)
#loc6 = loc("/tmp/ipykernel_1718/1626969236.py":21:33)
#loc7 = loc("/tmp/ipykernel_1718/1626969236.py":25:24)
#loc8 = loc("/tmp/ipykernel_1718/1626969236.py":25:16)
#loc9 = loc("/tmp/ipykernel_1718/1626969236.py":26:12)
#loc10 = loc("/tmp/ipykernel_1718/1626969236.py":27:21)
#loc11 = loc("/tmp/ipykernel_1718/1626969236.py":27:30)
#loc12 = loc("/tmp/ipykernel_1718/1626969236.py":27:4)
#loc16 = loc("mask"(#loc1))
#loc17 = loc("pid"(#loc3))
#loc18 = loc("offsets"(#loc4))
#loc19 = loc("offsets"(#loc5))
#loc20 = loc("offsets"(#loc6))
#loc21 = loc("x"(#loc7))
#loc22 = loc("x"(#loc8))
#loc23 = loc("y"(#loc9))
```

From a [blog post on Trition compilation cycles](https://pytorch.org/blog/triton-kernel-compilation-stages/), I could understand that this is **based** on the open-source LLVM compiler project. Which I am assuming to mean that the syntax and semantics are "similar".

Let's ignore the fluff for now (we'll come back to all the `loc` lines later) and look at the center of attraction:

```c
module {
  tt.func public @constant_add_kernel(%x_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("x_ptr"(#loc)), %constant: f32 loc("constant"(#loc)), %y_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("y_ptr"(#loc))) attributes {noinline = false} {
    %mask = arith.constant dense<1024> : tensor<1024xi32> loc(#loc16)
    %c1024_i32 = arith.constant 1024 : i32 loc(#loc2)
    %pid = tt.get_program_id x : i32 loc(#loc17)
    %offsets = arith.muli %pid, %c1024_i32 : i32 loc(#loc18)
    %offsets_0 = tt.make_range {end = 1024 : i32, start = 0 : i32} : tensor<1024xi32> loc(#loc19)
    %offsets_1 = tt.splat %offsets : i32 -> tensor<1024xi32> loc(#loc20)
    %offsets_2 = arith.addi %offsets_1, %offsets_0 : tensor<1024xi32> loc(#loc20)
    %mask_3 = arith.cmpi slt, %offsets_2, %mask : tensor<1024xi32> loc(#loc16)
    %x = tt.splat %x_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc21)
    %x_4 = tt.addptr %x, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc21)
    %x_5 = tt.load %x_4, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc22)
    %y = tt.splat %constant : f32 -> tensor<1024xf32> loc(#loc23)
    %y_6 = arith.addf %x_5, %y : tensor<1024xf32> loc(#loc23)
    %0 = tt.splat %y_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc10)
    %1 = tt.addptr %0, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc10)
    tt.store %1, %y_6, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc11)
    tt.return loc(#loc12)
  } loc(#loc)
}
```

In LLVM IR, all the `%` prefixed strings are identifiers, which I am assuming is the case here. We're defining a function (`tt.func`) that is `public` (which I am assuming means that it is accessbile outside of this module definition as well, LLVM IR doesn't have any `public` linkage though, its called `external` or something). The name is a global definition (`@constant_add_kernel`) and we can see that we're passing in the same params we had defined in our function:

```py
def constant_add_kernel(
    x_ptr,          # Pointer to the input vector x
    constant,       # The constant value to add
    y_ptr,          # Pointer to the output vector y
    N0: tl.constexpr,      # Total number of elements in vector x (and y)
    BLOCK_SIZE: tl.constexpr  # Block size, set equal to N0
):
```

One interesting thing to note is that the IR doesn't include the number of elements in the vectors and the block size. If you look at these lines carefully:

```c
%c1024_i32 = arith.constant 1024
%pid = tt.get_program_id x : i32 loc(#loc17)
%offsets = arith.muli %pid, %c1024_i32 : i32 loc(#loc18)
```

It just assumed the block size to be 1024 (`N0`), and proceed from. So, it never takes that as a function parameter, cause its smart. (this is the same `pid * BLOCK_SIZE` multiplication we used in the kernel).

- The `arith` dialect is intended to hold basic integer and floating point mathematical operations. You can see here that it has a lot of functionality and its quite similar to the basic assembly instructions like `add`, `imul` etc.

- Note that most of the operations are ALSO dependent on the strings following it. Look at this example from the documentation:

```c
// Scalar addition.
%a = arith.addf %b, %c : f64

// SIMD vector addition, e.g. for Intel SSE.
%f = arith.addf %g, %h : vector<4xf32>

// Tensor addition.
%x = arith.addf %y, %z : tensor<4x?xbf16>

// Scalar addition with rounding mode.
%a = arith.addf %b, %c to_nearest_even : f64
```

In our case for example we have this `addf`:

```c
%y_6 = arith.addf %x_5, %y : tensor<1024xf32> loc(#loc23)
```

This means a tensor addition! Nice.

Let's look at the analogs for these parts of the code now:

```py
x = tl.load(x_ptr + offsets, mask=mask)
y = x + constant
tl.store(y_ptr + offsets, y, mask=mask)
```

which we'll find here:

```c
%offsets_0 = tt.make_range {end = 1024 : i32, start = 0 : i32} : tensor<1024xi32> loc(#loc19)
%offsets_1 = tt.splat %offsets : i32 -> tensor<1024xi32> loc(#loc20)
%offsets_2 = arith.addi %offsets_1, %offsets_0 : tensor<1024xi32> loc(#loc20)
%mask_3 = arith.cmpi slt, %offsets_2, %mask : tensor<1024xi32> loc(#loc16)
%x = tt.splat %x_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc21)
%x_4 = tt.addptr %x, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc21)
%x_5 = tt.load %x_4, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc22)
%y = tt.splat %constant : f32 -> tensor<1024xf32> loc(#loc23)
%y_6 = arith.addf %x_5, %y : tensor<1024xf32> loc(#loc23)
%0 = tt.splat %y_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc10)
%1 = tt.addptr %0, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc10)
tt.store %1, %y_6, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc11)
tt.return loc(#loc12)
```

We had seen what `%offsets` is storing (the `arith.muli` instruction), now we can trace this out.

- The `tt.make_range` is defined [here](https://triton-lang.org/main/dialects/TritonOps.html#tt-make-range-triton-makerangeop). It creates a 1D int32 tensor whose values span from `$start` to `$end` (exclusive), with step = 1.

- So our `offsets_0` is a 1D tensor, a vector (which is what is denoted by the `: tensor<1024xi32>` in the end) that spans from 0 to 1024 (the `N0` value).

The reason the code is doing that is because we had defined something like this:

```py
offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
```

So, it already calculated the `pid*BLOCK_SIZE` and now it needs the vector to add it to. But it also needs to ensure alignment:

```c
%offsets_1 = tt.splat %offsets : i32 -> tensor<1024xi32> loc(#loc20)
%offsets_2 = arith.addi %offsets_1, %offsets_0 : tensor<1024xi32> loc(#loc20)
```

which is exactly what the `%offsets_1` identifier is doing. The `%offsets_2` identifier is the analog of the `offsets` variable in python which is the final result of the addition. The output is a tensor. The `splat` function is used to convert between datatypes.

The syntax for the `tt.splat` operation is as follows:

```
operation ::= `tt.splat` $src attr-dict `:` type($src) `->` type($result)
```

which means in our case, it converts the single `i32` value we got in `%offsets` calculation. Recall that

```c
%offsets = arith.muli %pid, %c1024_i32 : i32 loc(#loc18)
```

`%offsets` was therefore a 32 bit integer before, which we converted now to a tensor for addition.

- Then it performs the addition which also results in a `tensor<1024xi32>` (basically a 1D tensor or a vector of 32 bit integers).

Then we see it create the mask here:

```c
%mask = arith.constant dense<1024> : tensor<1024xi32> loc(#loc16)
...
%mask_3 = arith.cmpi slt, %offsets_2, %mask : tensor<1024xi32> loc(#loc16)
```

I am not sure why its `mask_3` and not `mask_1`? or even `mask_0`? I am assuming this is also SSA like LLVMIR. The numbering might be a little off.

- The `arith.cmpi` instruction is documented [here](https://mlir.llvm.org/docs/Dialects/ArithOps/#arithcmpi-arithcmpiop), it follows this syntax:

```
operation ::= `arith.cmpi` $predicate `,` $lhs `,` $rhs attr-dict `:` type($lhs)
```

in our case, the `$predicate` is `slt` which stands for **signed less than**, the `$lhs` is `%offsets_2` (which basically the "**offsets**" variable in the python code) and the `$rhs` is the older `%mask` which is simply a constant vector held in memory.

- Recall that when we were making the mask, we said `mask = offsets < N0`, that's the comparision we're going to do here.

- The result is `1` if the comparison is true and `0` otherwise. Note that the syntax doesn't provide us the output type of the result, rather the output type of `$lhs` so lets not get confused as to why its a tensor.

So our `mask_3` is either a 0 or 1, let's move on:

```c
%x = tt.splat %x_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc21)
%x_4 = tt.addptr %x, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc21)
%x_5 = tt.load %x_4, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc22)
%y = tt.splat %constant : f32 -> tensor<1024xf32> loc(#loc23)
%y_6 = arith.addf %x_5, %y : tensor<1024xf32> loc(#loc23)
%0 = tt.splat %y_ptr : !tt.ptr<f32> -> tensor<1024x!tt.ptr<f32>> loc(#loc10)
%1 = tt.addptr %0, %offsets_2 : tensor<1024x!tt.ptr<f32>>, tensor<1024xi32> loc(#loc10)
tt.store %1, %y_6, %mask_3 : tensor<1024x!tt.ptr<f32>> loc(#loc11)
tt.return loc(#loc12)
```

- Recall how we wanted to add `x_ptr + offsets` before passing it to `tl.load` (which is `tt.load` here). To do that, we need to ensure that both are of the same types.
- The `tt.splat` in this case also converts the 32 bit floating pointer to a tensor of 32 bit floating pointers. This is creating the `constant` indentifier we're using in the python code for `y`.

- Then we call the `arith.addf` function, and from previous discussions we know that this is tensor addition between the output of `tl.load` (or `tt.load`) add that to the constant to get the `y` value from the python code.

- Then we load in the `y_ptr` via `%0` and convert it from a floating 32 bit to a tensor of 32 bit floats.
- Add the `y_ptr` to the `offsets` (or `%offsets2` in this case) and then we store it along with the `mask`, just like we do in python.

---

That brings us to an end of this introduction. You can see that its NOT very different from the python code itself except for a few more details on how things are actually working. But its not "there" yet, as in not sufficiently low level.

So next we'll be looking at TTGIR which is the next stage in the compilation process and then understand how the IR maps to the GPU architecture.

Thanks for reading!