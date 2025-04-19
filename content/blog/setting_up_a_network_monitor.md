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

---

Alright so the first step I figured I will try is just directly piping the output of tcp dump to my flask server. Then I will add some filtering options (which will probably be difficult). So direct `tcpdump` I will simply run that as a subprocess, something like this

```py
def generate_tcpdump():
    process = subprocess.Popen(
        ['sudo', '/usr/bin/tcpdump'],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        text=True,
        bufsize=1
        )

    for line in process.stdout:
        yield f"data: {line.strip()} \n\n"

@app.route("/tcpdump", methods=["GET"])
def show_work():
    return Response(generate_tcpdump(), mimetype='text/plain')
```

This works nicely for now. The only thing to keep in mind is, to avoid giving the sudo password, we can add ourself to the sudoer list for tcpdump.

```sh
sudo visudo
```

Then inside that, add the following line:
```sh
<username> ALL=(ALL) NOPASSWD: /usr/bin/tcpdump
```
Make sure the path for tcpdump is correct. This will allow the server to run this tcpdump without any password. 

I realised late that with this implementation, doing filtering and all will be pretty hard (I am not sure how I'll do it) so we'll see.

Additionally, there are some issues.

1. I can't run mitmproxy during startup because that requires a terminal interface and cronjob doesn't support that.
2. This means if I want to get the right logs, I will have to setup the proxy and ensure that my laptop (old server) isn't turned off.

Ideally it should never be off, but since the IP address I am receiving from the institute is dynamic, it sucks, as I have to setup the proxy from the client to new IP addresses all the time. This is the bigger problem I will try and resolve first. Setting up my own DHCP server that talks to the institute wifi and gets a dynamic address.

This is how the DHCP works, straight from wikipedia docs

> On receiving a DHCP request, the DHCP server may respond with specific information for each client, as previously configured by an administrator, or with a specific address and any other information valid for the entire network and for the time period for which the allocation (lease) is valid. A DHCP client typically queries this information immediately after booting, and periodically thereafter before the expiration of the information. When a DHCP client refreshes an assignment, it initially requests the same parameter values, but the DHCP server may assign a new address based on the assignment policies set by administrators.

In my case, the adminstrators probably assign new ip addresses every new day. Not sure of the time.

---

I have a cooler idea now:

- Firstly we need static IPs cause otherwise its a pain.
- I found an ethernet cable lying around that I want to use.
- I can setup the ethernet connection on a different interface `eth0` and forward my internet requests through that in my new laptop
- The server can provide a static IP to itself and the new laptop over this interface.
- The client will then route its internet requests via the eth0 interface to the server first, who will use the dynamic IP assigned to it by the institute's DHCP server to connect to the internet.

I am not sure if this will work. Will test this out.

### Commands I am running (for reference)

So my old laptop detects the ethernet interface but doesn't have the drivers for it. So step 1 is installing the right driver. It uses intel's e1000e driver so,

```sh
modinfo e1000e  # This works
sudo modprobe e1000e
```

I checked that the drivers exist and are not bound because of something called the `ULP` mode. From the docs what I could understand is:

- This mode is a part of the Energy Efficient Ethernet (IEEE 802.3az) and not an intel thing.
- When ULP is enabled, the Ethernet controller may enter a low-power state that makes it less responsive.

The thing is the old server was previously my dad's business laptop and ULP is enabled in the UEFI by default (It supports legacy as well but who cares about that).

This is so fucked. So apparently my e1000e doesn't discover the NIC hardware (its not listed in the modinfo). I tried install a newer version of the e1000e driver and BAM! API misconfigs, deprecated functins etc. This is so frustrating. Without this I can't even setup a simple LAN connection.

For some reason manually binding the driver raises the issuse that "the file/directory cannot be found". BRUH I AM SITTING RIGHT HERE. its infront of me. Annoying as hell.

---

https://unix.stackexchange.com/questions/625912/e1000e-error-with-b460-motherboard-and-intel-i219-v-chipset

Ahh, mostly likely my driver is bad as well. It is somehow "stuck" in ULP and it contantly tries to achieve that. The mailing list mentioned has code to continue execution even if ULP failed, but I am not if following that is right.

With this I also figured that since the old laptop was my dad's `business` laptop, they have not even given the name of the mother board used in that. From what I could find online its a fully custom board built specifically for this laptop. This is the worst news ever because:

1. My entire day of solving this hardware issue through software and kernel debugging was waste
2. I can't even replace the motherboard

I might try the patches mentioned in the mailing list tomorrow and see if those work. I have some time to kill before 20th cause then I am locking in and studying. So why not. Let's see if I can get something working.

---

So, I have the e1000e driver version 3.8.7 loaded and ready. Running `make` is a pain because I think there is a kernel version mismatch, as this driver proably expects an older kernel (this is downloaded straight from the intel website). I think this to be the case because my new laptop has the e1000e driver working correct without any ULP errors, has the same kernel version `6.8.0-57-generic` and consequently the builds fail in that as well. I guess intel patched the driver for future versions of the kernel but hasn't included that on their website. So I have three choices:

1. Switch to an older kernel permanantly (Easy but not a good idea as its not maintained and is probably buggy)
2. Patch the driver myself
3. Download the linux source code (that will come with the patched driver) and apply the bypass for ULP.

I will first test out option 2 cause that seems fun.

---

Alright, after a day of trying to fix the `netdev.c` and `ethtool.c` I ran into some struct definition errors in `ptp.c`, and at this point I realised I am basically wasting my time because there are a lot of dependencies that I will need to take care of now. This is too painful so I am switching to option 3 now.

Alright so I got kernel v6.8 cloned and tried making it. Note that running `make` won't work because the Makefile expects to be included in the kernel build system, and is not a standalone thing. So, I had to run

`make -C /lib/modules/$(uname -r)/build M=$(pwd) modules`

The good thing is the build passed. sigh... If only I did this yesterday :(.

---

Sad stuff happened, cause turns out the patch I wanted to do is already there. haha. :(((. What the fuck. 