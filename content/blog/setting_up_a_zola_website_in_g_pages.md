+++
title = "Setting up Zola in GitHub pages"
date = 2025-01-25
draft = false

[taxonomies]
categories = ["Dev"]
tags = ["webdev", "blog"]

[extra]
lang = "en"
+++

I figured that its quite easy to host a website using GitHub pages especially for people like me who aren't webdevelopers, but it was not quite so. In this blog I detail the steps I took to setup this website that you're seeing and I will also attempt to explain why certain things were written as they were and the challenges you may run into.

# First principles

- Refer Zola documentation
- Figure out a good theme (especially if you're not a webdev dude and can't make one on your own)

# Action and yml files

### What are yml files?

### What is GitHub Actions exactly

- The main.yml file
- Don't forget to add your token in `secrets` (and you cant use GITHUB_ so the docs are a little wrong)

# Final building and deploying

- Installing bun and other frameworks for tailwind (if using something else then ensure you do that)
- General steps to copy-paste exactly

# Further editing

- Changing colors, messing with stuff etc.
- Adding images and YouTube links 
- Creating a good README.md file

## Adding your own section

- Go to home.html
- Add the link to the new directory
- Create new directory under contents/
- Create \_index.md file, use same syntax, use a page and a page-template
- Create the page and page-template html files, use a similar syntax as others, save it in templates/
- Build and serve locally first