+++
title = "Developing duxMLB, an extension for MLB fans"
date = 2025-01-29
draft = false

[taxonomies]
categories = ["AI", "Software"]
tags = ["Python", "yolo", "Deep learning"]

[extra]
lang = "en"
+++

This is how I built duxMLB and what it really is. It was developed for a hackathon and though I eventually got bored I decided to finally finish it and write about it. The following is the elevator pitch that I gave for the official submission.

## Inspiration

I found this hackathon through a friend and I figured something very interesting can be done with this problem statement. Around a week before the launch of this hackathon I was working on an AI based terminal, which I called `TerminAI`. It was a LAM type framework where the user could enter their commands in natural lanaguge (and not bash or MAC commands) and have it execute. So, things they didn't know how to do using a normal terminal could be done there. So, I was pretty much `into` the idea of creating LAM based applications because I found normal LLMs to be pretty boring and overdone.

When I heard of this, the first thing that came to my mind was a **live statcast generator**, that would record your screen realtime and generate data based on that. This was the time when Apple Intelligence was also gaining some hype and it did something similar so I figured I would do this. But soon I realised that, though it make for a **good project**, it would've been pretty useless cause nowadays statcast data is present during games! 

To figure what to build, I watched some games and I had never watched baseball before so it took time to figure out the rules and man I got hooked! I won't go into my watching spree cause that's probably not needed but it was a fun time. However, I found myself constantly searching for players and teams so the best place to start with seemed like a **simple LLM** that I can type the player's name and get information. And morever it had to be `while` I was watching the games cause I didn't want to open new tabs! So, therefore the idea of a `chrome extension` came to me.

Since then, I have included a lot more functionality to my extension (catering to the given problem statements) and I decided to call it `duxMLB` that is `Captain of MLB` in Latin (I like to have fun with names). The next few sections will explain more details about this extension.

## What it does

The following are the features that **duxMLB** shows:

1. A panel on the side for you are watching live matches. It is `Gemini` instructed to be a `good baseball coach` and answer related questions.

- It has three API calls that it can make. Firstly to get `player information`, secondly for `team information` and lastly for getting the `schedule`. 
- The user can normally interact with it, and when they ask for any of the three above, the LLM calls an API and gets the results.
- The results are pretty printed through another Gemini model (that I call the `pretty_printer`).

2. The panel also allows users to get the last `5 seconds of video` they were watching and generate statcast data for that.

- The timing is crucial for this and the implementation is also pretty slick. I will explain how this works in the next section.
- The `statcast` data generated is basically just two things:

	- Pitch speed
	- Bat swing speed

- If there is no such **pitches** or **swings** in those 5 seconds then it will output nothing basically.

3. Then there is the `options` page. Here there are 3 things:

- The first is the **MLB future predictor** which takes in the `homerun` data for the user and based on similarities with the top players, it tells the user how good or bad they are.
- This comparision is done using a dataset that was provided with the problem statement itself and a `vectorDB`.

- There is a guide page that also goes into the implementation and functionality (I didn't know I would have to write here as well, so I was planning to use that as a guide)

- Finally there is a classics video/name uploader which users can use to upload their favourite games, and generate statcast data for that. Again statcast data means 
	- Pitch speed
	- Bat swing speed
- If the user doesn't have the video with them locally (which is usually going to be the case), they can simply enter the name and it will be scraped.

So, I have tried to develop mulitple functionalities mentioned in the problem statement into one product. I had a lot more things in mind, but I will talk about them in another section.

## How I built it

First I will talk about the panel. The GUI is pretty basic

-- Give code to 

## Challenges I ran into

-- Getting the buffer feed
-- Finding the right model for baseball tracking
-- The math for the camera correction
-- Hosted backend on render but it ran out of memory

## Accomplishments that I am proud of

-- Multi-model structure
-- Multiple simultaneous architecture

## What I learned

-- First time using DL stuff
-- Building this was fun!

## What's next for duxMLB

Lot of things to write here!

-- Get users to upload their swings and compare with MLB swings
-- Host it up so you don't have to run the python file again and again
-- Since we are already detecting pitchers and catchers, we can do similar things for other players and then based on where they are standing, figure out what sort of game is being played

The reason I didn't do this is because I had absolutely no idea what type of games exist. (give them how to make it though)