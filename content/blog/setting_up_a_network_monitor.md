+++
title = "Setting up a network monitor on my server"
date = 2025-04-13
draft = false

[taxonomies]
categories = ["Hardware" ,"Homelab", "Networking"]
tags = ["Monitoring"]

[extra]
lang = "en"
+++

The idea now is to use that flask server I created and display network logs in there as well at a certain endpoint. This is pretty cool and I will setup a `mitmproxy` to enable this. So, now all my traffic goes through the server and that is forwarded to the internet (chrome was giving issues with certs so had to use firefox).

Firstly to enable proxy in the client, we need to do the following

## Setting up the proxy in the client

- Settings > Network > VPN > Network Proxy > Manual
- Add this line in there. (keep the port at 8080 only)
```
http://<server_ip>
```

My server_ip is currently dynamic because I am relying on my institute's (or ISP's, I am not really sure) DHCP server to assign IP address. So, I'll have to manually change this if the server's IP changes (which will). 

To remove the proxy just disable it, everything should go back to normal then.

## Starting mitmproxy in the server

I'll be using mitmproxy cause its easy as hell. Note that there are a few caveats with this. Firstly, apt install won't work cause it causes some issues (its described in an issue in their GitHub). We install using pipx

```sh
sudo apt-get install pipx
pipx ensurepath
pipx install mitmproxy
export PATH="$PATH:/gemnasium-maven/.local/bin"
```

This is to be run in the server. Then to start the proxy setup, we simply run

```sh
mitmproxy --mode regular --listen-host 0.0.0.0 --listen-port 8080
```

This will make the server a static observer of all my traffic. Then we can filter based on my client's IP to not read anything other than that (there won't be much, only stray devices trying to connect to my samba service and the server itself).

## Getting certs

Browser's are pretty solid these days and they can easily figure out if a hacker is trying to insert themself in the middle. So, the first thing to do after enabling proxies and starting the mitmproxy service, is to get a valid certificate.

- visit `http://mitm.it`
- Select the os/browser you're panning to set up the proxy on
- Follow the instructions provided and boom

This needs to be done by the client. So, you're actively supporting the MITM (its not an attack...) and you're telling your browsers to do the same.

---

With this basic mitmproxy setup, we can start the process of dissecting this and displaying this in the flask server.