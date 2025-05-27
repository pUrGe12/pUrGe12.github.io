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

## Version scanning work

27th May 2025
New day, gsoc starting time is coming closer and closer. I am thinking, fuck huey and all for now. Let's devote the next 3 days on version scanning and do that beautifully.

branch: `code-refactor-version-scan-faster`

I checked it out and it mostly works. I will first rebase this with the upstream master. First order of business. Ahh, wait. I had already done that.

Holy cow, just learnt about sliding windows rn. Crazy. I suck at this shit. Fuck, will have to watch some videos. 

Alright fuck that. So, today's goal is to fully understand what I had done and the changes I made. I really remember very less about this. Thankfully, I did document some parts of it (hopefully) in `docs.md` so I will focus on that right now.

> I am officially fcked cause I don't have the documentation for that. Will have to read the docstrings. Grind on. 

I am thinking I will do the `UDP scan` part first, because its relatively smaller and it will give me a nice intro to my own code and implementation. The major issue is, I think each thread is running the UDP scan for all the ports inside port.yaml. THIS IS FUCKED.

on the contrary, version scanning works? Its the same logic right, so there shouldn't be a different. Will have to clarify the flow again. Used a little syntactical sugar:

```py
    for entry in data.get("service_logger", []):
        if int(entry["value"]) == port_number:
            print(f"inside this if: port_number is: {port_number}")
            results["probes"] = entry.get("probe", [])
            # print(f"probes_list: {results['probes']}")
            matches_list = entry.get("regex", [])
            # print(f"matches_list: {matches_list}")
            break
    # We can potentially add an optimization here, we can have a for...else block in python.
    # The idea being that, only when I don't break out of the loop, will this block be executed.

    # So, earlier I was assigning matches_list as empty each time. Un-necessary overhead. Cause later I am checking
    # if it has a value and then getting the results list. So, rather than that, I can just do that if I don't break out,
    # that means entry["value"] != port_number (so, its not the right one) just return empty stuff. Finish it off fast.
    else:
        print(f"I came inside else for {entry['value']}")
        # It doesn't have probes for ports like 3306 (mysql)
        return {"probes": [], "matches": []}
```

