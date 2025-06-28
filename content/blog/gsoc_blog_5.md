+++
title = "Updating Huey processing logic for in-memory usage and progress tracking UI"
date = 2025-06-27
draft = false

[taxonomies]
categories = ["opensource"]
tags = ["Networks", "blog"]

[extra]
lang = "en"
+++

June 27th

I have another meeting with Mr. Sam today. I actually have to propose using `asyncio` for socket.py as well just like we do for sending http requests. I know that there is no need at the current moment to involve concurreny inside port_scanning because the threads seem to handle it well. But the future idea is to hit `multiple probes` for each thread. This would take a lot of time if not done concurrently, and hence shifting to a concurrent architecture is better!

I already have done that in: `testing-asyncio-for-socket`. So, I will show that to him. Will let you know what comes up!

I made a PR. So, the major changes we discussed now are:

1. I am currently creating a new `scan_id` inside `main.js` and then using that in the future scans. This is not ideal from a cybersecurity point of view because this is happening client side. This is the most important change that needs to be done. Fix the scan_id issue AND see if you can just directy use UUIDs.

2. Check if huey itself has a way to report the scan progress. I dont think this will work because the scan itself is not being `done` by huey! It is just queueing it nicely and allowing me to do stuff with it.

3. Create some endpoints to get the `scan_ids` of all the running processes. Basically, one empty endpoint that gives all the running scans and all.

4. There was some PR made regarding SSL changes, check what that was about. Some SSL functions are deprecated in the python version we're currently running for. Check if we can make this better.

---

