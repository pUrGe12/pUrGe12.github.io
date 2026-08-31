+++
title = "A Post-Quantum DTLS1.3 Handshake on bare-metal RISCV"
date = 2025-12-14
draft = false

[taxonomies]
categories = ["Hardware" ,"Homelab", "Networking"]
tags = ["DTLS", "PQC"]

[extra]
lang = "en"
banner = "assets/banners/low-power-riscv-pqc.jpg"
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

What follows is the report we submitted.

---

# Inter-IIT QTrinoLabs Report

## 1. Problem Understanding

The objective is to implement a DTLS 1.3 communication channel on a resource-constrained, bare-metal RISC-V (RV32IM) architecture simulated via LiteX. The implementation must integrate Post-Quantum Cryptography (PQC) primitives for both the Key Encapsulation Mechanism (KEM) and Digital Signatures. A critical requirement is the optimization of the cryptographic stack to minimize handshake latency and maximize data throughput within the constraints of the soft-core CPU.

## 2. Architecture and Design Approach

The client runs on a LiteX-simulated RISC-V (RV32IM) core at roughly 100 MHz (since in the meeting it was mentioned that we must use a minimum of 75MHz frequency), while the server executes on a modern x86 Linux machine, creating a pronounced performance imbalance. DTLS 1.3 communication is carried over Ethernet using LiteX's minimal UDP interface (`udp_send()`, `udp_callback()`, `udp_service()`). All handshake logic and cryptographic operations rely on WolfSSL and WolfCrypt, with post-quantum primitives integrated through ML-KEM-1024 (KEM) and ML-DSA-87 (signatures). Handshake latency is measured using CPU cycle counts from ARP completion to DTLS 1.3 session establishment.

*For a record on the analysis behind this approach, please refer to **Annexure 1.1**.*

## 3. PQC and Classical Algorithm Choices

The implementation uses the following cryptographic primitives:

- **KEM:** ML-KEM-1024 (Kyber)
- **Digital Signatures:** ML-DSA-87 (Dilithium Level 5)
- **AEAD:** ChaCha20–Poly1305
- **Hash Function:** SHA-256

All performance measurements and resource metrics reported in the following sections correspond to this configuration **unless stated otherwise**. For comparison, results for lower-cost variants (Kyber and Dilithium Level 1) are also included where relevant.

*For detailed rationale behind the choice of these algorithms, see **Annexure 1.2**.*

## 4. Firmware Design for RISC-V Bare-Metal

1. **Using ring buffers:** Incoming packets are stored in a ring buffer through a custom receive callback. The callback writes each received packet into the buffer, and our custom receive function—invoked internally by wolfSSL—retrieves the data from this buffer when needed.
2. **Interrupt timers:** We implement our interrupt timers which was important for session resumption.

## 5. Integration of WolfSSL/WolfCrypt

We opted for a direct source compilation strategy rather than linking a static `libwolfssl.a`. This allowed us to strip unused cipher suites at compile-time using preprocessor directives, significantly reducing the binary size.

*For the specific user_settings.h configuration and Makefile integration details, please refer to **Annexure 1.3**.*

## 6. Challenges and Solutions

- **MTU Constraints:** The 1500-byte MTU caused severe fragmentation for ML-KEM handshake messages. *Solution:* Enabled DTLS fragmentation and implemented timely ACK transmission to prevent server-side retransmissions.
- **Packet Loss Under Heavy Crypto Load:** Early handshake packets (EncryptedExtensions) required expensive decryption, and with only **two RX** slots on the SoC, packets were dropped. *Solution:* Added a ring-buffered receive path to decouple packet arrival from decryption.

  *Optional solution*: increase the nrxslots in the litex SoC.