crazy man, who knew! Also, UDP scanning is not been done on the ports already discovered! Duh, cause the ports discovered are only TCP ones by definition (or rather by how we're already doing it). Hence, we need to test every port, and hence, we're calling `port_to_probes_and_matches` for all ports. Since we are directly using the probes list we don't have to worry about that, but `matches_list` requires more parsing and hence I was setting that to be empty for the future if the port is not the right one.


So one more optimization that I can think of is using a seperate function for probe extraction from the `data` through the function inside common.py. I mean, why do we have to extract all probes first and then pass it to another function to get only the UDP parts. okay now that I say it, its the same thing whether I check while parsing or check after parsing. No!!!!!

Think about it, in the former case we are going over the list once only, check while parsing. While in the second case, we're going over it twice. Hmmm. I will look into this prospect. 

Alright I have made sense of the flow:

1. The `-sV` or `-sU` flag is specified by the user and read by the program
2. Inside `app.py`, if these flags are set, then we call `load_yaml`
3. `load_yaml` reads the big yaml file and stores that as a variable inside the options
4. It eventually reaches `base.py` where I check if udp_scan is needed or if service_scan is needed. In case of both, service scanning is done first, then UDP (according to the flow of the interpreter)
5. It basically calls the `udp_port_scanner`, which is an attribute I have assgined to the actual function inside `socket.py`. To this it passes the entire `sub_step` which basically contains
	- `host`
	- `port`
	- `timeout`
	- an additional field called `data` which is the big yaml parsed data

6. Now inside UDP scan the first order is to get all the UDP probes inorder to scan. This is does using two functions (at present, I might change this) `extract_UDP_probes(port_to_probes_and_matches())`. To the inner function, we pass the port number and `data` which came to us from `sub_step`
7. This is to extract from the `port` and `data`, the probes and the match list along with its other keys. This is done using the `port_to_probes_and_matches` inside `common.py`. 

The docstring for the function and the comments are sufficient enough I hope to understand what is going on.


This is the raw `data` for reference. I can't even print it because it takes so much time! Its big as hell. Even loading it into memory is an exhaustive process.
```
service_logger:
- value: 21
  probe:
  - Probe TCP GenericLines q|\r\n\r\n|
  - Probe TCP Help q|HELP\r\n|
  regex: &id002
    - 'match acpc m|^Usage: Valid commands are\nLIST\nCLEAR\nSTATUS\nKILL\nNEW\nCONFIG\nAUTONCONNECT\nGETINFO\nHELP\nFor
      specific help on each command, type HELP:COMMAND\r\r\n\n| p/Glassfrog computer
      poker server/'
    - match aleph m|^96\r$| p/Aleph Integrated Library System/
    - match bitkeeper m|^@SERVER INFO@\nPROTOCOL=([\d.]+)\nVERSION=bk-([\w._-]+)\nUTC=\d+\nTIME_T=\d+\nROOT=([^\n]+)\nUSER=(?:[^\n]+)\nHOST=(?:[^\n]+)\nREALUSER=(?:[^\n]+)\nREALHOST=([^\n]+)\nPLATFORM=([^\n]+)\n|
      p/BitKeeper distributed VCS/ v/$2/ i/protocol $1; root $3; $5/ h/$4/ cpe:/a:bitmover:bitkeeper:$2/
    - match chat m|^\r\n>STATUS\tset status\r\nINVISIBLE\tset invisible mode\r\nMAINWINDOW\tshow/hide
      main window\r\n| p/Simple Instant Messenger control plugin/
    - 'match cvspserver m|^cvs \[pserver aborted\]: bad auth protocol start: HELP\r\n\n?$|
      p/cvs pserver/'
    - 'match cvspserver m|^cvs \[server aborted\]: bad auth protocol start: HELP\r\n$|
      p/CVSNT cvs pserver/ cpe:/a:march-hare:cvsnt/'
    - 'match cvspserver m|^cvs \[server aborted\]: bad auth protocol start: HELP\r\nerror  \n$|
      p/CVSNT cvs pserver/ cpe:/a:march-hare:cvsnt/'
    - 'match cvspserver m|^cvsnt \[server aborted\]: bad auth protocol start: HELP\r\nerror  \n$|
      p/CVSNT cvs pserver/ cpe:/a:march-hare:cvsnt/'
    - 'match cvspserver m|^cvsntsrv \[server aborted\]: bad auth protocol start: HELP\r\nerror  \n$|
      p/CVSNT cvs pserver/ cpe:/a:march-hare:cvsnt/'
    - 'match cvspserver m|^cvs-pserver \[pserver aborted\]: bad auth protocol start:
      HELP\r\n\n| p/cvs pserver/'
    - 'match cvspserver m|^-f \[pserver aborted\]: bad auth protocol start: HELP\r\n\n|
      p/SunOS cvs pserver/ o/SunOS/ cpe:/o:sun:sunos/a'
    - match echo m|^HELP\r\n$|
    - match irc-proxy m|^:ezbounce!srv NOTICE \(unknown\) :\x02| p/ezbounce irc proxy/
      o/Unix/
    - match ftp m|^220 FTP Server[^[]* \[([\w.-]+)\]\r\n214-The following commands are
```

Another problem that I notice here is that, each tread is trying to extract probe and then send it. We shouldn't do that. Again back to the idea of extracting UDP probes directly. It will solve this issue as well. No more wasted resources. I am all for that.

8. the port_to_probes_and_matches function goes over each `value` field which is bascially the port number and checks if it matches the one we are CURRENTLY looking for.

BRUH THIS IS HIGHLY inefficient. This works for the version_scanning part because we are only testing selective ports there but here!? HERE we have to use ALL the ports. There is absolutely no reason for all threads to keep checking if it matches their port. NAHH. HAVE to change the function now. This is the root cause of all issues.

9. The extracted probes are then used to probe and get a response.

Since the process is sooo slow due to the above mentioned inefficiencies, I have never really seen a response from UDP scan :(. Creating a new function now.