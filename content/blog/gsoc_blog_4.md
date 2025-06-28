+++
title = "Updating Huey processing logic for in-memory usage and progress tracking UI"
date = 2025-06-20
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

Update: I do have a progress bar (at least the UI ready), I am able to stack multiple ones based on scan_ids. I just need to now figure out a way to calculate the progress for real and send it!

---

23rd June

Its 10am in the morning. I have found another issue with the webserver

1. When we launch nettacker it loads all modules, EVEN if its the webserver. Then when a scan is called for, it again loads all modules.

Why don't we see it? Because its supressed in `logger.py`. You know what, its too much of a pain to solve, cause that will involve I think major refactoring! I am not ready for that.

I will just get the progress bar thingie working. ALRIGHT BIG ISSUE. So you see this part of the code right
```py
    form_values["targets"] = [form_values["targets"]]
    nettacker_app = Nettacker(api_arguments=SimpleNamespace(**form_values))
    app_arguments = nettacker_app.arguments

    if not isinstance(app_arguments.selected_modules, list) and (app_arguments.selected_modules is not None):
        app_arguments.selected_modules = app_arguments.selected_modules.split(",")
    nettacker_app.arguments = app_arguments
    nettacker_app.run()

    return vars(app_arguments)
```

This is what I had to change. Spot the difference? I had just found out that after selecting a profile from the UI, my initial code was not really taking in the different modules under it!

This was because I wasn't really using the nettacker parsed arguments! So, simple bug fix.

And, everything works!!! How happy I am to report this. I shared the working video with Mr. Sam who was initially suggesting that this might be too complex to do (well, it did take 5 hours of non-stop work) but in the end, I did get it working. There is one big problem with this approach though (which Mr. Sam also noted)

> Using an SQLite database is not optimal cause WE'RE TRYING to avoid too many file read and writes!!!

So, I need to figure out a way to have an in-memory thing. It shouldn't be hard except for the fact that we're using multiprocess! This means, new processes! This means I CAN'T just share a dictionary between them and call it a day! I spent so long wondering why that wasn't working, which is the whole reason why I came up with the SQLite new table thingie. 

I have found one more thing to try so lets see about that now.

Alright!! This also is done!! Wow. The wonders of `multiprocess.Manager.dict()`. Absoultely lovely.

