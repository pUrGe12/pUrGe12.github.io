+++
title = "Understanding LLVM IR with TCO"
date = 2026-04-25
draft = false

[taxonomies]
categories = ["LLVM", "compilers"]
tags = ["blog", "assembly"]

[extra]
lang = "en"
+++

## The first program

Let's write some basic C code to see how its LLVM IR looks like. LLVM IR is `SSA` (Single Static Assignment) type sorta low level language that all frontends using LLVM compile to (example clang). I will be using clang to generate the IR and we'll go through what it exactly means. The manual for the IR will be referenced in the discussion.

Let's start with the basic hello world in C (we'll slowly get more complex, and finish with a tail recursive fibonacci function)

```c
#include <stdio.h>

int main() {
    printf("HelloWorld!");
    return 0;
}
```
Now we need to convert this to the LLVM IR. Reading the `clang` man page we get this:

```
-flto, -flto=full, -flto=thin, -emit-llvm
      Generate output files in LLVM formats, suitable for link time optimization.  When used with -S this generates LLVM intermediate language  assembly  files,  otherwise  this
      generates LLVM bitcode format object files (which may be passed to the linker depending on the stage selection options).
```

So, we just need to do:

```sh
clang -S -emit-llvm hello.c -o hello.ll
```

And we have this piece of beauty:

```c
; ModuleID = 'hello.c'
source_filename = "hello.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [12 x i8] c"helloWorld!\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i64 0, i64 0))
  ret i32 0
}

declare i32 @printf(i8* noundef, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
```

### Analysis