- **Packet loss due to ARP:** The UDP rxslots were filled with ARP packets which caused additional packet losses. *Solution:* Since **udp_service** internally calls for a pending read to the ethernet slots, we called this function at strategic places to ensure that our buffers are available for handshake packets.
- **Alignment Requirements:** VexRiscV's memory logic requires strict alignment; misalignment caused hard-to-trace failures. *Solution:* Applied WolfSSL alignment macros to all allocated buffers. (see [`WOLFSSL_USE_ALIGN`](https://github.com/wolfSSL/wolfssl/blob/3062d152409c4d86f00cb13c65a9d6942e1ef86f/wolfcrypt/src/misc.c#L186))
- **Lack of RISC-V32 Optimizations:** WolfSSL's optimized assembly targets rv64 only and not rv32 which we had. *Solution:* Relied on compiler-based optimizations.
- **ACK Handling:** With slower ACKs (due to large processing time in the client side), the server retransmitted most handshake data repeatedly, causing large delays. *Solution:* Issued ACK packets as soon as the receive buffer was processed, as permitted by the RFC.
- **Source Modifications:** Due to some added flags in the WolfSSL build we had to define our own **TimeNowInMilliseconds()** function and make some modifications in the WolfSSL source code.

  *for more information on this, refer to Annexure 1.6*
- **Parameter Tuning and minimizing ROM:** We systemically stripped the required macro list to reduce the compiled binary size while ensuring maximum throughput.

