+++
title = "Creating a NAS server"
date = 2025-04-13
draft = false

[taxonomies]
categories = ["Hardware" ,"Homelab", "Networking"]
tags = ["NAS"]

[extra]
lang = "en"
+++

So my (potential) mentor told me about something called a Homelab, and why it will be useful if I want to learn more about networking. I knew a few things before from CTFs and nmap and nettacker scans, but that's all. I had no idea how to setup my own servers, run services on ports, host websites (will be done in the future after I learn `port forwarding`) for all users on the internet (note that hosting one on the same LAN is so much simpler, cause you don't need to host it at all).

This post is about creating my own NAS server. I am not sure if what I have is really a NAS server but it achieves its purpose. So, I will be describing exacly what I did, the commands I used and the hardware as well.

---

# Hardware

I got this old `intel i3` Dell's laptop. Its got 4GB RAM and 512GB of hard-disk, without any SSD. I didn't really care about the display, all I did care about was the cost (at this point I am living on hackathon money until I get an intern, which I will, hopefully).

![old_laptop_image](old_laptop_now_NAS_server.jpg)

The keyboard doesn't work so I attached an external one. The battery is pretty much gone, it doesn't charge ever, so it needs to be plugged into the charger at all times. But other than these minor issues, its solid and can run Linux!

# Running Samba

`Samba` is an implmentation of the SMB networking protocol. You can find more on it in its wikipedia page, but what's relevant to us is the fact that its basically a file sharing service.

The idea was to create a samba server that runs on my old laptop such that any other device connected to the same LAN (in my case, my institute wifi `iitmwifi`) can access that server and upload files. These [official docs](https://ubuntu.com/tutorials/install-and-configure-samba#1-overview) by ubuntu explain how to set this up.

## Install and configure samba

Install samba using the following commands

```sh
sudo apt install samba
```

The way samba works is, we create a shared directory that can be used by any other computer if its mounted with authentication. Yes, authentication is important because duh, you probably dont want anyone in the internet to store pics in your device or worse, VIEW the information stored in your device.

So, we create a shared directory, following exactly the steps mentioned in the documentation

```sh
mkdir /home/<username>/sambashare/
```

Now we need to define this as the `samba` directory, and in order to do this all we need to do is edit the `smb.conf` file. This is what I added to the end of my smb.conf file.

```
[sambashare]
	comment = Samba config for my NAS
	path = /home/<your_username>/sambashare
	read only = no
	guest ok = no
	browsable = yes
	valid users = <your_username>
	force group = sambashare
	create mask = 0664
	directory mask = 2775
```

The settings for `force group`, `create mask` and `directory mask` are additional security features. If a user from another machine connects and creates a file, Samba on the server ensures:

- The file gets the right group `sambashare`
- The file gets the right permissions like `664` or `775`

These are server side and just a **background** security thing.

---

At this stage you should setup a password using

```sh
sudo smbpasswd -a <your_username>
```

This is important as its basically a first layer of security for your samba server.

Then all you need to do is restart the smbd service and allow samba traffic through the firewall (more on firewall rules later)

```sh
sudo service smbd restart
sudo ufw allow samba
```

# Access from a client

To access it from my personal device, I first had to get the private IP address of the NAS server (Note that the public IP will be the same as its the same LAN). This can be done using 

```sh
ip a | grep inet
```

I won't reveal the IP here (not that you can hack into it) but once you have yours, you can run this command in the new device and get access to the shared directory

```sh
sudo mount -t cifs //<ip_address>/sambashare /mnt/nas -o username=<your_username>,uid=$(id -u),gid=$(id -g),rw,vers=3.0 
```

You might be wondering what the `uid` and `gid` and `rw` are in the above command and why they're being used. It's got to do with the permissions we set in the `smb.conf` file.

- `uid=$(id -u)` sets ownership to your current user
- `gid=$(id -g)` sets group ownership to your current group
- `rw` forces read/write mode

And I am also forcing a version here because its makes stuff more stable.

> Note that these usernames are all the NAS server's names!

# Additional restrictions

You can try restricting the server to only a certain subnet that you will likely be connecting with.

```
[global]
   interfaces = lo wlan0
   bind interfaces only = yes
   hosts allow = <your_subnet_CIDR_notation> 127.0.0.1
   hosts deny = 0.0.0.0/0
```

If you do this, all scans will show this port as closed because this is available only to the IP addresses on that subnet. To find your subnet, run this

```sh
ip a
```

and look for an active network connection like `WLAN0` or `wlp2s0` etc. Under that you will see an inet address in CIDR notation, that is your subnet, if you set the last byte to `00`.

---

Addtionally you may want to restrict your server from ever closing by

```sh
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

and you probably want to create alias to do the mounting and unmouting for you. This goes inside zshrc or bashrc or whatever else you might be using.

```sh
# Alias for the NAS server's samba folder mounting
alias get_nas="sudo mount -t cifs //<your_ip>/sambashare /mnt/nas -o username=<your_username>,uid=$(id -u),gid=$(id -g),rw,vers=3.0"

# Alias for removing the samba folder
alias remove_nas="sudo umount /mnt/nas"
```

Now you're good.

# Future work

Next up I will try and host a flask server (a very basic one) such that I can just upload files into that and have it be stored in the samba directory. Then I am gonna take it further and eventually have this beautiful endpoint where lots of `crazy` things can happen.