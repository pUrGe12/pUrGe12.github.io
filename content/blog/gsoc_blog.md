+++
title = "Project Nettacker"
date = 2025-05-17
draft = false

[taxonomies]
categories = ["opensource"]
tags = ["Networks", "blog"]

[extra]
lang = "en"
+++


Update from the future (21st May)
I am going to be using this as a work tracker thingie, you'll find a lot of rant about test cases intially, and then some rant about other things. For the actual gsoc blog, stay tuned, it'll be coming soon.

---

Saturday - 2025-05-17
For the past few days I have been writing test cases for different files. So far I have 34% coverage locally and once I get to 70 which is hopefully by the end of this week, I will start pushing tests one by one (don't want to overburden the maintainer). I have written tests for the following files so far (will use this to keep track)

1. core/ip.py
2. api/engine.py
3. api/core.py
4. core/die.py

To do this I had to refactor `ip.py` for which I created a PR and further I had to add `.csv` to .gitignore because this file is created during test runtime and we don't want to commit that at all (this is for `test_engine.py`). The ip.py refactoring is just returning boolean values instead of objects cause that helps in writing tests (alternatively I could do while testing but same difference).


IMP:
> Branch's name is "tests" where I plan on doing all the test cases first and then pick one and add it to its own branch and make a PR

Additionally I have finished the APSW port and got it working with SQLAlchemy for mysql and postgres. It all seems to work fine.

> This branch is `patching-sqlalchemy-output` (don't ask why such a bad name)

Update: Just realised that the postgres stuff is still incorrect as it connects to the database itself so for a first time user, they need to have the database created! But that won't be true so it will raise errors and hence at this point we can connect to the default `postgres`database and create a new one from there and then use that.

---

Alright at this point, `patching-sqlalchemy-output` should be ready for raising a PR. I have tested all the database types.

Another thought:
> We should probably have tests for all databases! This should be inside the CI/CD checks as well... Lemme see.

---

Alright contuining with test cases. Let's do for arg_parser.py now. I am doing this randomly and not at all following the timeline I gave, but if the goal is finish allll of it before June then why does it even matter?


The idea behind testing arg_parsing logic is simply that I need to see if it parses each argument correctly or not. We'll have to patch these guys:

1. `sys.argv` (simulate command-line input)
2. File I/O functions (open, read, write).
3. Config access (Config.settings, Config.path, etc.).
4. External function calls (like die_failure, die_success).
5. Any module that causes side effects (start_api_server, generate_ip_range, etc.)

okay this is harder than expected. Let's do the easy ones first. (**agressively crying**)

---

Testing out databases actually. These are important too! I wrote tests for mysql, model and sqlite. Will write one for postgres later once the updates are merged (or neglected. I think it shouldn't be neglected cause uhh, it won't really work otherwise). Same goes for db.py. Its supposed to undergo a major refraction so I will wait.

1. core/ip.py
2. api/engine.py
3. api/core.py
4. core/die.py
5. core/fuzzer.py
6. graph.py

There are no major revisions to file in the future (probably some small nitty-gritties here and there) so will fix the as they come up.

---

Today is May 23rd. I did some work on GI attacks yesterday, back to full time gsoc work today. So, I'll be starting with a few test cases again cause those are simple and easy. Then I am thinking I should get the peripherals over with and finish off the UI improvements and keep it safe to push later.

The rebasing won't be difficult cause those files were never changed, so I will do that to. Its just important to keep track of which branch serves what purpose! Honestly I don't want to redo this work.

I did some for module.py. This is soo boring and hard man. 


1. core/ip.py
2. api/engine.py
3. api/core.py
4. core/die.py
5. core/fuzzer.py
6. core/graph.py
7. core/module.py (69%)

Will have to revist this. Let's finalize the ones for web dev.

Please to look in `adding-wordist-change-option` branch. It contains the rebased version of the webdev changes (the custom wordlist addition options). I will now finish the huey thingie as well. Had some missing things there. Tonights for that (after dinner)

---

24th May 2025

Alright, new day and I am starting with the huey thing I left out yesterday. I will have to go and get my new specs from the shop at 11am. So, I have like 30 mins before that. I'll plan.

1. Note that we'll have to create a `.broker` directory for huey to store its message brokering database
2. Will have to run something like this: `huey_consumer.py nettacker.core.tasks.huey -w 100 -k process` in a seperate process

I am thinking we can make the number of workers and all into a user-configurable parameter and add that to the config file. Additionally we can run this command in the very start with `nettacker.py` itself? or maybe `main.py`?

Alight I mean it sort of works actually! There is one small error I am getting:
```
sqlalchemy.exc.InterfaceError: (sqlite3.InterfaceError) Error binding parameter 0 - probably unsupported type.
[SQL: DELETE FROM scan_events WHERE scan_events.target = ? AND scan_events.module_name = ? AND scan_events.scan_unique_id != ? AND scan_events.scan_unique_id IS NOT NULL]
[parameters: ([[['127.0.0.1']]], 'port_scan', 'hvmnxwduvualunofvamvfawurgtgzsoo')]
```

I am suspecting it has something to do with the targets being a list of the port_scan not being inside a list... Cause this is what I hit initially

```
  File "/home/purge/Nettacker/nettacker/core/app.py", line 186, in expand_targets
    self.arguments.selected_modules.remove("port_scan")
AttributeError: 'str' object has no attribute 'remove'
```

This should've really been a string. So, I will try and see how to fix this. 

Todo:
1. Fix above error
2. Display a better message to the user that their scans are underway
3. Tell the user the scan is done!
4. Run Huey in the background

If all of this works perfectly then I should start writing test cases for this. This is a good practise besides, I am going a little slow on that. June 1st is the official beginning of the coding period and I can't take any risks!

I think the issue is a little deeper than what I assumed it to be. Let me first rebase this with the master branch. Then we'll see.

Update: The rebasing sucked. Made a new branch and cherry-picked commits: `clean-huey-with-flask`. Alright major issue spotted. The problem is that it is not saving anything to the database. It's just not reaching that part of the code for some reason. So, `find_events` returns nothing and that fucks me up cause now I can't do any other scan than port_scan.

For some reason during normal operation, the linear sequence means the "find_events" is triggered AFTER we submit to the db. In this case we are submitting to the DB just that, find_events is being trigged before. WHY WHY WHY?

Uhm, no. My bad. We're unsuccessful in adding to db. Hitting this part: 

```py
		else:
            print("hope we're not coming here?")
            del event["response"]["conditions"]
            log.verbose_info(
                _("send_unsuccess_event_from_module").format(
                    process_number,
                    module_name,
                    target,
                    module_thread_number,
                    total_module_thread_number,
                    request_number_counter,
                    total_number_of_requests,
                )
            )
            log.verbose_info(json.dumps(event))
            return "save_to_temp_events_only" in event["response"]
```

Now I know the issue!

---

Alright, sat and debugged and sad to report that the issue is we're somehow, for some unknown reason, using "find_events" `before` when actually should. That sucks. Cause IDK why. Like wtf? I compared with the normal nettacker operation. And yeah, pretty much this issue. I will try and run the API version too, and compare with that. Let's see.

You know what I think will be good? If I remove all other huey tasks except `new_scan_task`. Let's see how that goes. New branch baby.

branch: `keeping-only-new_scan_task`

Bloody hell, bloody hell (in British accent), that actually works! Alright, now lets first add this as a subprocess and see. once this is final, I am thinking I will first make a similar standalone setup for the normal huey based system and put subprocess there. 

This is done! Shit's now working. I am running this as a subprocess and it has the added benefit of showing the user what is going on and gracefully exiting and all. Nice. Also, we instantly get results so beautiful there too. I am thinking this is good enough, unless Mr. Sam thinks we should do the other parts as well. Till then, I am release the print statements and test this out more. With both API and non-API cases. Make sure its robust AF.

As expected some issues did come up. Multiple modules not being scanned properly. Another thing, we must close the process we opened when we close the program! otherwise bruh, it fucks everything up. 

Alright, branch `keeping-only-new_scan_task` is completely ready. Can be PRed today! But nope. We'll wait. Let's work on the next parts. I am going to start with the output types tomorrow. Finish that up quickly. And yeah, tests. yeah. BTW the new branch is completely rebased with the master, so pretty good.

So with this the webdev part is completed. At least from my side. Mr. Sam may have something to say about this. 

relevant branches for webdev:
1. `keeping-only-new_scan_task`
2. `adding-wordist-change-option`