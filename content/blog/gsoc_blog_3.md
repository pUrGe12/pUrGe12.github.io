+++
title = "Project Nettacker: Part 3"
date = 2025-05-29
draft = false

[taxonomies]
categories = ["opensource"]
tags = ["Networks", "blog"]

[extra]
lang = "en"
+++

May 29th 2025,

New day but old stuff.

Another optimization, we don't have to extract the UDP probes all the time! That's just time wasting. Since the port number doesn't matter here, we need to just extract it once and keep using that.

I managed that. But I think all the threads are still running all the ports. I mean think about it, its totally unncessary! Why, if this is the same scenario as the tcp_scan part? 

Let's go over what actually happens:

1. All threads will have to call the extract_udp_probes function. This is bad. Not ideal. No. I should have it like, I have one extracted list, and I pass it to all threads.
2. All threads then run from 1 to whatever the end port is in port.yaml. Not at all ideal! I will have to check how tcp_send_connect_and_recieve does it and just match that.

Alright so in order to make extract_udp_probe really not be running for all the threads, I just need to add that in the sub_step just like I had for the probes. 

I did this, basically did all the extraction in `app.py` and added that as a parameter itself. Now, fix the threading issue.

---

Bruh! I just realised, I am doing everything fine only! I printed which ports I am testing with each thread and I realised that we're testing 1 port with 1 thread, just like it normally works. But earlier, we have just 1 probe, now we have multiple. So, each thread for its own port it trying to throw all probes and see. This is fine I guess, I am not sure if we can parallize this further.

or if I even have to. Alright, so now I only have to see why it won't close nicely when I press ctrl+c, and if verbose works with this.

Yeah, verbose doesn't work. I will have to see this. With `tcp_send_connect_and_recieve` verbose works perfectly as in, we can see which request is being sent and to where. This is probably because I am not returning anything from the function and I haven't added the code to base.py as well. So, it doesn't really know what to do with this except printing the debugging print statements.

Bro also, how do we exactly detect UDP if they don't reply? I think they reply validly if the service is running and the right probe is used. I setup a udp listener just to see and I am hitting the same port (8334).

---

AHHH things work. I have a UDP echo server running using socat

`socat -v UDP-RECVFROM:8334,reuseaddr EXEC:/bin/cat`

Now, I ran into the real issues. I am recieving a response from the UDP server, so I hit this exception:

```
Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/purge/Nettacker/nettacker/core/lib/base.py", line 339, in run
    return self.process_conditions(
  File "/home/purge/Nettacker/nettacker/core/lib/base.py", line 249, in process_conditions
    log.verbose_info(json.dumps(event))
  File "/usr/lib/python3.10/json/__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
  File "/usr/lib/python3.10/json/encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib/python3.10/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
  File "/usr/lib/python3.10/json/encoder.py", line 179, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type bytes is not JSON serializable
```

Hmm. Interesting. 

What if I send TCP probes to the UDP echo server? It just silently drops! YESSSSS! Finally some validation that UDP probes work!

This is the normal event:

```
This is the event that was failing: {'timeout': 3.0, 'host': '127.0.0.1', 'port': 613, 'method': 'tcp_connect_send_and_receive', 'response': {'condition_type': 'or', 'log': "response_dependent['service']", 'conditions_results': [], 'ssl_flag': False}, 'method_version': 'tcp_version_scan'}
```

The event I have that fails has this big ass section called udp_probes! AHHH, I need to delete that in base.py. Yes. The problem probably is that I have added udp_probes in the sub_step, I should delete it from there once the scans are completed. Let's try now. Alright, this sort of works, I am now facing another issue. Let me articulate this once after running.

Firstly, the `method` name is wrong, `method_version` shouldn't be set. I am getting the same response from this as I get from a port_scan for a port that is closed.

---

okay, its been a while, with new clarity I can safetly say that verbose mode doesn't work. The reason i get `method_version` is because it is correct! I am getting verbose output only for `tcp_connect_send_and_recieve`. I will have to see to this. I think, other than that, should be fine. This is cause if I run the command

```sh
python3 nettacker.py -i 127.0.0.1 -m port_scan -g 8334 -v (-sU)
```

with or without -sU, I get the same output (if I don't print anything that is). Verbose needs to do better. Let's first fix that okay.