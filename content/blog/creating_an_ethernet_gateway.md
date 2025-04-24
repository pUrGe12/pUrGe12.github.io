+++
title = "creating a gateway"
date = 2025-04-18
draft = false

[taxonomies]
categories = ["Hardware" ,"Homelab", "Networking"]
tags = ["Monitoring"]

[extra]
lang = "en"
+++


Update: 20th April, bought one. The adapter has its own network interface inside that is indepedent of the motherboard's NIC. So, this might work (assuming my LAN cables work)

---

Got this, setting up a static IP address for this interface. 

old_laptop: 192.168.42.1
new_laptop: 192.168.42.2

So, ping works. Next, I will have to enable IP forwarding in my old laptop so that I can handle the traffic properly.

This is what I did on my host machine (because the interface shown here was a direct RJ45 connection)
```sh
sudo ip addr add 192.168.42.2/24 dev eno1
sudo ip link set en01 up
```

and this is what I did on my old laptop

```sh
sudo ip addr add 192.168.42.1/24 dev en<some_big_ass_string>
sudo ip link set en<some_big_ass_string> up
```

This was such a weird interface because it uses a USB-to-ethernet adapter. After this ping works.

This can act as a proper bridge and hence monitor my logs as well. Pretty useful stuff. BTW pls do ignore if I make some errors here and there, I am pretty drunk. 

The next step is then to enable IP forwarding. This is basically a single bit that decided whether it needs to be forwarded or not and it can be set in the file, `/proc/sys/net/ipv4/ip_forward`.

>[!NOTE]
> So, I have set this up to be a persistent thing, and I am not sure if this was a right choice. Now, if something doesn't work, later when I don't want this to work (i hope you get what I mean) then I will surely come back to this as the first point to be checked.

---


So, I will now setup my default gateway as the new laptop. This is risky (cause it might mess up shit)

```sh
sudo ip route add default via 192.168.42.1
``` 

and to revert, we follow this,

```sh
sudo ip route del default via 192.168.42.1
```

Writing this just in case something fails.

This needs to be written in the old laptop;
```sh
sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE
```

This is extremely important because this is what ends up setting the rules for the network traffic. That allows forwarding but it isn't much help unless I manully add a DNS IP.

The way this works is:

- Your router provides an IP + gateway + DNS (via DHCP)
- Thus, everytime you connect, you get yourself these necessesities including say the local DNS server that might be running, in which case the router acts as a relay to push that to 8.8.8.8 or something.

Now in our case, we've defined everything statically, so, we'll have to do the same for the DNS server! This can be done by editing the `/etc/resolv.conf` file. This means I will rewrite whatever DNS IP the institute router was giving me and saying something like no matter where you wanna go, use 8.8.8.8 or 1.1.1.1.

Running on the new one.

```sh
sudo resolvectl dns enx<interface> 8.8.8.8 1.1.1.1
sudo resolvectl domain enx<interface> '~.'
```

---

For the server files itself, I changed the samba configurations to route via the ethernet interface (goodbye wireless, for now), and I changed my aliases, tested it and its beautiful!

Now I have a static IP, I can just plug this ethernet cable and boom network attached storage (wired). Also, the webserver seems to work well. Now the next challenge is to make this persistent, which I have done via the following changes:

1. Persistence for the static IPs over the specific ethernet interface in both laptops

```sh
sudo nmcli con add type ethernet ifname eno1 con-name wired-static ip4 192.168.42.2/24 gw4 192.168.42.1
sudo nmcli con mod wired-static ipv4.dns "8.8.8.8 1.1.1.1"
sudo nmcli con mod wired-static ipv4.method manual
sudo nmcli con up wired-static
```

So, in both my laptops its `NetworkManager` who is doing the "managing" part ig so, we can use nmcli to setup the persistent setups. Similarly, we can do this in the old one.

```sh
# Create a static connection profile
sudo nmcli con add type ethernet ifname en<name> con-name wired-static ip4 192.168.42.1/24

# Set no DHCP and apply now
sudo nmcli con mod wired-static ipv4.method manual
sudo nmcli con up wired-static
```

2. Defined cronjobs for setting up the `postrouting` rule in the old laptop and `gateway` setup in the new one on reboot.

That should be it. Now as soon as I connect the ethernet cable, I can run `get_nas` and `start_server` and I will get everything I need!

---

## Making the webserver better

So, I learnt about `tshark` which is basically the CLI version of wireshark, and setting that up is easy. First I will have to add that to the sudoers file though

```sh
sudo visudo
```
and inside that,

```sh
purge ALL=(ALL) NOPASSWD: /usr/bin/tshark
```

Then I can simply define that in `app.py` and run that nicely. The specific command I want to run is

```sh
sudo tshark -i en<name> -T json -Y "ip.addr == 192.168.42.2"
```

This gives a nicely formatted json and filters that too. I want to eventually figure out a way to set these filters dynamically, and make the UI for this, as currently its only just printing stuff there.

---

## ON TO DOING BETTER

So, I got my hands on a tplink Archer C50 version 6.8 router. It sadly doesn't support openWRT but its pretty cool. I set it up to assign static IPs to all devices connected to it. This is done by the `binding` tne MAC address of the connected device to a IP address. So, within the LAN, all connected devices have known ip addresses.

Since this router will also act as a hub, I can connect two devices to it, assign them static IPs and then make them talk to each other. Thus, my NAS is now wireless! (Only need ethernet cables if I have to configure the router).

A small skill issue in my side, my room's ethernet port given by the institute is broken (I am pretty sure these idiots broke it during cleaning for placements or something), so I can't connect that to wifi yet and forward all the requests. Another thing is that, I will probably have to rethink the traffic monitoring idea now, because my packets are no longer being passed through the old laptop.

Pondering...