+++
title = "Understanding the Shakti microprocessor"
date = 2026-02-10
draft = false

[taxonomies]
categories = ["Hardware", "emulator"]
tags = ["blog"]

[extra]
lang = "en"
+++

So, I spend a few days diving deep into the shakti processor, specifically the one modified by Mindgrove into a secure-IOT chip called MGS2401. In this blog I just want to fight my demons and explain how thigns stand with Mindgrove's opensource repos and their documentation and my attempt at understanding them. Honestly, big cheers to Mindgrove for opensourcing all their code, it really shows how difficult and chaotic this world of development is.

## Part 1 -> The datasheets

[This](https://www.mindgrovetech.in/s2401-secure-iot) is the product I was targeting. Its the only chip sold by Mindgrove as of today. The [datasheet](https://corevoice.b-cdn.net/mindgrove/docs/MGS2401Q64CF8R16_datasheet.pdf) was last revised in April 2026 so its fairly recent (this is an important fact which I only realized later).

> Some overview

- Shakti-C-class 64-bit RISC-V core
- RV64GC
- 700 MHz clock frequency

> The peripherals

- 2xQSPI
- 2xSPI
- 1xI2C
- 5xUART
- 21xGPIO
- 7xPWM
- 1xADC
- 1xGPTimer
- 1xWatchdog Timer
- 1xPLIC
- 1xCLINT
- 1xDMA

Just to give some background on these things:

### Interrupt controls

Interrupts usually come about in three types:

1. Timers
2. Software
3. External (or global)

The interrupts through **timer** and **software** are handled by the `CLINT` (**Core Local INTerruptor**) while the global interrupts (due to **peripherals**) are handeled by the `PLIC`. The software interrupts are how one `hart` (**hardware thread**) pokes another (IPIs / **inter-processor interrupts**), or how a hart triggers itself.

The external interrupts are driven by other peripherals, all of which are listed above. The `PLIC` (**Platform Level Interrupt Controller**) is basically a device that has some interrupt gateways to the PLIC core. The core is responsible for **queuing** up the interrupts based on their priority and then do **arbitration** on the same. It will also manage and store completion events. Its basically a huge router + memory for interrupts.

> I am getting all this from [this documentation](https://shakti.org.in/docs/plic_user_manual.pdf) on PLIC.

If you're wondering what does it even mean for SPI to have interrupt handling (since SPI is a peripheral and it has a PLIC model), then you're right. It's kinda weird. SPI usually works through `DMA` (**Direct Memory Access**), but sometimes it can also be made to raise interrupts and ask for data/send data everytime it feels the need to. It's kinda wasteful to do that though. That's just one example, all other peripherals have some behaviour defined for the PLIC.

### What's C class?

The Shakti [user manual](https://shakti.org.in/docs/user_manual.pdf) has an answer to that question. It is an in-order 6 stage 64-bit micro controller supporting the **entire stable RISC-V ISA**. It is positioned against **ARM’s Cortex A35/A55**.

### Supported != Available

This was my first source of confusion. The datasheet mentions 5xUART in the overview, proceeds to define memory addresses for all 5 of them:

```
0x00011300 0x00011340 UART0 64
0x00011400 0x00011440 UART1 64
0x00011500 0x00011540 UART2 64
0x00011600 0x00011640 UART3 64
0x00011700 0x00011740 UART4 64
```

And then have only UART0, UART1, and UART2 in the pinout! I went ahead and checked the [driver code](https://github.com/FreeRTOS/FreeRTOS/compare/main...Mindgrove-Technologies:FreeRTOS:main.diff) for this here, which also defines only three UART lines (in this file: FreeRTOS/Demo/RISC-V_RV64_Secure-IoT/secure-iot.h):

```c
#define MAX_UART_COUNT 3

#define UART0_START 0x00011300 /*! UART 0 */
#define UART0_END 0x00011340 /*! UART 0 */

#define UART1_START 0x00011400 /*! UART 1 */
#define UART1_END 0x00011440 /*! UART 1 */

#define UART2_START 0x00011500 /*! UART 2 */
#define UART2_END 0x00011540 /*! UART 2 */
```

Turns out that this is fairly common. The support exists for 5 UART lines, but 3 actual have pins so support exists for 3 only. Unless...

If you look closely at the last commit on the github diff I shared above, it was made on 20th May 2024. That's 2 years before the latest documentation came out which probably means that the code I am looking at is obselete! This deviation was further enchanced, when I looked at the driver code for I2C:

```c
#define MAX_I2C_COUNT 2
#define I2C0_BASE 0x00044000 /*! I2C0 Start Address */
#define I2C0_END 0x000440FF /*! I2C0 End Address */
#define I2C1_BASE 0x00044100 /*! I2C1 Start Address */
#define I2C1_END 0x000441FF /*! I2C1 End Address */
#define I2C_OFFSET 0x100
```

Yeah, no way that the datasheet defines one I2C pin but someone wrote the driver for 2. That's when I went on a hunt for what **this** driver was even written for and found out that there exists a [prototype documentation](https://cdn.prod.website-files.com/63bb8de9076d75786876e803/677769d8383d9a93ed89e865_datasheet.pdf) which EXACTLY matches the driver behavior.

The reason I know this is not the right chip is simply because the earlier datasheet was pulled from their live website which is what they sell to people. So, now the time has come to hunt for the right drivers.

### Hunt begins

Before I tell you what all I found out, the question to acknowledge is why am I even looking at the code. Well, here's the thing. I have the following documents given by mindgrove on thier own:

1. [The datasheet](https://corevoice.b-cdn.net/mindgrove/docs/MGS2401B144C_datasheet.pdf)
2. [The API reference manual](https://corevoice.b-cdn.net/mindgrove/docs/MGS2401_API_Reference.pdf)
3. [User Manual](https://corevoice.b-cdn.net/mindgrove/docs/MGS2401_User_Manual.pdf)

What these don't tell me are the following:

- PLIC numbers for each peripheral
- Memory addresses for each peripheral
- UART model (what does UART do?)
- I2C model (how does I2C behave?)
- QSPI/SPI model (same with SPI)

So, the hunt in the codebase is to find a whole PLIC listing, drivers for peripherals to explain how to model them and get the IP block bitmaps.

Usually, chip manufactures would also provide something called a SVD or a DTS, this is what I am looking for because Mindgrove, even thought they didn't explicitly provide it, must have coded it out! If I get my hands on these it'll be golden.

So, to start with I dived straight into the shakti source and found something better than the codebase. The [SoC device registry manual](https://shakti.org.in/docs/shakti-soc-device-register-manual.pdf). This helps answer the modeling questions for the peripherals because this gives me for example for UART:

- `BAUD` offset
- `TX/RX` registers
- `Status` bits
- `Delay/Control/IEN` register offsets

A similar situation exists for I2C and SPI too. The manual is goated. And I cross referenced that with the code as well. As an example, for I2C:

```
For below table:

M = Manual shared above
Zi/N = Code from Mindgrove-Technologies

| Register | Offset | **M** (V1.3, pp.14-16) | **Zi** `i2c_secure_iot.c` | **N** `I2C_Type` (L2267-2332) |
|---|---|---|---|---|
| PRESCALE | `0x00` | "Prescale ‘h00 8 bits" | `#define I2C_PRESCALE 0x00` | first member (0x00) |
| CONTROL  | `0x08` | "Control ‘h08 8 bits" | `#define I2C_CONTROL 0x08` | `CTRL` (L2274) |
| DATA     | `0x10` | "Data ‘h10 8 bits" | `#define I2C_DATA 0x10` | `S0` (L2291) |
| STATUS   | `0x18` | "Status ‘h18 8 bits" | `#define I2C_STATUS 0x18` | `STATUS` (L2297) |
| SCL      | `0x38` | "SCL ‘h38 8 bits" | `#define I2C_SCL_DIV 0x38` | `SCL` (L2331) |
```

That was decisive for me that the manual is true! BTW, I verified, all the code above was commited in 2026. That's likely for the latest chip and hence correct.

So that was for the peripherals, now I needed the PLIC numbers so that I can do interrupt routing. For ARM Cortex chips, I take the NVIC numbers btw, PLIC is pretty much the same thing but different. So, finding this was a pain. Because I kept stumbling upon outdated code!

For example, at one point, I came across this:

```
#define GPIO_INTERRUPT_0      1	 /* GPIO 0  */
#define GPIO_INTERRUPT_1      2	 /* GPIO 1  */
#define GPIO_INTERRUPT_2      3	 /* GPIO 2  */
#define GPIO_INTERRUPT_3      4	 /* GPIO 3  */
#define GPIO_INTERRUPT_4      5	 /* GPIO 4  */
#define GPIO_INTERRUPT_5      6	 /* GPIO 5  */
#define GPIO_INTERRUPT_6      7	 /* GPIO 6  */
#define GPIO_INTERRUPT_7      8	 /* GPIO 7  */
#define GPIO_INTERRUPT_8      9	 /* GPIO 8  */
#define GPIO_INTERRUPT_9      10	 /* GPIO 9  */
#define GPIO_INTERRUPT_10     11	 /* GPIO 10 */
#define GPIO_INTERRUPT_11     12	 /* GPIO 11 */
#define GPIO_INTERRUPT_12     13	 /* GPIO 12 */
#define GPIO_INTERRUPT_13     14	 /* GPIO 13 */
#define GPIO_INTERRUPT_14     15	 /* GPIO 14 */
#define GPIO_INTERRUPT_15     16	 /* GPIO 15 */
#define GPIO_INTERRUPT_16     17	 /* GPIO 16  */
#define GPIO_INTERRUPT_17     18	 /* GPIO 17  */
#define GPIO_INTERRUPT_18     19	 /* GPIO 18  */
#define GPIO_INTERRUPT_19     20	 /* GPIO 19  */
#define GPIO_INTERRUPT_20     21	 /* GPIO 20  */
#define GPIO_INTERRUPT_21     22	 /* GPIO 21 */
#define GPIO_INTERRUPT_22     23	 /* GPIO 22 */
#define GPIO_INTERRUPT_23     24	 /* GPIO 23 */
#define GPIO_INTERRUPT_24     25  /* GPIO 24 */
#define GPIO_INTERRUPT_25     26  /* GPIO 25 */
#define GPIO_INTERRUPT_26     27  /* GPIO 26 */
#define GPIO_INTERRUPT_27     28  /* GPIO 27 */
#define GPIO_INTERRUPT_28     29  /* GPIO 28 */
#define GPIO_INTERRUPT_29     30  /* GPIO 29 */
#define GPIO_INTERRUPT_30     31  /* GPIO 30 */
#define GPIO_INTERRUPT_31     32  /* GPIO 31 */
#define PWM_INTERRUPT_7       33  /* PWM 7 */
#define PWM_INTERRUPT_6       34  /* PWM 6 */
#define PWM_INTERRUPT_5       35  /* PWM 5 */
#define PWM_INTERRUPT_4       36  /* PWM 4 */
#define PWM_INTERRUPT_3       37  /* PWM 3 */
#define PWM_INTERRUPT_2       38  /* PWM 2 */
#define PWM_INTERRUPT_1       39  /* PWM 1 */
#define PWM_INTERRUPT_0       40  /* PWM 0 */
#define GPTIMER_INTERRUPT_0   41  /* GPTIMER 0 */
#define GPTIMER_INTERRUPT_1   42  /* GPTIMER 1 */
#define GPTIMER_INTERRUPT_2   43  /* GPTIMER 2 */
#define GPTIMER_INTERRUPT_3   44  /* GPTIMER 3 */
#define I2C_INTERRUPT_0       45  /* I2C 0 */
#define I2C_INTERRUPT_1       46  /* I2C 1 */
#define UART_INTERRUPT_0      47  /* UART 0 */
#define UART_INTERRUPT_1      48  /* UART 1 */
#define UART_INTERRUPT_2      49  /* UART 2 */
#define QSPI_INTERRUPT_1      50  /* QSPI 1 */
#define QSPI_READY_1          51
#define QSPI_INTERRUPT_0      52  /* QSPI 0 */
#define QSPI_READY_0          53
#define SPI_INTERRUPT_3       54  /* SPI 3 */
#define SPI_INTERRUPT_2       55  /* SPI 2 */
#define SPI_INTERRUPT_1       56  /* SPI 1 */
#define SPI_INTERRUPT_0       57  /* SPI 0 */
#define ADC_INTERRUPT         58  /* ADC  */
```

You see the problem here? The datasheet mentions 81 PLIC numbers!

```
6.2.14 Platform Level Interrupt Controller (PLIC)

This device receives the interrupts from all the peripherals and notifies the system for an interrupt.

Key Features:
• Interrupt from 81 sources are connected.
• Interrupt priority value upto 7.
• A threshold register to service interrupts above a required priority value.
```

So, I kept searching, I found this exact file which had all the changes in a separate branch in a separate repo of Mindgrove. 

```c

/* =========================================================================================================================== */
/* ================                                Interrupt Number Definition                                ================ */
/* =========================================================================================================================== */

typedef enum {
/* =======================================  Shakti C-Class Specific Interrupt Numbers  ======================================= */
/* =========================================  Secure_IoT Specific Interrupt Numbers  ========================================= */
  GPIO0_IRQn                =   1,              /*!< 1  GPIO0                                                                  */
  GPIO1_IRQn                =   2,              /*!< 2  GPIO1                                                                  */
  GPIO2_IRQn                =   3,              /*!< 3  GPIO2                                                                  */
  GPIO3_IRQn                =   4,              /*!< 4  GPIO3                                                                  */
  GPIO4_IRQn                =   5,              /*!< 5  GPIO4                                                                  */
  GPIO5_IRQn                =   6,              /*!< 6  GPIO5                                                                  */
  GPIO6_IRQn                =   7,              /*!< 7  GPIO6                                                                  */
  GPIO7_IRQn                =   8,              /*!< 8  GPIO7                                                                  */
  GPIO8_IRQn                =   9,              /*!< 9  GPIO8                                                                  */
  GPIO9_IRQn                =  10,              /*!< 10 GPIO9                                                                  */
  GPIO10_IRQn               =  11,              /*!< 11 GPIO10                                                                 */
  GPIO11_IRQn               =  12,              /*!< 12 GPIO11                                                                 */
  GPIO12_IRQn               =  13,              /*!< 13 GPIO12                                                                 */
  GPIO13_IRQn               =  14,              /*!< 14 GPIO13                                                                 */
  GPIO14_IRQn               =  15,              /*!< 15 GPIO14                                                                 */
  GPIO15_IRQn               =  16,              /*!< 16 GPIO15                                                                 */
  GPIO16_IRQn               =  17,              /*!< 17 GPIO16                                                                 */
  GPIO17_IRQn               =  18,              /*!< 18 GPIO17                                                                 */
```

This was beautifully exhaustive, exactly 81 numbers as I wanted. And that's all I needed now to write my emulator for this chip! If only they had opensourced their SVD, I won't have had to search their drivers!

## Conclusion

I made the emulator, it was able to boot a hello-world binary **for the vision-soc**!! That's the wrong board but it works because `hello world` barely touched any peripherals and the ones it did, were the ones which were shared between the two. I later compiled the hello world for the secure-IOT chip and tested that, and it worked too!

Try it out [here](https://macrohill.com) (hopefully the link is still live by the time you read it. Otherwise, well, you gotta take my word for it)