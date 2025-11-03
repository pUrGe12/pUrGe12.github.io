+++
title = "GSoC @ OWASP Nettacker"
date = 2025-09-03
draft = false

[taxonomies]
categories = ["opensource"]
tags = ["Networks", "blog"]

[extra]
lang = "en"
+++

> Note: Copied directly from my post in [medium](https://medium.com/@helloitsme0218/gsoc-2025-owasp-nettacker-188ee5f36362)

Hello!

I am Achintya Jai, a 2nd year undergraduate at IIT Madras. This summer I participated in the Google Summer of Code under OWASP. I was working on a vulnerability scanning tool called Nettacker. My focus for the summer was to improve its scanning capabilities and optimising for lower computational overhead.

## About Nettacker

Nettacker is a powerful and extensible open-source tool for automated vulnerability scanning and penetration testing. Nettacker can scan thousands of targets in parallel, detect a wide range of vulnerabilities, and perform brute-force attacks using known wordlists — all with negligible setup, no external dependencies and minimal resource overhead even on standard hardware.

It can provide detailed reports in multiple formats and integrate with multiple databases and dashboards which makes it suitable for both red and blue team cases.

## My contributions

I worked directly on the main GitHub repo as I had been doing before GSoC started. Outside of bug fixes and request based feature implementations I was working on three major things

- Integrating a huey based queuing system for WebUI scans
- Using APSW as a substitute for SQLite for database operations
- A version scanning module

Out of these,

- I have the working version of huey setup running in my local fork (I am yet to make a PR for this as Mr. Sam, the code maintainer, decided this should be included in a later version of Nettacker)
- The APSW port is yet to be merged and is currently open @ [PR1076](https://github.com/OWASP/Nettacker/pull/1076)
- I have a part of the version scanning ready in my local fork (this is a UDP scanning module) [here](https://github.com/pUrGe12/Nettacker/tree/UDP-scanner-full).


According to the provided list of enhancements to be made, I worked on

1. Increasing the code test coverage
2. Improving recon scanning by adding/improving (new) regexes
3. Bug fixing and implementing multiple features

### Following is a list of some of the more important merged PRs:


- #1008: fixed the admin_scan output to include the hit URLs
- #1019: Added base path for directory enumeration
- #1026: Custom wordlist functionality addition for scan modules
- #1056: Fixing database issues
- #1060: Implementing logging response_dependent conditions in socket.py
- #1091: fixing the global flags issue in joomla_template_scan and drupal_theme_scan
- #1077: Unittests for database files
- #1081: Refactor/migrate tests to pytest
- #1107: add custom headers for http requests via CLI and remove sensitive headers before adding it to the database
- #1099: Exclude certain ports from being scanned
- #1113: skipping service discovery, exclude ports and custom HTTP headers to the web
- #1096: unicode encoding of special characters to avoid breaking WAF scans graph
- #1130: pyproject updates to fix warnings issued by pytest
- #1093: Handle OSError for unknown ports in /etc/services
- #1083: Banner grabbing regex fixes for MariaDB and MySQL
- #1072: fixing the create database part of postgresql
- #1085: Adding new report types -> SARIF and DefectDojo compatible

These are the few open PRs which are under review:

- #1076: porting sqlite operations to APSW

- There is a PR for my WebUI improvements which I am yet to release but can be found in my local fork.

- Huey integrated WebUI with live scan tracking

And a PR for new modules for UDP_scans and version_scanning. The latter is a little buggy (that is, a little slow) so it still resides in my local fork.

## Work Summary

Over the course of the summer I mostly carried out research and benchmarks in the side while adding new features and fixing old ones in the main repository. I was in constant contact with my mentor and we had discussed about this approach in advance.

Additionally I made a few extra blog posts over this course which might be interesting to some readers:

1. [Starting with opensource](https://purge12.github.io/blog/opensource/)
2. [Getting the Huey task queue working](https://purge12.github.io/blog/gsoc-blog/)
3. [Problems in version and UDP scans](https://purge12.github.io/blog/gsoc-blog-2/)
4. [Optimising the UDP scan part with minor adjustments](https://purge12.github.io/blog/gsoc-blog-3/)
5. [Updating Huey processing logic for in-memory usage and progress tracking UI](https://purge12.github.io/blog/gsoc-blog-4/)

I helped resolve issues that users were facing, updated documentation based on the same, worked on feedback provided by users on special feature requests and fixed bug as and when I encountered them.

## What’s new

A bunch of cool things came up during this time which aren’t technically a part of GSoC but I am excited to work on:

1. OpenAI gave some credits to Nettacker for us to use their codex, so we need to come up with a clever way to utilise AI for a network pentesting tool.

2. I started working on a streamlit version of the WebUI which will make Nettacker more like a dashboard than a static page.

3. There are some compatbility issues with python3.13 which are to be resolved and me and the Mr. Sam’s (the maintainer) guess is that its due to the SSL modules.

4. From what Mr. Sam has been telling me, there are better ways to cache the module files because right now we’re keeping them open in memory during the entire scan (even when they aren’t needed) which crashes the ulimit

## What I learnt

I had only barely worked on async codebases and had never worked on such a large and impactful project before. I learnt a lot of best practices for python development, especially about the importance and maintainance of the code architecture. I remember Mr. Sam emphasising this to me so many times when I would “hack” my way into an implementation! I also developed an interesting in networks and network security in general. I started out a homelab, from NAS servers, to upgrading with RPis and a switch and an old laptop which I bought of cheap.

I became an OWSAP member (now I have an OWASP mailing address!), took part in programs other than Nettacker (GenAI security initiatives) and used their resources to help me understand best practices for secure coding in python.

I also applied for a talk at OWASP AppSec Bangalore 2025 to speak on Nettacker! This was the first time I applied to any conference so I am psyched (thought I didn't get it :()

## Acknowledgements

I would begin by thanking my mentors [Mr. Sam](https://github.com/securestep9) and [Mr. Arkadii](https://github.com/arkid15r) for being so helpful throughout the summer. A big thank you to everyone who has worked on this tool before and made it such a big success, and good luck to all who will be building Nettacker in the future. Thank you to Google for running such a program and improving the status of OpenSource among students like me.

To learn more about my contributions and code just visit the GitHub repo linked at the start of the document and use the tool! Hope you have a good time (and please attack responsibly!)