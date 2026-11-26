+++
title = "Testing OpenNCB through AMBA CHI specs"
date = 2026-11-26
draft = false

[taxonomies]
categories = ["Hardware"]
tags = ["blog"]

[extra]
lang = "en"
+++

## Introduction

[OpenNCB](https://github.com/OpenXiangShan/OpenNCB) is a `CHI SN-F to AXI4` bridge. Both (that is, `CHI` and `AXI4`) of these are `AMBA` (Advanced Microcontroller Bus Architecture) protocols, which basically means they come from the same family.

`AMBA` is Arm's family of open specs for how blocks talk to each other on a chip. By blocks we mean CPU clusters, caches, DMA enginers, peripherals etc. There are multiple different **protocols** within AMBA:

- [x] `APB`: Used for simple slow peripherals (UART, GPIO, timer registers)
- [x] `AHB`: Small microcontroller-class buses, connecting to sensors for example
- [x] `AXI3/AXI4/AXI5` (Advanced eXtensible Interface): General high-performance memory-mapped point-to-point links.

Note: here memory-mapped means that hardware registers, control/status interfaces, and external memory live inside a shared, unified physical address space, and a **master** accesses them using standard read and write transactions with a target address. This is load-store style read and write.

- [x] `ACE`: Extends AXI such that multiple caching masters like CPU cores, can share a unified view of memory without stale cache lines. We need this because in multi-core processing, the cache lines can be dirty (old) and without visibility it's a losing battle.
- [x] `CHI`: Packet-based, layered coherent interconnect for many-core, mesh-style SoCs.

`CHI` stands for "Coherent Hub Interface" which is the latest in this long line and AXI4 is a little older but still widely use for memorry devices like DDR. So, if your new multi-core CPU (multi-cores are where the 2D mesh structure of CHI pays off) wants to talk to your DDR4, it gotta convert its messages from one protocol to another.

A specific part of that is what OpenNCB does, in chisel! Now let's look what they individually mean and what a `conversion` would entail.

> What I am trying to do here, is see test this OpenNCB repo out. So, I want to find out ideas for what SHOULD be tested in the first place. I have it compiled to verilog and want to run it through verilator.

---

## AXI4

This guy uses 5 handshake channels.

Handshake channels are called so because the protocol uses "VALID" and "READY" bits which are driven by a SOURCE and DESTINATION respectively. It basically means that AXI4's `source` will pull VALID high and start sending data and HOLD it until READY is also high. Data transfer happens on a rising clock edge, when both are high. If any is not high, no data transfer happens.

AXI4 split's the read and write traffic. Remember, that this is P2P which means a `master` and a `slave`. A master will initiate the transaction and a slave will respond to it. So, the 5 channels are:

1. `AW` -> **Write Address** -> Master writes to slave. It just sends the address to which it's going to write stuff to, ID, type etc.

2. `W` -> **Write data** -> Master writes to slave. It sends the data.

3. `B` -> **Write response** -> Slave writes to master. It acknowledges the data. It also flags if there are problems.

4. `AR` -> **Read address** -> Master writes to slave. It tells the slave that we're gonna be reading from here.

5. `R` -> **Read data** -> Slave writes to master. It gives the data.

In general, with `AXI4` masters are 'CPU cores', 'PCIe controllers', 'GPUs/accelerators' etc. and typical slaves are 'DDR', 'SRAM', 'Peripheral blocks like UART, SPI, GPIO, timers' etc.

For us, the masters are all in the `CHI` network, while the slaves are in `AXI4`, so our bridge will get a CHI message from the masters there, convert it, give it to the slaves here (on channel `AW`, `W` or `AR` channels) and gets a response back in `AXI4` format that it must convert to `CHI` format and give to the required masters there (we'll see how that works too).

Now let's talk about `CHI`.

---

## CHI (Coherent Hub Interface)

I'll be reading the specs for this guy cause its fun. You can find it [here](https://kolegite.com/EE_library/datasheets_and_manuals/FPGA/AMBA/IHI0050E_a_amba_5_chi_architecture_spec.pdf) if you wanna follow along.

Now this guy is closer to a small network. So, there is no `master` or `slave` here, rather we have nodes and a network.

Its a "coherent" NOC protocol. NOC just means Network on Chip, its a packetized, switched network built directly on silicon to serve as an interconnect. We have analogies to a "router" and "switches" and flow control in here. There are a few topologies that the specs list, like a 2D mesh.

Its functionality is grouped within 3 layers:

1. `Protocol Layer` => Communicates via "**transaction messages**" => Operational at the Nodes, defines their behaviour with other nodes, eg. response types, protocol level flow control etc.
2. `Network Layer` => Communicates via "**packets**" => Converts the protocol message into network packets which includes figuring out what goes where to whom and how.
3. `Link Layer` => Communicates via "**flits**" => To provide flow control between network devices.

The "interconnect" itself is USUALLY a 2D mesh, each vertex is a Node and each edge is a wire that can transfer data following this protocol VIA a router. So, each vertex is really a `router + Node`. Henceforth, if I say ICN or mesh or interconnect, it all just means a 2D mesh. See this image for clarity:

{{ figure(src="assets/interconnect_mesh_image.png", alt="2D grid", caption="A typical 2D network with CHI") }}

Some important definitions:

- `Transactions` -> A single operation, either reads from memory or writes to memory.

- `Transaction messages` -> A Protocol layer term that defines the **granule-of-exchange** between two components. E.g. Request, Data Response, Snoop Request.

- `Packet` -> The **granule-of-transfer** over the interconnect between endpoints.

> A "Transaction message" can be made of one of more Packets and each packet contains routing information

- `Flit` -> A packet can be made up of one or more flits. In CHI however, all packets have EXACTLY 1 flit. This is the smallest **flow control unit**.

- `Requester` -> A component (OUTSIDE of the interconnected mesh) or a node (INSIDE the mesh) that starts a transaction by issuing a Request message. This component can either independently raise a request as in the former or do so as a side effect as in the latter. It's also called `Master`.

- `Completer` -> A component that responds to a transaction it receives from another component. This can be a Node (INSIDE the mesh) or an external component. This is also called `Slave`.

- `Protocol Credit` -> A guarantee, from a Completer that it will accept a transaction.
- `Link Layer Credit` -> A credit, or guarantee, that a flit will be accepted on the other side of the link. A Link layer Credit (L-Credit) is a credit for a single hop at the Link layer.

A few important nodes in the ICN (interconnected mesh):

- `RN`: Request Node. The requester that generates a protocol transaction.

There are 3 types of Request Nodes depending on what they request for:

    RN-F: Fully coherent Request Node: Can generate all kinds of transactions, has a hardware coherent cache, supports all snoop transactions
    
    RN-D: IO coherent Request Node with DVM support: Generates only a subset of transactions. Recieves DVM transaction responses from MN and has a hardware coherent cache.
    
    RN-I: IO coherent Request Node: Generates only a subset, no DVM responses recieved, no hardware coherent cache, no snoop transactions supported.

- [x] `HN`: Home Node. The completer that recieves the transaction from RN, and completes the required coherency action and returns a response.

There are of 3 types too:

    HN-F: Fully coherent Home Node. This is the boss man. The point of serialization (PoS), that manages order between memory requests and point of coherence (PoC) that manages coherency by snooping the required RN-Fs consolidating the snoop responses for a transaction, and sending a single response to the requesting RN.
    
    HN-I: Non-coherent Home Node. Processes a subset of responses. Cannot do snooping.
    
    MN: Misc Node. These are there in the ICN to recieve DVM messages from RN and return a response.

- [x] `SN`: Slave Node. A compelter that recieves a request from HN, completes the required action and returns a response.

These are of 2 types:

    SN-F: Slave node used for normal memory
    SN-I: Slave node for peripherals OR normal memory

If it looks like having two slave nodes defined this way are redundant, you're not wrong. I don't know why they did this.

> DVM (Distributed Virtual Memory) messages are there to keep virtual-to-physical address translations and instruction caches synchronized across multiple CPUs.

### Coherence

> Regions of memory are coherent if writes to the same memory location by two components are observable in the same order by all components.

The coherence protocol ensures that all masters observe the correct data value at any given address location by enforcing that no more than one copy exists whenever a store occurs to the location. After each store to a location, other masters can obtain a new copy of the data for their own local cache, to permit multiple cached copies to exist.

The masters are RNs which each have a local cache and there is an optional cache in the ICN. The slave does the diry work. Every write happens to a single memory location and then a copy is made available for masters to store in their own cache.

Now `cache lines` have some classification too. Cache lines here refer to contiguous block of bytes that a cache allocates, transfers, and tracks as a single unit. Under CHI protocol, it is supposed to be 64 bytes in size. These can be:

1. Valid/Invalid: Valid => This cache holds a valid copy of the cache line. Otherwise Invalid.
2. Unique/Shared: Unique => This cache line is present in ONLY this cache. Otherwise Shared (though it's existence in other caches is NOT guaranteed).
3. Clean/Dirty: Clean => A clean cache doesn't have to update main memory. Dirty => it must update main memory with this cache line.
4. Full/Partial/Empty: Full => This cache has all bytes valid. Partial => Some bytes valid. Empty => No bytes valid.

### Reading data

Reading data happens from 3 sources:

1. Optional cache within the ICN
2. Slave Node (which fetches it from Normal memory or peripherals) gives it to requester: `DMT` (Direct Memory Transfer) and `DWT` (Direct write-data transfer) where the slave node writes to memory.
3. Peer RN-F nodes (for snoops and coherency): `DCT` (Direct Cache Transfer)

---

## Back to the problem

With this knowledge, we can define the operation of OpenNCB better:

Its a "CHI SN-F -> AXI4" bridge that means, we're talking about a slave node that's used for normal memory access but this time the memory access is not so simple as it needs to talk to another device (like a DDR) which uses AXI4, so the slave node needs to be smart here and convert the message in a format that AXI4 can understand then reconvert it to CHI protocol transactions and give it back to the RN-F/HN-F depending on what kinda transfer was initiated (with DMT on, it goes directly to RN-F, else to HN-F).

We compiled the chisel to verilog, now we want to write test scripts. So the question is, what to test. The first things we want to test is whether the CHI parts are handled properly or not! So, jumping directly to the `SN-F` specifications, we'll see what is necessary for the protocol to work here and see if the code implements that.

Let's do this quickly. We have 4 **channels** in the `SN-F` side:

1. RXREQ: For inbound request
2. RXDAT: For inbound write data
3. TXRSP: For outbound response (responses from the completer which can be another slave)
4. TXDAT: For outbound data, like read data

Do these exist in OpenNCB? Yes they do!

{{ figure(src="assets/OpenNCB_repo_search_image.png", alt="search image", caption="Searching for these keywords") }}

In our case, we want to see how OpenNCB will do the following conversations:

1. `RXREQ` -> `AR/AW`: Recieve a CHI request and translate that to the AXI4 equivalent, either `AR` or `AW`.
2. `RXDAT` -> `W`: Write data that should be translated to the `W` channel message
3. `B` channel -> `TXRSP`: Convert the AXI4 response from `B` to a `TXRSP` response to send it to the ICN
4. `R` channel -> `TXDAT`: Convert the AXI4 read data at `R` to a `TXDAT` flit.

(See the channel definitions from the `AXI4` part above)

So, there must be some parser for RXREQ and a converter for RXREQ -> AR/AW for example. Let's analyze what the RXREQ structure looks like. This is a `Request field` and it has a LOTTTT of subfields fields inside of it. I'll name a few:

- `TgtID`: Target ID (of the node)
- `SrcID`: Source ID (of the node)
- `TxnID`: Transaction ID
- `ReturnNID`: Return Node ID (Who to send to the response to)
- `ReturnTxnID`: Return Transaction ID (A transaction request from Home to Slave also includes a ReturnTxnID field to convey the value of TxnID in the data response)
etc.

Similarly we have a bunch of IDs for **response fields** and **data fields**. So, where in OpenNCB is this translation happening?

Turns out that there are seperate chisel files doing exactly this. For example, I'll pull up the **RXREQ -> AXI4** translation code sitting inside `NCBUpstreamRXREQ.scala` (TRUNCATED for brevity)

```scala
    
    // Definitions ...
    io.queueAllocate.bits.info.QoS          := regRXREQ.flit.QoS.get
    io.queueAllocate.bits.info.TgtID        := regRXREQ.flit.TgtID.get
    io.queueAllocate.bits.info.SrcID        := regRXREQ.flit.SrcID.get
    ...

    // Convert to AXI4 operands
    if (!paramNCB.axiBurstAlwaysIncr)
        io.queueAllocate.bits.operand.axi.Addr  := regRXREQ.flit.Addr.get
    else
    {
        when (CHIFieldSize.Size1B.is(regRXREQ)) {
        if (paramNCB.axiBurstAlwaysIncr)
            io.queueAllocate.bits.operand.axi.Addr  := regRXREQ.flit.Addr.get

        io.queueAllocate.bits.operand.axi.Size  := AXI4FieldAxSIZE.Size1B.U
        io.queueAllocate.bits.operand.axi.Len   := 0.U

        if (!paramNCB.axiBurstAlwaysIncr)
            io.queueAllocate.bits.operand.axi.Burst := AXI4FieldAxBURST.FIXED.U
        else
            io.queueAllocate.bits.operand.axi.Burst := AXI4FieldAxBURST.INCR.U
        }.elsewhen{...}
       ...
       ...
    }
```

It's all exactly there! Nice. And we have 4 such files: 

- NCBUpstreamRXREQ.scala
- NCBUpstreamRXDAT.scala
- NCBUpstreamTXDAT.scala
- NCBUpstreamTXRSP.scala

Which confirms that atleast in principle this seems to be doing what we expected it to do. Anyway, this brings us back to the first few checks that we can perform on the verilog code in verilator, and that is "BASIC handling of input and response types". That includes request types, sizes, errors, ReadReceipt, PrefetchTgt, WriteDataCancel, link deactivation etc. These are also defined in the specs (duh) but I am not going to explain it here.

Okay maybe one liners:

`errors`: AXI SLVERR/DECERR -> CHI NDERR on reads (these are their respective error types) and on EWA=0 writes (this is a specific AXI4 condition)
`receipt`: ReadNoSnp with Order = Request Accepted -> ReadReceipt
`prefetch`: PrefetchTgt -> no response, no AXI traffic (According to spec, a PrefetchTgt should have no response!)
`WriteDataCancel`: WriteNoSnpPtl + WriteDataCancel -> Comp, no AXI write, memory unchanged
`link deactivation`: deactivate / reactivate the RX link, then full-concurrency traffic. See if it fucks up.

These are the CHI essentials. For testing the translation, all we gotta do is ensure that every CHI request gets its valid expected CHI response. If the translation works, this will happen. Else it won't! So, we don't have to go and test individual functions.

Lemme give a more concrete example. So, in the spec they have an example for "Normal memory 32-byte Read transaction from an unaligned address". Look at this image for the explaination I am about to give:

{{ figure(src="assets/misaligned_read_image.png", alt="Misaligned read", caption="Reading address is misaligned") }}

The following happens:

- A requester asks for a 32-byte data (`0b101`) from a particular memory address (`0x0078`).
- The 32-byte read is broken down into two 128-bit data flits over a 128-bit data bus.
- If the address asked by the requester is misaligned as in the example above (it asked for 32 byte data at `0x0078` which is in the middle of the 16-byte region), WE STILL RETURN the aligned 32-byte chunk under which it falls, in WRAP order.

That's what its trying to say. And this is something that the CHI part of the bridge should follow! So, we'll be testing that.

--- 

## Features

So, OpenNCB added `DMT` too! Remember that DMT is when the `SN-F` directly talks to the `RN-F` node. What does that mean for the bridge you may ask? Well, not a lot! The few things that change are the ReturnNIDs and that nothing should route via the Home Node. That's easy with code.

But we can test it as well. We just change the expected CHI response based on the Node IDs of the requester.

I wouldn't call other things features exactly but more like convinience thoings that can be tested. I'll list them down here:

1. `early_comp`: Data arrives while the AXI B (`B` is the write response channel in AXI) is still outstanding (and so an AXI write error cannot be reported); so we must wait

2. `order`: a newer read or write to a line waits on AXI until older writes to that line have their channel B; other lines are not held up

3. `depth`: If 15 transactions in flight on AXI, the 16th waits for a REQ link credit

So, we can test for these too.

---

## Issues

An issue popped up when I tested OpenNCB on verilator. Remember that misaligned memory access part? It doesn't work like its supposed to. The software just hung up, it must be a code bug which I am yet to investigate.

Claude says there are 3 more issues which I am not sure since I haven't found anything in the specs regarding them yet. I'll put up updates in a new post maybe.

---