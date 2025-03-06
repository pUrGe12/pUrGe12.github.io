+++
title = "Getting into Open Source development"
date = 2025-02-03
draft = false

[taxonomies]
categories = ["Dev", "OpenSource"]
tags = ["Python"]

[extra]
lang = "en"
+++

# The beginnings

I have used git for quite some time now and I was spending most of my day staring at my screen working on things. Now seems like the right time to step up with game and start making contributions to projects that people `actually use` already.

Its harder to get a whole new thing working from scratch but that is what I will do eventually and the only way to learn about managing big repos and resolving issues is to start making OpenSource contributions. I have talked to a couple of guys and apparently there is GSoC applications coming up soon. I am thinking of applying.

---

Alright, this is day 2 of my deep dive into OpenSource. Its not that I have never made contributions, but only that I never specifically searched for issues and tried to solve them (most of my contributions were fixing the issues that I myself faced while using the app). Its a fun thing.

I don't want to make a lot of the details public yet, at least until the application phase ends.

---

This is day 3, I got my first PR merged, after having made around 5 in the last 3 days, with 2 issues and multiple comments regarding code updates. I will try and focus on different repos too along with 1 proper issue in the one repo I want to get in with.

---

Alright, day 8 today.

I have made some contributions, raised issues etc. The org is mostly dead man and it takes so much time to do anything! I really want to make this a faster process.

---

Today I worked on a big parser, trying to update it to ensure the latest data format is matched. Let's hope it works well.

---

Yes, day 11 (11th Feb, coincidence?) I guess. Went out to meet a friend. Apparently there is a `prom` tonight. I don't have no one but that's not stopping me from having my fun. I saw a bunch of cucks wait in all black suits outside the girls' hostels. Its just so fucking sad, waiting for your girl to show up in a pretty dress, waiting alongside 100 other boys all wearing the same, looking the same, being the same. 

There is nothing that stands them out.

I pushed a PR fixing an output report for a scanner. The mod said do it in a different way and don't change the main functionality for a single scan, so I did that. Then I did the same thing for another and released a PR. So far so good. Let's see. 

---

Day 13 or 14. Added my first new functionality to the codebase and released a PR. BTW the previous one got merged. one step at a time. I made the bug fixes to this one and a previous PR in defect dojo for a parser upgrade. This one's fixes worked, hopefully the docker doesn't show cock in the other one! I am bored now. I will make the documentation for the project proposal for Cysec. 

---

Made a bunch of PRs yesterday, 1 more got merged. Told the moderator on slack to check my PR for the new feature in nettacker. Let's see how it goes, it's been a day, he hasn't reached back.

He subtly hinted on implementing a version scanner along with normal port detection so I am now working on that. It's pretty crazy stuff, trying to imitate nmap as much as possible. 

---

Day 16 or something I guess. 

Bruh this takes so much time! He said he'll review today but I am still waiting (granted the afternoon just started in London) but come on man. 

I have a good idea about what I wanna do next. I am trying to get two big things working

1. Path building in URL during directory scans
2. Version detection for port scanning

---

New day!

Alright so didn't do much today. Cause I have 2 quizes today. Made some fixes for the drone security sheet, including formatting the table in markdown.

---

Day 23ish I guess. I am so bored. I think the maintainer is busy so he isn't reviewing my PR. I need to step up my game but will only succeed once he merges this!
I opened another in a different branch for custom wordlist addition. I have a feeling he's against error catching and using that as a core logic, but let's see.

---

Alright, My PR is still not reviewed, and today is a Saturday. I am not that worried cause I have started working on my application. I have included the following ideas into that, 

- [ ] Integrating Nettacker output with DefectDojo
- [ ] Integrating Grafana’s visualisation tool
- [ ] Version and filtered ports detection
- [ ] UI improvements for the dashboard
- [ ] Multi-threading issues fix -> Code refactoring
- [ ] Adding a SARIF output report format
- [ ] Implementing a testing framework

The problem is, unless I talk to Mr. Sam I am not sure what they except from DefectDojo and Grafana integration? Do they want me to make contributions in their repos to include enpoints and parsers for nettacker? or what else can they be actually asking my friend?

I am pretty sure its the former, cause there is no other way to integrate that, even if we use APIs, that still means I will have to create a parser for nettacker and its output formats. The question then is, should that be for the SARIF outputs or should it be for the HTML/json outputs? I am thinking I will say SARIF cause it makes more sense especially if that is the standard now.

---

Bhai, my head is spinning. I have way too many things to work on. I need to plan this properly else I'll continue spinning forever.

---

If an implementation is correct, and it doesn't harm the existing code, why not accept that? I don't understand the point of "fixing" something that's not really broken or hard to use.