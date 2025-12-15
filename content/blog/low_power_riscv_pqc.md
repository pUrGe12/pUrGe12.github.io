+++
title = "A Post-Quantum DTLS1.3 Handshake on bare-metal RISCV"
date = 2025-12-14
draft = false

[taxonomies]
categories = ["Hardware" ,"Homelab", "Networking"]
tags = ["DTLS", "PQC"]

[extra]
lang = "en"
+++

This year for InterIIT we had by the best solution (we got gold). This is a blog that explains how we did what we did.

## The challenge

The problem was to implement a DTLSv1.3 (The UDP version of TLSv1.3) in a bare-metal RISC-V simulation through post quantum KEMs and signature verification schemes. There are basically the following problems in doing this:

- [x] The sizes of the generated keys and certificates through PQC algorithms is very large
- [x] UDP default buffer size is 1500 bytes (called the MTU/PMTU)
- [x] We have only 2 rxbuffer slots (which means our sim can only hold 2 UDP packets at a time)

So, the certificates and keys were all fragmented, which later had to be corrected. Now this is allowed according to the [RFC9147](https://datatracker.ietf.org/doc/html/rfc9147) but it's a pain to deal with.

## The setup

- We're running the simulation on litex which is a python based simulator for emdedded systems, its pretty cool
- This is a `rv32im` machine, which means it can't do no floating point operations, so we need to be careful here
- `wolfssl` is a beast. It's a beautiful library in `C` which provides us all the necessary code for actually performing a DTLS handshake according to the RFC.

So the idea is the following:

1. Cross compile the wolfssl library for `rv32im`
2. Define a `user_settings.h` file for setting up the right flags to enable DTLSv1.3
3. We don't have a filesystem or a RNG so we'll have to figure that out
4. Measuring latency through `number of CPU cycles` taken for the handshake to be completed
5. Resuming a session without performing a handshake again after authentication has finished once before

---

Cross compiling wolfssl is a slight problem, firstly because we need to compile the `riscv` 32-bit toolkit. We compile and link all the wolfssl source code during the `make` process.

It was actually a lot of bull fuckery. I don't think I have the strength to write this now. Will do this later.