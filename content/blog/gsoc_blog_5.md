+++
title = "Official member! mostly fixes and rant"
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

June 29th

And the day of reckoning is coming nearer. I got a new laptop. Its got a 16 core CPU, 32GB DDR4RAM and 1TB SSD. Its pretty sexy, and the first thing I did is install and rice up my linux for the dev enviornment that I prefer. This looks now. I just need to sign into my `GCP` credits account and all will be done. Also I have Barclays' intern test tomorrow morning 12pm.

I checked my code for the new UDP scanning. Few things to note

- Do not forget that the `-sU` flag should and will only work with `-m port_scan`. This is a concious thing
- With the new async code for the sockets, try out sending UDP probes concurrently. See if that helps. I have given the async code for a PR

Getting this to work

- I removed all the return statements for `run_udp_scan` inside the engine and also don't need to go inside `response_conditions_matched`.

This is because I currently dont have this in the right format. It gives all the wrong keys and values! Use this for debugging

```sh
poetry run python3 nettacker.py -i paypal.com -m port_scan -sU -v -g 443
```

- I am hacking a LOT. Completely messing up the architecture. This is definetly not ideal because, uhh, because its bad. I shouldn't define a new run just for UDP scanning. 

- Even the minimal working example has these few issues. Also I need to change the ulimit because I hit a lot of `many open files~` OSError. NOW THIS SUCKS! Because uhh, LOTS of overhead, this is something I have to avoid.

So there must be a way to get the datagram protocol without running so many open files and all.

---

July 1st

New day! Today I got my OWASP email finally! Its achintya.jai@owasp.org! yeah, I know I know, pretty cool! Mr. Sam wants me in on their Nettacker x OpenAI codex project so thats super exciting. I also got access to a bunch of OWASP resources specific to members so LETS GO.

Anyway I am currently making a seperate branch for UDP scanning because right now there are probably a lot of architectural issues that I need to sort. This one has a lot of changes for different stuff that I don't need as of now.

branch: `udp-scanner-full`

Actually now that I am thinking. It will be SOOOOOO much cleaner to just have this as a seperate YAML file! Why am I so adamant on `port_scan` be present when UDP is run? Why can't we just have a seperate method called "udp_scan" and be done with it!

Alright, this branch will hvae this implementation, then I will let Mr. Sam choose. Finally I have some direction on this.

1. I created a new yaml file called `udp.yaml` for `udp_port` scanning which calls the `udp_scan_receive` function.
2. I have removed the regexes from the file. I will have to define new ones once I test mine enough.
3. Then I basically want to have all the UDP probes present with the `udp_send_receive`.

I can make this analogous to subdomain_scan because even that works by basically specifying a flag right. I can just have a flag like I used to have and then check inside app,py if that flag is set and if it is set, then simply set the module name as `udp_scan`.

Also, is it not better to save all the probes in a shared list rather than having to pass it around in arguments? That way I don't have to worry about adding and deleting it from the dictionary inside `base.py`.

4. Okay this is so much simpler! I dont have to create a new run function (that was extremely dumnb) I dont have to delete anything extra from the dictionary inside base.py. This is whole reason to have a yaml file! Now I have the probes inside `udp_send_receive` and I have threading also working nicely and all.

I have simply defined a flag `-sU` that checks if the user wants UDP scanning or not. If the flag is set then I load the UDP probes and I store that in a shared list. Then I start the scan with the module being only `udp_scan`, just like we do for subdomian scans and port scans and icmp scans. Then just like subdomain scans, I dont define the success of future scans on this one (because see, if port_scan failed, then it basically runs nothing cause `find_events` doesn't work anymore) so we don't care about that in this case. If there are no UDP services, well, so it be! I simmply move on.

5. I changed that shared list to a dictionary because its faster and no duplicates (there is no set implementation directly, so the value can just be stored as `True`)

This finishes the basic implementation. The only, only issue now is that each thread needs to send around 80 different probes. This means, after the initial `-t` threads are called for, they will each finish of their 80 probes, then the next few ports will be tested and so on. This is slow as fuck and I need to now introduce something called concurrency into this picture. 

I hope the `testing-asyncio` part is merged because that will genuinely make it so much easier for me to work on this. Otherwise I may have to spawn new threads here and thats bad! Even verbose mode works! Everything is so much easier I swear!

---

July 2nd

I have to make a small website for an intern test, so I will do this today. I made a small PR to fix the uncaught exception for /etc/services in `socket.getservbyport()` thats all. I haven't worked on the udp-scanner since yesterday because I am waiting for any sort of confirmation from Mr. Sam on the asycio test codes. Let's see about that till then.

---

July 3rd

I am done with the website thing. I just have to host it on render now. I am thinking I will write some test cases and make PRs for those today. Additionally, since I am done with the UDP scanner, I should probably make a different file for service scanner as well. Takes care of a lot of unncessary things that I was initially doing!

Hosting on render is probably going to take time cause I suck at this stuff. Let's see. I am writing the test case for module.py and making a PR for the same. No more words on this! 

Made tests for module and graph. PRs done for both. Turns out it took some time, its 4th July now. Today I am finishing off that last part of huey, that is somehow fixing the scan_id issue. Let's see how to do it cause I am literally getting no ideas whatsoever.

---

July 4th

So those intern thingie guys, they wanna have a talk. Its a WFO thing in bangalore and since I am travelling in August and semester also starts then, there is no way I can do that, unless they agree to a hybrid mode or something. I know they're not desperate to hire me, nor am I desperate to get hired. So, its a pretty level playing field, open to negotitations. let's see.

Today, `new_scan_task` my friend. Finally to be over with so that i can show Mr. Sam something in the weekends!

---

July 20th

So, some time has passed. There has been some updates. I will continue this. Also, I feel like shit now. I made a lot of silly things that ended up being big. Bigger than I thought.