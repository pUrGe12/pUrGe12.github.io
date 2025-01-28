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

So, these are your best guides. 

1. **Refer to Zola Documentation**: The [official Zola documentation](https://www.getzola.org/documentation/) is a fantastic resource. It explains everything from setup to theming.
2. **Pick a Good Theme**: Zola has several ready-made themes available [here](https://www.getzola.org/themes/). If you're like me and not a webdev dude, then using a theme is the best way to get a running site. 

# Action and yml files

### What are yml files?

YML (or YAML) files are human-readable configuration files. They are used to define the steps and dependencies in your workflow. They basically tell GitHub what and how should your project be executed and rendered. It should have all the styles that you want to load.

### What is GitHub Actions exactly

GitHub Actions automates tasks. For our purposes, we’ll use it to:  
- Build the Zola site  
- Deploy it to GitHub Pages  

This runs everytime you push code to your repo and it renders your site again (don't worry, the site will still be live meanwhile)

#### The main.yml file

The `main.yml` goes in the `.github/workflows` directory from the root of the repo. 

Here’s an example of a simple `main.yml` workflow for Zola that I used:

```yaml
on: push
name: Build and deploy GH Pages
jobs:
  build:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: checkout main
        uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.G_TOKEN }}
      - name: Prebuild
        uses: oven-sh/setup-bun@v1
      - run: bun install
        working-directory: ./themes/tranquil
      - run: bun x tailwindcss -i styles/styles.css -o static/styles/styles.css --minify
        working-directory: ./themes/tranquil
      - name: build_and_deploy
        uses: shalzz/zola-deploy-action@master
        env:
          # Target branch
          PAGES_BRANCH: gh-pages
          # Provide personal access token
          #TOKEN: ${{ secrets.TOKEN }}
          # Or if publishing to the same repo, use the automatic token
          TOKEN: ${{ secrets.G_TOKEN }}
```

> Don't forget to add your github token in `secrets` (and you cant use GITHUB_ so the docs are a little wrong). I have used the name `G_TOKEN` you can do the same if you wish.

# Final building and deploying

If you look carefully at the `yaml` file then it requires you using **bun**. 

This is how you install bun. (change `zshrc` to bashrc if you need)

```sh
curl -fsSL https://bun.sh/install | bash\
source ~/.zshrc 

bun add -D tailwindcss\
bun x tailwindcss -i styles/styles.css -o static/styles/styles.css --minify\
```

If all this works then you're good to go.

# Adding your own section

> It’s best to copy all template files into your local templates/ directory to avoid breaking updates.

- Go to `home.html`

Add a link to your new section. Ensure that the section you make comes inside `content`.

```sh
mkdir content/new-section
```

- Create \_index.md file

Inside your new section, create a \_index.md file. The syntax should be similar to every other \_index.md files.

```
+++
title = "New Section"
sort_by = "date"
template = "new-section-template.html"
page-template = "page_template.html"
+++

Welcome to the new section!
```

Create the template files, using a similar syntax as every other template files. (just copy paste the boiler plate codes) and save that inside the `/templates` directory

# Local testing

Test your website locally using 

```sh
zola serve
```