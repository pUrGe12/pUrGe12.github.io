+++
title = "Installing and setting up renode"
date = 2026-06-15
draft = false

[taxonomies]
categories = ["Hardware", "emulator"]
tags = ["blog"]

[extra]
lang = "en"
+++

Welcome to the renode setup. I hope you know why you want to do this, it won't take much time (depending on your internet speed) and I won't be explaning anything other than the problems I faced and how to exactly do it.

## Go through the readme

The initial parts are chill. I am trying to install this on a linux machine, so I can just use the linux portable version:

```sh
mkdir renode_portable
wget https://builds.renode.io/renode-latest.linux-portable.tar.gz
tar xf  renode-latest.linux-portable.tar.gz -C renode_portable --strip-components=1

# Add it to path
cd renode_portable
export PATH="`pwd`:$PATH"
```

Then we need to install all related dependencies. At this point you should create a python virtual env and activate it.

## Dotnet part

Dotnet installation is a little painful. The first thing you need to do is check which debian version you are on:

```sh
cat ~/etc/debian_version
```

Here, `bookwork/sid`: 12, `trixie`: 13

Before you go on following the instructions for dotnet installation for these versions though, be aware that's probably not gonna work.

For example, I use ubuntu 22.04LTS, which is built on top of `bookworm` but its NOT bookworm. It has its own kernels and all.

> Going forward always ignore the debian instruction. I am ubuntu.

And `.net` doesn't maintain support for my ubuntu 22.04LTS, but `canonical` does. They have a .NET backports PPA (Personal Package Archive) though [some sources](https://www.reddit.com/r/linux/comments/vmkex5/ubuntu_ppas_are_insecure_how_canonical_gets/) say that its insecure, but like... okay. We'll see about this later.

Very luckily dotnet 10.0 has its EOL on November 14th, 2028, so I can install a version >= 6 (which is a requirement)

```sh
sudo add-apt-repository ppa:dotnet/backports
sudo apt-get update && sudo apt-get install -y dotnet-sdk-10.0
``` 

Note that the documentation for installation doesn't mention if you need the SDK or the runtime. I am assuming its the SDK cause they mentioned GTK as well. Maybe its a UI thing.

Ensure that it is in path, otherwise you'll face trouble later

```sh
export PATH="$PATH:/home/purge/Desktop/fauvido/Stuff_new/renode_portable"
```

## Robot framework

> To write and run test cases, Renode integrates with the Robot testing framework

Just install the requirements and make sure you have a python virtual env

```sh
pip install -r requirements.txt
python3 -m pip install -r tests/requirements.txt
```

---

> Note you could always just run it in a docker container like they have mentioned but this is more fun

Now you can run renode! More on that soon...
