+++
title = "Project Nettacker: Part 3"
date = 2025-05-29
draft = false

[taxonomies]
categories = ["opensource"]
tags = ["Networks", "blog"]

[extra]
lang = "en"
+++

June 20th
After the talk with Mr. Sam:

1. Have to change Huey's implementation cause I need to not run that as a `subprocess`. Cause that's bad. So, I tried checking "immediate" mode with Huey and it works!

But I still need to work on getting the output nicely and exactly as we discussed.

2. I had to benchmark APSW against SQLAlchemy for my implementation of APSW in nettacker. So, I did that already. I think its a good enough improvement, let's see what Mr. Sam thinks about it.

This is the result I came up with: [Gdrive Link](https://docs.google.com/spreadsheets/d/1fmeKdajLh1n67C35l6u_DnzkKUhbw21Q3pl_ZqGd8mM/edit?usp=sharing)

3. Lastly, I need to figure out some stuff for webUI. I need to get streamlit running. Let's see about that.

This blog is mostly about my Huey stuff. I am facing slight issues with that. The immediate mode works and I am getting the scans running and the results and all. But I don't think its working AS WELL as I needed it to.

Let's see about that.

---

June 21st

So, I didn't do much work today. Its a saturday and I am reallllyyyy chilling. I just ordered pizzas actually. Hmmm. I have been attending some social events (a meetup with old friends and professors yesterday and my brother's investiture's ceremony today). Its been fun. I am relaxing. I was thinking I will check some socials before I get to work today, likely by 6pm. I just want to get this part ready, furiously, before today ends. So, saving up for that you can say.

Alright its 6:31pm now, I have finished my pizza, but I am reading a novel. Still haven't started work. I feel so fucking guilty, DAMN IT. I'mma start now.

So, I am able to use Huey with the immediate mode and its **not** using my immediate memory cause I am still using a database. So, its like, just no scheduling. I also changed `logger.py` to log even in case of APIs (I am not sure why they wanted to give the user **no** information while running the debugging API. I personally find the scan being performed much more useful)

Maybe we don't need to log every single thing. Yeah, just small hints are enough I suppose. Yes, I'll change that.

- Not logging `success_event_info` cause that just is not necessary. As I said, some hints are enough.

- I checked with multiple scans at the same time on github codespaces in the MAC (2 to be precise) and it still works as expected. So, yeah. So far its perfectly replicating what I wanted to implement. Like exactly. Now just the status-bar and I am done.

---

22nd June
I will have to get a queue implementation as well. Hmm...  sad noises, cause I think its a lot of work. 

I will first get the status bar (progress bar working) then we'll see about that. I really hope he likes this huey bit only so I don't have to work extra hard on that.