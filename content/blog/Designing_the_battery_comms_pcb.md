+++
title = "Designing a PCB for CAN comms"
date = 2024-12-23
draft = false

[taxonomies]
categories = ["Hardware", "PCB"]
tags = ["Altium", "blog"]

[extra]
lang = "en"
+++

I have spent the winter vacations here in my college. I have been working on multiple things, helping my team finalise the electronics for the car, working for a MLB based hackathon and some cysec things. Recently I was working on a PCB board for the battery that will do the following:

1. Take CAN data from the BMS and display battery voltage on an 3.3V 1.5in OLED screen.
2. Log the CAN data irrespective of the CAN-ID to a microSD card.
3. Filter the battery temperature from the incoming CAN signal and drive fans through PWM

I designed a breadboard circuit for this first and I will outline the connections I made during that. While doing this I decided to make a generic CAN input to fan driving PCB cause its pretty useful for components that get heated. 

# The connections

