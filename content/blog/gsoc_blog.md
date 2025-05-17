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