- So for multiple targets, it creates different processes. This is fine and dandy but since they are under the same scan_id I will have to display the cumulative progress which creates an illusion that things are happening sequentually (they aren't).

This is a slight issue because the part where I am creating the updates for the percentages, are in the lower levels of threading which means, they are all acting on the single target. This means I have absolutely no way of know how many targets were specified by the user in the upper levels cause its all abstracted away.

Fuck these problems man.

I think one way to resolve this can be to have a `num_targets` value being shared across all processes, using the same Manager inside `__init__.py`. This might work. Let's test this out. The idea is simple, if there are `n` targets, then either

1. Multiply the total number of requests by `n`
2. Divide the current request number by `n`

A is of-course the better idea because it only needs to be done once inside `module.py`.

Guess what, that thing works, but life is never that easy. I just found out that for some reason, I am unable to enter multiple targets. This is again a revelation, second time in one day (technically this is a new day, its 1am now). Let's see.

Alright, that is also now sorted! There is another issue (no one is surprised). If I choose more than 1 targets, it keep looping. It goes from 0 to 100 for the first one, then back from 0 to 100 for the next one and so on. Honestly, I dont mind. I might actually add a small bar next to it to indiviate the number of targets that it finished scanning!

> Classic example of its not a bug, its a feature!

okay sent the changelog to Mr. Sam. Let's see what he thinks. I also asked about the new-outputs changes for the SARIF and defect_dojo outputs. I am not sure if any changes are required there. I mean, since I am not the one using it, we can keep it there, and whoever's interested can modify and do it themselves! Thats the spirit of opensource isn't it.

---

June 24th

So, I mentioned some problems to Mr. Sam about this. He asked me to send the changelog to him first in case there needs to be some architecture change. Let's see. I am watching `vanilla sky`.

That's all I did today

---

June 25th

Ahh, new day. I am finishing up the huey with flask thing. Took much longer than expected. I am so behind schedule! Mr. Sam hasn't replied yet so I will set forth and make the remaining changes. 

1. Cap the limit at 100% and once it reaches that, change it to **done!**
2. In case of multiple targets or modules, handle. 

See, I am thinking for multiple modules, I can just let it display which module it is currently scanning. Hmm, same can be done for targets!

Yeahh, this is done. Looks pretty good NGL. I would add this in my gallery but I am too lazy. Actually, I shall. and then reference it here. hmm, that works. I will make a nice video for Mr. Sam first, then do this.

Also have to order that watch and something for mom rn through a friend who's in the US rn.

I sent him a [documentation](https://docs.google.com/document/d/1RsYGEXXK32k3yBkJ4a6OoFEAE7zvh70pb23yZzb22nA/edit?tab=t.0#heading=h.wul3v0eg5n84) and a video running both the web and the normal scan. He was a little skeptical and rightly so because the changes at a glace may look like I have broken something, but to be sure, I haven't! I ran both the scans simultaneously to show that it works! I think i should seperate the huey part with the progress report and display part. Hmm, maybe I can't. I will see.

Firstly I have to fix my new-outputs thingie. Boy, this is not ideal! I was thinking I am done with this and this was supposed to be the easy part! Come on! See the problem is, I am reopening all the files in order to figure out the severity and all. That's redudundant because I have already opened those files before! Gotta fix it all. Its almost 12am, before 2, this should be ready.

BTW I found out that the drupal_scan and joomla_template scans are broken because of a python regexing issue. So, I created a test case that will scan through all regexes inside the `scan` and `vuln` modules and tell which of them are fine and which aren't. I added this to nettacker today. So, atleast something came from the day!

---
June 26th

Haha, took less than 20 minutes. Cause I didn't have to juggle about! There is only 1 place in the entire codebase where we are actually reading all the modules. That is inside load_modules in arg_parser. So, that's where I attacked and boom, I have all the severity and descs for everyone.

This is not good though, this day was a waste SMH. I had to do UDP scanning today! There is less than 4 days left to the end of the month now! Come on! Gotta be fast fast.  Huh, I didn't really work today, all the stuff was done before sleeping.

---
June 27th

Today I have a meet with Mr. Sam. He wants to discuss the Huey part again with me. I don't know, let's see what happens. Its at 6:30. Until then I am thinking I will FINALLY get some work done on the UDP port scan! I want to be done with huey, at least for now, LATEST by July 1st. Let's not be doing the same things in July as well... oh, and also the new outputs thingie.


So, back to the old track. I have to do the following to make UDP scanning proper. I will first descibe the entire architecture, then the remaining work

1. The user runs Nettacker with the `-sU` flag enabled.
2. This sets the `udp_scan` variable and hence loads all the UDP probes.
3. The probe loading logic is that, it opens the YAML file for the service probes that is present inside `nettacker/lib/payloads/probes` and it pulls the probes from that, seperates the UDP ones and gives it.

Note that we don't and we shouldn't load this YAMl if the `-sU` flag is not set because it takes too much time! Its a big file. We could look into manually seperating the UDP probes from the TCP ones but that is currently just a matter of optimization and not principle.

4. While it is loading, we display to the user that it is loading UDP probes and it may take some time.
5. After it is done, nettacker runs a `port_scan` as before. Then once the port_scan is over, it displays `TCP scan is finished`. Now if the `UDP_scan` flag was set, it displays, `Now starting UDP scan`.

I don't want it to say `TCP scan is finished, now starting UDP scan` because the user might not have ever specified the `-sU` flag.

6. Then we start UDP port scanning. Here each thread picks up a port, sends around 100 or so probes sequentially. After each probe, each thread waits for 3 seconds for a response, and if nothing, then it sends the next probe.

Improvements:

1. Make it such that only if `port_scan` is specified by the user, will the UDP scanning take place. I don't want it to be like

```sh
python3 nettacker.py -i example.com,test.com -m dir_scan,http_vuln_scan -v -t 100 -sU
```

This makes no sense. I know that internally it will do a port_scan first unless -d is specified, but still. I want the command itself to make sense, so `port_scan` must be specified by the user explicitly if they want UDP scanning to take place.

2. three seconds of wait time after each request should actually be a user defined parameter inside settings.

3. Improve the request sending capacity in the UDP scanning part. I want to thread it. I know its already inside a thread, but I want to see if I can make it faster.

So currently each thread is sending a 100 or so probes sequentially. I want to see, if this can be parallelized in itself. If yes, then boom, instant boost in speed. Lets work on that, and swtich to a new doc.

I think I should change the names of these titles. They are too boring.