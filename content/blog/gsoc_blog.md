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