Okay, where do we start? Let's see if there are any reference materials for the LLVM IR. Ummm. good news and bad news. Good news is I found the reference manual. bad news is that's the only think I found. See for youself here: [Manual](https://llvm.org/docs/LangRef.html#introduction).

Few bits of information:

1. Comments are started off with a semi-colon, that's good to know
2. Variables come in two types, global (preceeded by an `@`) and local (preceeded by a `%`). Usually we'll see `%` a lot because we tend of define stuff inside functions locally and all.
3. String definitions are simple, each character is read literally except a backslash. They start and end with `"`. So, in my code, 

```c
@.str = private unnamed_addr constant [12 x i8] c"helloWorld!\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i64 0, i64 0))
  ret i32 0
}
```

- This is the more important part. Here a global variable named `.str` is assigned and its "helloWorld!\00" The final \00 is the null byte which if you will recall is what C uses to define end of string and all. 

- The `private` linkage type basically means: it is only directly accessible by objects in the current module.

- Global variables can be marked with `unnamed_addr` which indicates that the address is not significant, only the content.

- `[12 x i8]` -> This simply means array of 12 "8 bit" integer values. Why 12? Because our string length is 12 (including null byte). Each letter is represented by an 8 bit integer. That's beautiful.

- align <n> or align(<n>): This indicates that the pointer value or vector of pointers has the specified alignment. This probably makes sense to compiler folks by not me, so I am going to take lite on this for now. I am assuming its about word (as in the computing definition ) alignment but then what does `align 1` or `align n` exactly mean?

Then we have a snarky little comment and then the main function definition:

```c
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i64 0, i64 0))
  ret i32 0
}
```

- `dso_local`: The compiler may assume that a function or variable marked as dso_local will resolve to a symbol within the same linkage unit. Direct access will be generated even if the definition is not within this compilation unit.

In our case, the `dso_local` is binding for the main function. `%1` and `%2` are the language's way of defining every unnamed variabe. It cannot let anything hanging and it starts sequentually. these are all local values. This is the whole idea behind **Static Single Assignment (SSA)** for which LLVM owns a part of its populatrity.

- This line:

```c
store i32 0, i32* %1, align 4
```

Looks like its trying to store the return value 0, by giving it a pointer which we just defined before `%1`. Actually no, this is an artifact of the unoptimized representation. This is equivalent to storing a random 0 for no reason because in the final return statement, it never referenes `%1`! Not sure why it does this.

Its kind of like `clang's` fault. So, hahaha.

- Then we call the function `printf` (which has a global definition), on our global `.str` variable `@.str` and returns 0.

- Obviously a bunch of other things were passed to `printf()`, but that's doing pointer arithmetic and we'll ignore that for now.

What about a bunch of other stuff that the code has:

```c
declare i32 @printf(i8* noundef, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
```

What's all this about?!

- The `!` is the metadata prefix. We have named and unnamed metadata (which get sequenced from 0). So all the lower 6 lines above, are unnamed metadata for this artifact. 

Information about the module as a whole is difficult to convey to LLVM’s subsystems. The LLVM IR isn’t sufficient to transmit this information. The `llvm.module.flags` named metadata exists in order to facilitate this. These flags are in the form of key / value pairs — much like a dictionary — making it easy for any subsystem that cares about a flag to look it up.

Note how it makes a reference to the unnamed metadata. That's just bookkeeping.

The `attributes` tag is from the "attribute groups": Attribute groups are groups of attributes that are referenced by objects within the IR. They are important for keeping .ll files readable, because a lot of functions will use the same set of attributes. In the degenerate case of a .ll file that corresponds to a single .c file, the single attribute group will capture the important command line flags used to build that file.

There are target dependent (`#0`) and target independent (`#1`). So this line `declare i32 @printf(i8* noundef, ...) #1` then means that `printf` has the attributes of attribute group `#1`.
- And `main` if you will recall then has the attributes of `#0`, which are **target dependent**.

## The second program

Now that we understand this a little bit, lets look at more relatively complex codes and see what changes and how.

```c
#include <stdio.h>

int main() {
	int a = 10;
	int b = 20;
	printf("sum=%d", a+b);
	return 0;
}
```

I just remembered how one of the optimizations that LLVM would do, was to replace printf with puts when we're not passing in dynamic values.

so looking at this IR:

```c
; ModuleID = 'hello2.c'
source_filename = "hello2.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"sum=%d\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 10, i32* %2, align 4
  store i32 20, i32* %3, align 4
  %4 = load i32, i32* %2, align 4
  %5 = load i32, i32* %3, align 4
  %6 = add nsw i32 %4, %5
  %7 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([7 x i8], [7 x i8]* @.str, i64 0, i64 0), i32 noundef %6)
  ret i32 0
}

declare i32 @printf(i8* noundef, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
```

### Analysis

We've understood most of the stuff, the important things other than bookkeeping are just these two things:

```c
@.str = private unnamed_addr constant [7 x i8] c"sum=%d\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 10, i32* %2, align 4
  store i32 20, i32* %3, align 4
  %4 = load i32, i32* %2, align 4
  %5 = load i32, i32* %3, align 4
  %6 = add nsw i32 %4, %5
  %7 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([7 x i8], [7 x i8]* @.str, i64 0, i64 0), i32 noundef %6)
  ret i32 0
}
```

- This time the number of bytes in the `.str` global variable is 7, it is litearlly counting the format specifier! This is ofcourse the non-optimized case. We'll see what happens in the optimized case soon.

- So it assigned three placeholders in memory with local unnamed variables, then it stores 0 again to one of them (as it did last time!), then stores the two integers we defined to be added together.

- Then it loads the two defined values into two new locations and calls `add` on them. The nsw keyword stands for `no signed wrap` which if specified means that the result value of the add is a poison value if signed overflow occurs. 

Basically its saying that this addition is not protected from signed overflows.

- Then it does the same things as before and prints it out. You can see printf calling `%6` this time! Compare that with the older vanilla printf:

```c
%2 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i64 0, i64 0))
```
No arguments at all!

## The third program (with optimizations enabled)

Let's try to see the optimizations now, what happens if I write a recursive function and let it perform a Tail call optimisation?

```c
#include <stdio.h>

int notailfib (int n) {
	if (n == 0) {
		return 0;
	} else if (n == 1) {
		return 1;
	} else {
		return (notailfib(n-1) + notailfib(n-2));
	};
}


int rec (int n, int acc1, int acc2) {
	if (n == 0){
		return acc1;
	} else if (n==1){
		return acc2;
	} else {
		return rec (n-1, acc2, acc2+acc1);
	}
}

int tailfib (int n) {
	int a = rec(n, 0, 1);
	return a;
}

int main () {
	int n = 15;
	int c = notailfib(n);
	int d = tailfib(n);
	printf("This is the %dth fib number (notail): %d\n", n, c);
	printf("This is the %dth fib number (tail): %d\n", n, d);
}
```

So this is the program I have, slightly more complex but nothing over the top. Thanks to OCaml for making my understanding of creating tail-recursive functions clear. 

So now this should TCO the tailfib function but not the notailfib. If you're struck with what TCO means then checkout my blog on that. Anyway, it simply means that instead of "calling the function" (as in a `call` operand in assembly) which takes up more overhead in the stack, we perform a "jump" because after all the function is already defined and when we write a recursive loop, a JUMP is what we MEAN.

Jumps are faster than calls, so that's the optimization. Let's see what clang does (note that we'll have to compile this with optimizations enabled as it won't do it by default)

```c
; ModuleID = 'fib.c'
source_filename = "fib.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [42 x i8] c"This is the %dth fib number (notail): %d\0A\00", align 1
@.str.1 = private unnamed_addr constant [40 x i8] c"This is the %dth fib number (tail): %d\0A\00", align 1

; Function Attrs: nofree nosync nounwind readnone uwtable
define dso_local i32 @notailfib(i32 noundef %0) local_unnamed_addr #0 {
  br label %2

2:                                                ; preds = %6, %1
  %3 = phi i32 [ 0, %1 ], [ %10, %6 ]
  %4 = phi i32 [ %0, %1 ], [ %9, %6 ]
  %5 = icmp ult i32 %4, 2
  br i1 %5, label %11, label %6

6:                                                ; preds = %2
  %7 = add nsw i32 %4, -1
  %8 = tail call i32 @notailfib(i32 noundef %7)
  %9 = add nsw i32 %4, -2
  %10 = add nsw i32 %8, %3
  br label %2

11:                                               ; preds = %2
  %12 = add nsw i32 %4, %3
  ret i32 %12
}

; Function Attrs: nofree nosync nounwind readnone uwtable
define dso_local i32 @rec(i32 noundef %0, i32 noundef %1, i32 noundef %2) local_unnamed_addr #0 {
  br label %4

4:                                                ; preds = %8, %3
  %5 = phi i32 [ %0, %3 ], [ %9, %8 ]
  %6 = phi i32 [ %1, %3 ], [ %7, %8 ]
  %7 = phi i32 [ %2, %3 ], [ %10, %8 ]
  switch i32 %5, label %8 [
    i32 0, label %11
    i32 1, label %12
  ]

8:                                                ; preds = %4
  %9 = add nsw i32 %5, -1
  %10 = add nsw i32 %7, %6
  br label %4

11:                                               ; preds = %4
  br label %12

12:                                               ; preds = %4, %11
  %13 = phi i32 [ %6, %11 ], [ %7, %4 ]
  ret i32 %13
}

; Function Attrs: nofree norecurse nosync nounwind readnone uwtable
define dso_local i32 @tailfib(i32 noundef %0) local_unnamed_addr #1 {
  br label %2

2:                                                ; preds = %6, %1
  %3 = phi i32 [ %0, %1 ], [ %7, %6 ]
  %4 = phi i32 [ 0, %1 ], [ %5, %6 ]
  %5 = phi i32 [ 1, %1 ], [ %8, %6 ]
  switch i32 %3, label %6 [
    i32 0, label %10
    i32 1, label %9
  ]

6:                                                ; preds = %2
  %7 = add nsw i32 %3, -1
  %8 = add nsw i32 %5, %4
  br label %2

9:                                                ; preds = %2
  br label %10

10:                                               ; preds = %2, %9
  %11 = phi i32 [ %5, %9 ], [ %4, %2 ]
  ret i32 %11
}

; Function Attrs: nofree nounwind uwtable
define dso_local i32 @main() local_unnamed_addr #2 {
  %1 = tail call i32 @notailfib(i32 noundef 15)
  %2 = tail call i32 (i8*, ...) @printf(i8* noundef nonnull dereferenceable(1) getelementptr inbounds ([42 x i8], [42 x i8]* @.str, i64 0, i64 0), i32 noundef 15, i32 noundef %1)
  %3 = tail call i32 (i8*, ...) @printf(i8* noundef nonnull dereferenceable(1) getelementptr inbounds ([40 x i8], [40 x i8]* @.str.1, i64 0, i64 0), i32 noundef 15, i32 noundef 610)
  ret i32 0
}

; Function Attrs: nofree nounwind
declare noundef i32 @printf(i8* nocapture noundef readonly, ...) local_unnamed_addr #3

attributes #0 = { nofree nosync nounwind readnone uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree norecurse nosync nounwind readnone uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nofree nounwind uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nofree nounwind "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
```

### Analysis

Let's first look at the `notailfib`:

```c
define dso_local i32 @notailfib(i32 noundef %0) local_unnamed_addr #0 {
  br label %2

2:                                                ; preds = %6, %1
  %3 = phi i32 [ 0, %1 ], [ %10, %6 ]
  %4 = phi i32 [ %0, %1 ], [ %9, %6 ]
  %5 = icmp ult i32 %4, 2
  br i1 %5, label %11, label %6

6:                                                ; preds = %2
  %7 = add nsw i32 %4, -1
  %8 = tail call i32 @notailfib(i32 noundef %7)
  %9 = add nsw i32 %4, -2
  %10 = add nsw i32 %8, %3
  br label %2

11:                                               ; preds = %2
  %12 = add nsw i32 %4, %3
  ret i32 %12
}
```

- The old syntax of a global variable definition (`@`) is there, along with the `dso_local` declaration.
- This time the function takes in a parameter which is a local unname variable (`%0`).
- For the `br` instruction you can choose to [read the documentation](https://llvm.org/docs/LangRef.html#br-instruction) or my simple explanation: The way it is being used here, its an **unconditional** branch to a label identified as `2`.

So the program will start at the label 2, let's see what it does from there on:

```c
2:                                                ; preds = %6, %1
  %3 = phi i32 [ 0, %1 ], [ %10, %6 ]
  %4 = phi i32 [ %0, %1 ], [ %9, %6 ]
  %5 = icmp ult i32 %4, 2
  br i1 %5, label %11, label %6
```

- For the `phi` instruction, you can again choose to read the docs, or simply understand the semantics that at runtime, the `phi` instruction logically takes on the value specified by the pair corresponding to the predecessor basic block that executed just prior to the current block.

- In other words, it allows for you to dynamically update a variable AND reference that in the next turn. Usually used in case of loops or recursive functions!

This is an example from the docs:

```c
Loop:       ; Infinite loop that counts from 0 on up...
  %indvar = phi i32 [ 0, %LoopHeader ], [ %nextindvar, %Loop ]
  %nextindvar = add i32 %indvar, 1
  br label %Loop
```

Note that something interesting has happened here. If you look at branch `%6`, there is a "tail call" there, this is because LLVM managed to perform TCO for one of the two recursive calls! 

```c
%3 = phi i32 [ 0, %1 ], [ %10, %6 ]
```

So, this is telling us that **if** coming from `%1`, deifined inside main like this:

```c
%1 = tail call i32 @notailfib(i32 noundef 15)
```

then `%3` will take a 0, otherwise if coming from `%6`, `%3` will take the value of `%10`. We'll worry about `%10` in just a minute. So, similarly we have `%4` also defined, and finally `%5` compares `%4` to 2 and decides to branch based on the value of `%5`, either to `%11` or `%6`.

What this means is, if `%4` is less than 2, we branch to `%11`, which returns a sum of `%4` and `%3`. This is the base case btw, which will become clearer as we explore what `%3` actually is. This implies that `%4` is actually the number we enter `n`.

Note that this is not very different from reading assembly, in fact, this can be a very good material to learn assembly! Anyways, let's say we head to %6 from the above branching, what happens then?

```c
6:                                                ; preds = %2
  %7 = add nsw i32 %4, -1
  %8 = tail call i32 @notailfib(i32 noundef %7)
  %9 = add nsw i32 %4, -2
  %10 = add nsw i32 %8, %3
  br label %2
```

- First thing to notice is that this branches unconditionally to `%2`. We decrement the `%4` value (remember that this will be populated from the `%2` block), and this should remind you about `notailfib (n-1)` because the next line does exactly that!

- Notice how LLVM is flagging this as a tail-call? As I said earlier, it looks like the compiler figured out a way to make 1 recursive call into a loop.

- Then we do `n-2` and store that in `%9` and we take the value we got from `notailfib (n-1)` and add that to `%3`. And `%3` if you recall is either 0 or `%10` (which is this value we're currently setting) depending on where it comes from. 

- Since right now it comes from `%6`, the value of `%3` will be `%10`. Now we go back to the %2 block and again check our base case while evaluating on `(n-2)` instead of `n` (why? Because `%4` will pick up the value of `%9` which was `n-2`).

So essentially the compiler figured out that we can loop for `n-2` and call the function for `n-1` which is better than calling for both!

Okay now equipped with this you can probably trace out the entire flow for this function given the input 15. Its a fun exercise! I will move on to the tail recursive function now:

```c
define dso_local i32 @rec(i32 noundef %0, i32 noundef %1, i32 noundef %2) local_unnamed_addr #0 {
  br label %4

4:                                                ; preds = %8, %3
  %5 = phi i32 [ %0, %3 ], [ %9, %8 ]
  %6 = phi i32 [ %1, %3 ], [ %7, %8 ]
  %7 = phi i32 [ %2, %3 ], [ %10, %8 ]
  switch i32 %5, label %8 [
    i32 0, label %11
    i32 1, label %12
  ]

8:                                                ; preds = %4
  %9 = add nsw i32 %5, -1
  %10 = add nsw i32 %7, %6
  br label %4

11:                                               ; preds = %4
  br label %12

12:                                               ; preds = %4, %11
  %13 = phi i32 [ %6, %11 ], [ %7, %4 ]
  ret i32 %13
}
```

Lets first look at `rec` and then we'll talk about what `tailfib` does. Let's not go over the full flow of the program again, but talk about only the differences:

1. This is using a `switch` to handle the 0 and 1 case. Is this more efficient than a simple `icmp ult`? An `icmp` is essentially an if-else equivalent and a switch is faster IF the number of entries in the jump table are large enough to justify it.
In this case, the choice is arbitrary in my opinion and won't really optimize or fuck the code.

2. There are no function calls!

This is a complete loop with no recursive function calls at all. This is the exactly what **TCO** promises us!

And if we checkout the `tailfib` function we'll see that its pretty much the same thing. Why? Because the compiler is smart! It figured out that we're calling `rec()` inside the failfib function and doing nothing else, so it substituted the entire code for `rec` inside it with the right params so there is no function call overhead!

Okay, so with that, we have come to an end of our discussion on LLVM IR. It has been fun and entertaining and I got to learn something new.