Open bug in wolfssl: [KeyShare mismatch](https://github.com/wolfSSL/wolfssl/issues/9362) is not detected as wolfSSL does not raise errors for incorrect `useKeyShare()` configurations, causing handshakes to appear successful with invalid ML-KEM suite settings.

*For more information on the challenges and solutions, see **Annexure 1.4***

## 7. Security Considerations

- **Relay attacks:** Since we're implementing session resumption, it raises concerns for relay attacks where the PSK is spoofed and used within the TTL. To minimize this we've set the expiry time for session resumption at 5 minutes.
- Our use of **ChaCha20** cypher stream allows the implementation to be resistant to timing attacks because all crypto algorithms used are just ARX.
- **MLKEM's** [underlying assumption](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) is to keep secret the decapsulation key and shared secret key key. Since these keys are not stored locally and are encrypted in epoch 2, the implementation is resistant to this attack vector.

## 8. Performance Metrics

The following is a measurement of the clock cycles, the CipherSuite specifies the **MLKEM** and **MLDSA** levels, the syntax being (**MLKEM_version, MLDSA_version**). The CPU cycles for the DTLS handshake are written as (**establishment_cycles, resumption_cycles**). The Handshake times are written for (**establishment_time, resumption_time**) in **seconds**.

| CipherSuite | Handshake cycles | Handshake time |
|---|---|---|
| **(1024, 87)** | (40,017,198; 8,147,943) | (0.400, 0.081) |
| **(1024, 44)** | (23,617,691; 8,049,218) | (0.236, 0.080) |
| **(512, 87)** | (39,449,096; 8,137,365) | (0.394, 0.081) |
| **(512, 44)** | (21,008,301; 6,989,774) | (0.210, 0.069) |

*Table 1: Performance metrics for different cipher suites*

We established a DTLS Handshake using the industry standard MLKEM1024 and MLDSA87 crypto suites using **40 mil CPU cycles** for establishment and **8 mil CPU cycles** for resumption on litex.

*For comparison, a modern x86 machine without fpu takes **24 mil cycles** for the latter.*

Our best case was with **MLKEM512** and **MLDSA44** for which a handshake could be established using **21 mil CPU cycles** and resumption in **7 mil CPU cycles**.

1. **Max heap usage:** 122kb
2. **Max binary size:** 349kb
3. **Max throughput:** 860 kbps (for a 100MHz setting in Litex with client sending to server)
4. **CPU cycles for Encryption and decryption:** For decrypting 150 bytes of data on the client side, it takes approximately **38000 cycles** and this value is roughly the same for encrypting the same **150 bytes** (tested on **MLKEM1024** and **MLDSA87**)

*For further graphs and more details on how we calculated the metrics, please refer to **Annexure 1.5**.*

## 9. Support for Session Resumption

Session resumption allowed us to reduce the handshake time by **60-70%**. **0-RTT** early data allowed user payload transmission during the initial ClientHello, eliminating **one RTT** when reconnecting.

Implementing custom timing functions (due to **NO_ASN_TIME**) enabled stable ticket-age validation and prevented session-cache invalidation.

Optimizing the server with **WOLFSSL_DTLS13_NO_HRR_ON_RESUME** removed the HelloRetryRequest on compatible resumptions, further reducing overhead.

*For more information on this, please refer to **Annexure 1.6**.*

## 10. Low-Power RISC-V Optimisations

- **Link-Time and Linker Optimizations:** Enabled `-flto`, `-ffunction-sections`, and `-fdata-sections` along with `-Os` to allow whole-program optimization and minimize binary size.
- **Low-Power Idle via `wfi`:** Used the RISC-V `wfi` instruction to gate the CPU clock

*For details on compiler flags and memory access optimizations, please refer to **Annexure 1.7**.*

## 11. Custom simulated TRNG

We integrate a lightweight entropy source into the simulation by combining an LFSR-based hardware stub with a ChaCha8-based CSPRNG in software. When called using a custom flag, the entropy source is used for the random number generation.

*For more details on the simulated TRNG implementation, see **Annexure 1.8**.*

---

# Annexures

## Annexure 1.1: Architecture and Design Details

**Performance Asymmetry:** The client is in a single-threaded environment with a clock frequency of about 100MHz. This makes it orders of magnitude slower than the server which is running on an X86 Linux machine. This was deliberately done to replicate a real world scenario.

This disparity creates a severe computational bottleneck during DTLS 1.3 handshakes, particularly when using post-quantum primitives. As a result, the crylptographic routines and network-processing paths must be aggressively optimized to avoid retransmissions, watchdog resets, and handshake timeouts.

**RISC-V Toolchain:** The bare-metal client firmware is built using a custom RV32IM toolchain configured with: `./configure --prefix=/opt/riscv --with-arch=rv32im --with-abi=ilp32`. This configuration produces compact 32-bit binaries suited to the limited instruction set and memory footprint of the simulated soft-core.

*For the simulated TRNG implementation, please refer to **Annexure 1.8**.*

## Annexure 1.2: Algorithm Selection Rationale

The cryptographic primitives used in this work are selected to comply with the emerging post-quantum security landscape defined by NIST. In particular, the Key Encapsulation Mechanism (KEM) must follow the NIST-standardized algorithms published in FIPS 203, "Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM)" ([Federal Register Announcement](https://www.federalregister.gov/documents/2024/08/14/2024-17956/announcing-issuance-of-federal-information-processing-standards-fips-fips-203-module-lattice-based)). The ML-KEM family consists of three parameter sets (512, 768, and 1024), formally defined in Section 8 of the specification ([FIPS 203 PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)). In addition, NIST has recently selected the HQC algorithm as a secondary or "fallback" post-quantum KEM ([NIST Announcement](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption)), though ML-KEM remains the preferred primary mechanism for interoperability and compatibility within standardized protocols such as TLS/DTLS 1.3.

Among the available ML-KEM parameter sets, **ML-KEM-1024** provides the highest security strength. Its larger keys and ciphertexts impose additional computational and network overhead, but its security justify this choice for a DTLS 1.3 channel.

For authentication, we use the **ML-DSA** (Dilithium) family, standardized by NIST as the primary post-quantum signature scheme. The three security levels—ML-DSA-44 (Level 2), ML-DSA-65 (Level 3), and ML-DSA-87 (Level 5)—offer progressively stronger protection. We select **ML-DSA-87** to maintain consistency with the high-security ML-KEM-1024 KEM. However, this choice results in **substantially larger artifacts**: the signatures (4627 bytes) significantly increase handshake message sizes. Consequently, DTLS 1.3 fragmentation and retransmission handling become essential to ensure handshake reliability on a constrained RISC-V client.

Additionally, we had the option of using [Falcon](https://en.wikipedia.org/wiki/Falcon_(signature_scheme)) instead of Dilithium but Falcon relies on floating point operations as well, hence we did not go ahead with that.

**ChaCha20–Poly1305** is chosen as the AEAD cipher due to its efficiency on embedded and software-only environments. Unlike AES-GCM, which is competitive only when hardware acceleration is available, ChaCha20 exhibits uniform performance on low-frequency RISC-V cores. Its use reduces the overall handshake cycles by approx imately half compared to AES-GCM.

**SHA-256** remains the standard selection for hashing, supporting HKDF, transcript hashing, and integrity guarantees.

| Algorithm | Type | Rationale |
|---|---|---|
| ML-KEM-1024 | KEM | NIST-standardized (FIPS 203) highest-security parameter set; provides Level 5 protection. Larger key and ciphertext sizes (e.g., 1568-byte pk) increase fragmentation, but ensure long-term post-quantum confidentiality. |
| ML-DSA-87 | Signature | NIST-selected Level 5 signature scheme. Strongest security configuration (256-bit). Large artifacts (4.9 kB sk, 2.6 kB pk, 4.6 kB signatures) require careful DTLS 1.3 fragmentation and retransmission handling. |
| ChaCha20–Poly1305 | AEAD Cipher | Significantly faster than AES-GCM on software-only embedded CPUs; reduces per-record cycle cost by nearly half. Optimal choice for a RV32IM soft-core lacking AES acceleration. |
| SHA-256 | Hash | Widely standardized and required for DTLS 1.3 transcript hashing and HKDF. Lowest-complexity member of the SHA-2 family and fits comfortably in constrained RISC-V environments. |

*Table 2: Selected Cryptographic Primitives and Rationale*

## Annexure 1.3: WolfSSL Configuration (user_settings.h)

To integrate WolfSSL, we defined `WOLFSSL_USER_SETTINGS` in the Makefile and created the following configuration:

```c
#ifndef USER_SETTINGS_H
#define USER_SETTINGS_H
#include <sys/types.h>
#define WOLFSSL_SP_MATH_ALL // maths backend for crypto
#define NO_TIME_H // Disable all time related imports
#define WOLFSSL_NO_CLOCK // Disable clocks
#define NO_ASN_TIME // Disable certificate "time" validation
#define HAVE_SECURE_RENEGOTIATION // Force client Initiated Secure Renegotiation
#define WOLFSSL_SEND_HRR_COOKIE // Important for resumption
#define WOLFSSL_TLS13 // TLSv1.3 related functions
#define WOLFSSL_DTLS // DTLS related functions
#define WOLFSSL_DTLS13 // DTLS1.3 specific functions
#define WOLFSSL_DTLS_MTU    // MTU support functions for DTLS
#define WOLFSSL_DTLS_CH_FRAG // Allowing for framgmentation in Client Hello
#define WOLFSSL_NO_SOCK // Disable built in BSD sockets
#define NO_WRITEV // We don't have <sys/uio.h>
#define HAVE_TLS_EXTENSIONS // Extensions to specify cipher suites, important for DTLS1.3
#define HAVE_SUPPORTED_CURVES // For cryptography
#define WC_32BIT_CPU // Enable 32 bit optimisations
#define WOLFSSL_NO_TLS12    // Strictly disable TLS1.2
#define WOLFSSL_USER_IO      // Defining our own IO through Litex
#define WOLFSSL_SMALL_STACK       // Optimize for small stack usage
#define WOLFSSL_SMALL_CERT_VERIFY // Lower memory certificate verification
#define NO_FILESYSTEM              // Don't use file system
#define NO_WOLFSSL_DIR             // Don't use directory access
#define SINGLE_THREADED // No threading support needed
#define WOLFSSL_SMALL_SESSION_CACHE // Smaller session cache
#define NO_OLD_TLS                   // Only support TLS 1.2+
#define NO_DH                        // Disable DH to save space
#define WOLFSSL_API_PREFIX_MAP    // Enforces wolfssl compiler time optimsations
#define WOLFSSL_SHA256    // Using SHA256 for hashes
#define WOLFSSL_USE_ALIGN // Important for VexRiscV's memory alignment
#define NO_RSA        // Strictly disabling RSA because
#define HAVE_CHACHA // Enable ChaCha20 for cipher stream
#define HAVE_POLY1305 // Enable Poly1305 for AEAD support
#define HAVE_DILITHIUM     // For dilithium certificate verification
#define WOLFSSL_WC_MLKEM // Enables some MLKEM functions
#define WOLFSSL_HAVE_MLKEM // Also enabled some MLKEM functions
#define WOLFSSL_ALLOW_NO_SUITES    // Fixing compiler error during building ssl.c
#define WOLFSSL_HAVE_KYBER // enable ML-KEM in wolfSSL
#define WOLFSSL_SHA3        // ML-KEM uses SHA3/SHAKE
#define WOLFSSL_SHAKE256     // Used by MLKEM functions
#define WOLFSSL_SHAKE128    // Used by MLKEM functions
#define NO_DEV_URANDOM    // Disable /dev/urandom (we don't have a filesystem)
#define WOLFSSL_MLKEM_CACHE_A    // Caches for MLKEM, speeds processing
#define HAVE_HKDF   // For key derivation
#define WOLFSSL_AEAD_ONLY    // Define AEAD functions
#define WOLFSSL_KEY_GEN // For key generation
#define WOLFSSL_WC_DILITHIUM    // Enables some dilithium functions
#define NO_DES3 // Deprecated security system
// Disabling all deprecated/vulnerable security systems
#define NO_DSA
#define NO_MD4
#define NO_MD5
#define NO_SHA
#define NO_PWDBASED
#define NO_RC4
#define WC_NO_RSA_OAEP
#define NO_CAMELLIA_CBC
#define NO_DH // Remove Diffie-hellman (we're using post quantum suites)
#define NO_OLD_SSL_NAMES
#define NO_OLD_WC_NAMES
#define NO_OLD_POLY1305 // Use the latest poly1305 code
#define NO_HANDSHAKE_DONE_CB // useful for reducing code size according to wolfssl manual pg. 26
#define NO_TLS_DH   // Not using Diffie-Hellman in TLS
#define NO_WOLFSSL_CM_VERIFY // useful for reducing code size accoding to wolfssl manual pg. 26
#define NO_WOLFSSL_RENESAS_TSIP_TLS_SESSION // We don't need this
#define WOLFSSL_NO_CLIENT_AUTH // Disables the caching code required for using Ed25519 and Ed448
// #define WOLFSSL_SP_
#define WOLFSSL_MLKEM_INVNTT_UNROLL // Enables an alternative inverse NTT implementation
#define WOLFSSL_SP_FAST_NCT_EXPTMOD  // Enables the faster non-constant time modular exponentiation implementation
#define SP_WORD_SIZE 32
extern int CustomRngGenerateBlock(unsigned char *, unsigned int);
#define CUSTOM_RAND_GENERATE_SEED CustomRngGenerateBlock
#define WC_NO_ASYNC_THREADING // Disable all forms of async code
#define WOLFSSL_STATIC_MEMORY // Good for bare-metal
#endif
```

We added the following sources in the Makefile to compile all the wolfssl/wolfcrypt source code and link it to our binary

```make
SRCS += $(wildcard wolfssl/wolfcrypt/src/*.c)
SRCS += $(wildcard src/*.c) #our src files
SRCS += $(wildcard wolfssl/src/*.c)
```

This approach also allowed us to reduce the compiled binary size by simply deleting source files in wolfssl/wolfcrypt libraries which we did not use.

## Annexure 1.4: Additional Challenges and Solutions

- **Limited Ethernet Buffers:** The Ethernet interface exposed only two RX buffers, which frequently became saturated with ARP packets. This prevented our application packets from being received in time. We resolved this by invoking `udp_service()` at specific points in the control flow, ensuring timely buffer draining.

- **wolfSSL Documentation Gaps:** Several wolfSSL configuration macros lacked proper documentation, and the examples provided in both the website and the manual often conflicted with the actual source code. Key functions such as `LowResTimer` and `TimeNowInMilliseconds` were referenced but never defined, leaving their implementation entirely to the user with no guidance. Critical flags were also undocumented; missing them caused internal wolfSSL functions to fail silently. These had to be discovered and enabled manually.

- **LiteX Simulation Throughput Issues:** The LiteX simulation environment is significantly slower than real hardware. As a result, our `udp_service()` routine could not process more than two consecutive packets sent by the server. To mitigate this, we throttled the server's transmission rate by inserting a `usleep()` delay into the packet-send path in `internal.c`, allowing the simulated client enough time to drain buffers and maintain correctness.

## Annexure 1.5: Performance Metrics & Methodology

Here we describe the methodology for computing the metrics

### Calculating CPU cycles

The 64-bit CPU cycle counter is read from the `mycycle` (lower 32 bits) and `mycycleh` (upper 32 bits) registers.

```c
uint64_t get_cpu_cycles(void) {
  uint32_t h, l, h_check;
  do {
    asm volatile("csrr %0, mcycleh" : "=r"(h));
    asm volatile("csrr %0, mcycle" : "=r"(l));
    asm volatile("csrr %0, mcycleh" : "=r"(h_check));
  } while (h != h_check);
  return ((uint64_t)h << 32) | l;
}
```

We calculate the difference in the cycle counts for three cases:

1. The entire handshake (since the Client Hello to the session establishment)
2. Processing individual PQ computation parts (during Client Hello and Server Hello)
3. Processing back-and-forth encryption and decryption after session establishment

See the **firmware/benchmark.c** file for the code

### Calculating Heap usage

WolfSSL allows us to pass in custom allocator functions via the use of **wolfSSL_SetAllocators**, passing in functions corresponding to malloc, free and realloc. In our case to measure the heap usage, our custom_malloc modifies a static variable called "current_heap" which is incremented by the size passed to the malloc on every call, thus effectively tracking the heap usage during the handshake. Similarly we implement the logic for free-s and realloc-s, and then we can track the heap usage throughout the program.

See the **firmware** directory for the code

### Calculating throughput

We store the cpu cycle counter before the **wolfSSL_write()** function using the **get_cpu_cycle()**. We again find the cpu cycle counter after the function finishes. Now the difference between these values is the number of cycles taken to send a particular payload to the server.

We calculate the number of cycles taken for payloads of varying sizes from 1 byte to 300 bytes. When we plot this we approximately get a straight line with an offset (due to common computations being done there is an offset). We removed the offset to only account for the changes in the number of bytes transmitted. Now we divide this value by the frequency to find the time taken for a particular size of payload to be transmitted.

To find the throughput, we need to divide the size of payload by the time taken. We calculate this value which turns out to be **approximately constant and take the average**.

### Encryption-decryption cycle counts

To calculate the CPU cycles for encryption, we ran our benchmark for the **udp_send()** function and calculate the difference in this function. Another method to do this can be to add the benchmark for the specific **ChaCha20-Poly1305** functions inside WolfSSL.

## Annexure 1.6: Session Resumption Implementation

**Overview.** To support DTLS 1.3 session resumption and 0-RTT early data on a constrained LiteX-based platform, several build-time flags, timing implementations, and server-side adjustments were required. The primary goal was to reduce reconnection latency and allow data transmission without repeating a full handshake.

**Client configuration.** Session resumption required enabling session tickets and PSK support while avoiding flags that disable the cache. The client build defined: **NO_SESSION_CACHE_REF**, **BUILD_TLS_PSK_WITH_CHACHA20_POLY1305_SHA256**, and **HAVE_SESSION_TICKET**. Flags such as `NO_SESSION_CACHE` and `NO_PSK` were excluded to avoid disabling the resumption logic.

**Effects of `NO_ASN_TIME`.** Defining `NO_ASN_TIME` disables wolfSSL's built-in time-handling paths. The library conditionally undefines session-ticket functionality or forces `NO_SESSION_CACHE` when this flag is present. These behaviours are not documented clearly and required commenting out in `settings.h`. With `NO_ASN_TIME` defined, the platform must supply its own timing functions:

- `TimeNowInMilliseconds()` in `tls13.c`

  ```c
  // tls13.c
  #include <client/benchmark.h>
  // Return time in milliseconds
  sword64 TimeNowInMilliseconds(void){
      return (sword64)(get_cpu_cycles() / 100000);
  }
  ```

- `LowResTimer()` in `internal.c`

  ```c
  // internal.c
  #include <client/benchmark.h>
  word32 LowResTimer(void){
      return (word32)(get_cpu_cycles() / 100000000);
  }
  ```

Both were implemented using the RISC-V cycle counter at 100 MHz. Their accuracy directly affects ticket-age validation and session-ticket acceptance.

**Session management API.** Resumption used the modern session API:

- `wolfSSL_get1_session()` to obtain a persistent session object.
- `wolfSSL_set_session()` to apply it to a new connection attempt.
- `wolfSSL_SESSION_free()` to release the object after use.

The session is saved at disconnect and reused at the next user-initiated reconnect. No modifications were required to the resumption logic inside wolfSSL.

**Server build configuration.** The wolfSSL server was built with DTLS 1.3, session tickets, PSKs, and early data enabled. Additionally, the server was compiled with:

```
-DWOLFSSL_DTLS13_NO_HRR_ON_RESUME
```

to suppress HelloRetryRequest on compatible resumptions. This reduces one round trip, provided that the client's ClientHello fits both the PSK binder and a key-share without exceeding MTU. Larger KEM parameter sets may still force HRR due to fragmentation.

**Ticket hint and age tolerance.** The server validates the client's ticket age against its own timing source. On constrained hardware with coarse timing resolution, this check frequently rejected valid resumptions. The tolerance window in `internal.c` was increased to match the configured ticket hint, preventing unnecessary failures. Improving the timing source is preferable, but widening the tolerance was sufficient for stable operation.

**0-RTT early data.** Both client and server enabled early data using `WOLFSSL_EARLY_DATA`. The client transmitted its payload using `wolfSSL_write_early_data()`, and the server processed it with `wolfSSL_read_early_data()` during the handshake progression. The server additionally set a maximum early-data size via `wolfSSL_set_max_early_data()` to avoid fragmenting the initial ClientHello.

**Simulation constraints.** LiteX's simulation environment significantly slows packet processing. The DTLS pipeline could not consume packets fast enough unless application-level pacing was introduced. A temporary solution was adding a small `usleep()` delay on the server's transmit path to prevent packet bursts from overwhelming the simulated client.

**Result.** With these changes, the system performed reliable PSK-based DTLS 1.3 resumption, supported early data, maintained valid ticket-age handling using custom timing functions, and avoided unnecessary HelloRetryRequests where possible.

## Annexure 1.7: Low Power Optimizations

- **Link-Time and Linker Optimizations:** These flags place each function and zero-initialized object in its own section. Combined with `-Wl`,`--gc-sections`, the linker can remove unused code and data.

  With LTO, GCC embeds intermediate representation (GIMPLE) in the object files. During linking, the linker invokes the compiler to perform cross-module inlining and dead-code elimination using global visibility over all translation units. Although this increases compile time and memory usage, the host system comfortably handles the overhead. The linker script finally merges all generated `.text.*` and `.bss.*` sections into contiguous segments while retaining the size reductions achieved through dead-code pruning.

- **Low-Power Idle via `wfi`:** We used the RISC-V `wfi` instruction to gate the CPU clock until an interrupt arrives, lowering power consumption during idle periods. Since the design does not benefit from an Ethernet interrupt handler and enabling one could increase latency due to ISR overhead, the system continues to poll for Ethernet events. A periodic timer interrupt is used instead to exit `wfi`.

  ```c
  void Process_Pending_Packets(uint32_t timer) {
    while (ethmac_sram_writer_ev_pending_read() & ETHMAC_EV_SRAM_WRITER) {
      init_timer0(timer);
      udp_service();
      asm volatile("wfi");
      timer_stop();
    }
  }
  ```

## Annexure 1.8: Custom Entropy (TRNG) Integration

We implemented a simulated TRNG in the hardware, which pulls out its value from a Linear Feedback Shift Register (LFSR). The shift register updates its values after each clock cycle of the processor according to the following implementation:

```python
class EntropySource(LiteXModule):
    def __init__(self, platform):
        self.seed = CSRStatus(32, description="Raw Entropy for Seeding PRNG")
        if (platform is None) or (platform.device == "SIM"):
            fake_noise = Signal(32, reset=0x12345678)
            self.sync += [
                fake_noise.eq(Cat(fake_noise[1:],
                              fake_noise[31] ^ fake_noise[21] ^ fake_noise[1] ^ fake_noise[0])),
                self.seed.status.eq(fake_noise)
            ]
```

```c
// In main setup:
int CustomRngGenerateBlock(byte *output, word32 sz) {
    for (word32 i = 0; i < sz; i++) {
        output[i] = (byte)(abs(get_secure_random()));
    }
    return 0;
}
```

The LFSR is seeded with a constant seed in the hardware simulation. But in a practical system, the randomness is generated by natural noise. After each clock cycle it updates its internal values according to the above expression, the register values only repeat after an astronomically large number of clock cycles.

The value of this register can be accessed using the `entropy_seed_read()` function, which is generated in the `generated/csr.h` header during the simulation. The register value is used as the TRNG seed from the hardware. Then, the simulated TRNG seed is used to initialize ( and reinitialize ) ChaCha8, a Cryptographically Secure Random number Generator. For faster implementation, we buffer the value of ChaCha8 up to 16 values and then (after 16 cycles) update the internal state of ChaCha8, using the TRNG seed in the register at the next clock cycle.

ChaCha8 is implemented inside the function `get_secure_random()` and this function is called whenever the CustomRngGenerateBlock function is used by the wolfssl.

In a Real Hardware implementation we use a Ring Oscillator to provide the required Randomness.
