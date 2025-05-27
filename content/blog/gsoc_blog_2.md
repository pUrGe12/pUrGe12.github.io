+++
title = "Project Nettacker: Part 2"
date = 2025-05-25
draft = false

[taxonomies]
categories = ["opensource"]
tags = ["Networks", "blog"]

[extra]
lang = "en"
+++

### Recap

> Things that are fully implemented (at least as of now, before mentor review):

1. branch: `patching-sqlalchemy-output` --> APSW for SQLite and SQLAlchemy for MySQL and PostgreSQL, integrated with master.
2. branch: `adding-wordist-change-option` --> Adding the custom wordlist path for enumeration and usernames and passwords (web) integrated with upstream master.
3. branch: `keeping-only-new_scan_task` --> Using Huey with flask perfectly, including running huey-consumer as a subprocess, integrated with the upstream master.
4. branch: `all-new-outputs` --> SARIF and DefectDojo output types perfectly done and integrated with master.
5. branch: `tests` --> Writing all test cases.

> Things that are left to be implemented

1. Some test cases
2. version scanning robustness
3. huey for other threading replacements (This will be a pain to integrate with the webdev one...)

---

The plan therefore is to finish tests first. Cause I want to dedicate the maximum efforts during GSoC to version scanning. I will finish tests, then throw everything at that huey implementation, finally when GSoC starts, I only work on version scanning (and other things that the mentor wants me to look at, related to AI I guess :))

I realised that the web+huey implementation I was going for that was failing due to 

```py
if not self.arguments.targets:
	log.info(_("no_live_service_found"))
    return True

```

was not a problem in the web part at all. Let me isolate the huey tasks, apply them one by one, and see which one is causing this issue (I mean, there are only two left out techincally, run_engine_task and scan_target_task)

---

27th May 2025
New day, gsoc starting time is coming closer and closer. I am thinking, fuck huey and all for now. Let's devote the next 3 days on version scanning and do that beautifully.

branch: `code-refactor-version-scan-faster`

I checked it out and it mostly works. I will first rebase this with the upstream master. First order of business. Ahh, wait. I had already done that.

Holy cow, just learnt about sliding windows rn. Crazy. I suck at this shit. Fuck, will have to watch some videos. 

Alright fuck that. So, today's goal is to fully understand what I had done and the changes I made. I really remember very less about this. Thankfully, I did document some parts of it (hopefully) in `docs.md` so I will focus on that right now.

> I am officially fcked cause I don't have the documentation for that. Will have to read the docstrings. Grind on.