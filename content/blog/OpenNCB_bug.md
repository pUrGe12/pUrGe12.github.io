+++
title = "OpenNCB L-credit limit exceeds maximum"
date = 2026-11-28
draft = false

[taxonomies]
categories = ["Hardware", "systems"]
tags = ["blog"]

[extra]
lang = "en"
+++

Goodday. I had been trying to do some stuff with OpenNCB (related to compiling it to verilog and running tests) and in the process I hit upon this "bug". Its technically not a "bug" but a unimplemented spec.

I'll admit, this took longer than expected EVEN with AI assistance. Like what. I had a hard time getting into all the chisel mindset, but I think I did okay. Anyway, I have raised a [PR](https://github.com/OpenXiangShan/OpenNCB/pull/16) for this because I AM A GOOD GUY :). I have fixed and generated the verilog locally for my use case.

Let's start.

## Introduction

The maximum number of L-Credits that a receiver can provide is 15 -> Section 14.2.1, L-layer flow control, [AMBA CHI specs](https://kolegite.com/EE_library/datasheets_and_manuals/FPGA/AMBA/IHI0050E_a_amba_5_chi_architecture_spec.pdf).

There are a bunch of request params defined in the spec for L-credits. BTW, if you don't know what L-credits are, its just a guarantee that a recievier will accept a sender's data. Each L-credit corresponds to a single flit of data. These are two types of requests that the spec defines:

    REQLCRDV -> Request L-Credit Valid. The receiver sets this signal HIGH to return a request channel L-Credit to a transmitter

    RSPLCRDV -> Response L-Credit Valid. The receiver sets this signal HIGH to return a response channel L-Credit to a transmitter

Similarly for `snoop` but we're dealing with non-coherency here so that doesn't matter in OpenNCB.

Then the specs clearly say:

> An L-Credit is sent from the receiver to the transmitter by asserting the appropriate LCRDV signal for a single clock cycle. There is one LCRDV signal for each channel.

## Code analysis

With that let's look at the code. We're inside the `CHILinkCreditManagerRX`:

```scala
protected val logicLcrdv = ValidMux(io.linkState.run, Mux(logicInitialCreditDone,
            io.linkCreditProvide,
            logicInitialCycleEnd))
```

This is how it's defined. The `ValidMux` is defined as follows:
```scala
object ValidMux {

    def apply(valid: Bool, bit: Bool): Bool = 
        Mux(valid, bit, false.B)

    def apply[T <: Data](valid: Bool, bits: T): T =
        Mux(valid, bits, 0.U.asTypeOf(bits)) 
}
```

Scala lesson 101. Calling `ValidMux(a, b)` might seem odd because well, wtf does it even do! Turns out that its sugar for saying `ValidMux.apply(a, b)` which obviously makes sense. In general, when we put round brackets `()` right after an object, the compiler thinks of it as "object.apply(something)". It assumes the `.apply`.

Anyway, this tells us that `ValidMux` is indeed a boolean, and it returns the `bit`, the second argument iff the `valid` field is True, else it returns False. Same happens for LCRDV but with the `linkState.run` state as the `valid` condition.

The inner `Mux` is going to pick `io.linkCreditProvide` when `logicInitialCreditDone` is True or `logicInitialCycleEnd` when its False.

So, let's look at what this condition `logicInitialCreditDone` means:

```scala
    protected val logicInitialCycleEnd      = regInitialCycleCounter === paramCycleBeforeSend.U
    ...
    // Increment regInitialCycleCounter code
    ...

    protected val logicInitialCreditClear   = regInitialCreditCounter === paramInitialCount.U
    ...
    // Increment regInitialCreditCounter code
    ...

    protected val logicInitialCreditDone    = logicInitialCycleEnd && logicInitialCreditClear
```

So this is triggered when both `CycleEnd` and `CreditClear` is True, them as defined above. In a typical run, `logicInitialCreditDone` will be True after 15 credits have been issued because of the `CreditCounter`. That is, before the "initial burst" is done, the inner Mux will pick the `logicInitialCycleEnd` and after its done, (that's when `CreditDone` will be True), will it pick `io.linkCreditProvide`.

This means, after 15 credits in a normal run, `Mux(logicInitialCreditDone, io.linkCreditProvide, logicInitialCycleEnd)` is going to be `io.linkCreditProvide` and if the run is going on, then `io.linkState.run` will be True and the ValidMux will ALSO give `io.linkCreditProvide` which means,

```scala
protected val logicLcrdv = io.linkCreditProvide
```

is a valid state. Just to give you an idea, the linkState has the following params inside it:

```scala
class CHILinkActiveBundle extends Bundle {

    val stop            = Bool()    // STOP
    val activate        = Bool()    // ACT
    val run             = Bool()    // RUN
    val deactivate      = Bool()    // DEACT

    /*
    * Connects to CHI Link-Layer LINKACTIVE signals.
    * 
    * @param linkactive_req LINKACTIVEREQ
    * @param linkactive_ack LINKACTIVEACK
    */
    def from(linkactive_req: Bool, linkactive_ack: Bool) = {
        stop        := !linkactive_req && !linkactive_ack
        activate    :=  linkactive_req && !linkactive_ack
        run         :=  linkactive_req &&  linkactive_ack
        deactivate  := !linkactive_req &&  linkactive_ack
    }
}
```

This entire class is just the code representation of **specs 14.5.1**: "Request and Acknowledge handshake".

Then we create a 1-bit flip-flop that updates on every rising clock edge to match the `logicLcrdv` boolean value and resets to 0, and define the output of the module as this register value:

```scala
protected val regLcrdv  = RegNext(init = 0.B, next = logicLcrdv)
io.linkCreditReady := io.linkState.run && logicInitialCreditDone
io.lcrdv := regLcrdv
```

Okay, now come to where this is called and implemented. That's two places, `NCBUpstreamRXREQ` and `NCBUpstreamRXDAT`.

Let's walk through `NCBUpstreamRXDAT` first. We see that it calls the CreditManager:

```scala
protected val uLinkCredit   = Module(new CHILinkCreditManagerRX(
        paramCycleBeforeSend    = 0,
        paramEnableMonitor      = true
    ))
```

It uses the default value of `paramInitialCount` which is 15. Then it takes the output of this Module and assigns it inside its own register:

```scala
protected val regRXDAT  = RegInit(init = {
        val resetValue = Wire(io.rxdat.undirectedChiselType)
        resetValue.lcrdv    := false.B
        resetValue.flitpend := false.B
        resetValue.flitv    := false.B
        resetValue.flit     := DontCare
        resetValue
    })

...

regRXDAT.lcrdv := uLinkCredit.io.lcrdv
```

Then we see that it creates a `val` for a `ProvideBuffer`, and sets the `linkCreditProvide` value:

```scala
val uLinkCreditProvideBuffer = uLinkCredit.attachLinkCreditProvideBuffer()

// Implemented separately, attachLinkCreditProvideBuffer initializes this
class ProvideBuffer extends Module {
        /*
        * Module I/O 
        * 
        * @io input     linkCreditProvide       : Provide Link Credit.
        * 
        * @io output    outLinkCreditProvide    : Provide Link Credit, to manager.
        * @io input     outLinkCreditReady      : Provide Link ready, to manager.
        */
        val io = IO(new Bundle {
            // link credit provide input
            val linkCreditProvide       = Input(Bool())

            // link credit provide output to manager
            val outLinkCreditProvide    = Output(Bool())
            val outLinkCreditReady      = Input(Bool())
        })

uLinkCreditProvideBuffer.io.linkCreditProvide   := regRXDAT.flitv
```

But what is `regRXDAT.flitv` you may ask.

```scala
regRXDAT.flitv      := io.rxdat.flitv
when (io.rxdat.flitv) {
        regRXDAT.flit := io.rxdat.flit
    }
```

Its a flag, that we get every clock cycle and if its true, then we store that data. Okay, lets look at linkCreditProvide in a little more detail (I've kept only relevant sections of the code):

```scala
class ProvideBuffer extends Module {
    val io = IO(new Bundle {
        val linkCreditProvide       = Input(Bool())
        val outLinkCreditProvide    = Output(Bool())
        val outLinkCreditReady      = Input(Bool())
    })
    protected val logicBufferPushReady  = io.linkCreditProvide
    io.outLinkCreditProvide := !logicBufferEmpty

...

    def attach(uManager: CHILinkCreditManagerRX)    = {
        uManager.io.linkCreditProvide   := io.outLinkCreditProvide
        io.outLinkCreditReady           := uManager.io.linkCreditReady
        this
    }
```

Remember the `io.linkCreditReady` from the output of the Manager in the above snippets? It checked for currently running and `logicInitialCreditDone` both to be True. And `logicInitialCreditDone` was when `InitialCycleEnd` and `InitialCreditClear` which means we're DONE with the burst.

So, when `linkCreditReady` is True, the manager is saying that it can send the flits now.

Now, let's bring it home and look at the final moments:

1. The burst has just finished => `regInitialCreditCounter` = 15, so `logicInitialCreditClear` = 1. `logicInitialCycleEnd` is already 1, so `logicInitialCreditDone` = 1.
2. That switches the inner `Mux` from before to its other input as we talked about before. So, `Mux(logicInitialCreditDone, io.linkCreditProvide, logicInitialCycleEnd)` now picks `io.linkCreditProvide`.
3. `io.linkCreditProvide` on the manager is the buffer's output (via `attach()`) which means, `io.outLinkCreditProvide := !logicBufferEmpty`. But, `regBufferedCreditCounter != 0` which means its 1. This is because the counter still holds the 1 IOU from the LCrdReturn.

To see this, look at `NCBUpstreamRXDAT.scala`

```scala
protected val uLinkCredit   = Module(new CHILinkCreditManagerRX(
    paramCycleBeforeSend    = 0,
    paramEnableMonitor      = true
))

...

uLinkCredit.io.monitorCreditReturn  := logicLCrdReturn
uLinkCredit.io.monitorCreditConsume := regRXDAT.flitv
```

So this part of the code KNOWS that this is a "return" credit. But, what was provided:

```scala
uLinkCreditProvideBuffer.io.linkCreditProvide := regRXDAT.flitv
```

is ANY flit include a return one. That's why this problem happened with RXDAT!

Here's a short table to summarize the bug:

| phase | regInitialCreditCounter | regBufferedCreditCounter | lcrdv pulses | sender holds |
| --- | --- | --- | --- | --- |
| link up (RUN), burst | 0 → 15 | 0 | 15 | 15 |
| idle (RUN) | 15 | 0 | 0 | 15 |
| DEACTIVATE (1 cycle): DataLCrdReturn arrives, flitv=1 | reset → 0 | 0 → 1 (manager not ready, so the IOU is stored) | 0 | 14 (1 given back) |
| STOP | 0 | 1 | 0 | 0 (drops the other 14) |
| RUN again, burst | 0 → 15 | 1 (still waiting: linkCreditReady needs the burst done) | 15 | 15 |
| burst done, so linkCreditReady = 1 | 15 | 1 → 0 | 1 | 16 X|

And that's the bug! If you say, wait! How do we know that lcrdv pulses in that last step? Bear with.

BTW. if you look at `RXREQ`, that has `paramInitialCount` at 0:
```scala
protected val uLinkCredit   = Module(new CHILinkCreditManagerRX(
        paramInitialCount       = 0,
        paramCycleBeforeSend    = 0,                            // TODO: parameterize on demand
        paramEnableMonitor      = true
    ))
```
So, there are no bursts here! I am not sure if this is a bug too. I'll have to look into the specs for this, will do this later.

## The Fix

Just this in `NCBUpstreamRXDAT.scala`:

```scala
uLinkCreditProvideBuffer.io.linkCreditProvide := regRXDAT.flitv & !logicLCrdReturn
```

This is really it. You just ensure that you don't count any returned credits in here.

---