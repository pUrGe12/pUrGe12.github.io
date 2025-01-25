+++
title = "WiFi spoofing part B: Creating an ESP32 based WiFi deauther"
date = 2025-01-23
draft = false

[taxonomies]
categories = ["Hacking", "Hardware"]
tags = ["Hardware", "Networks", "Cysec", "blog"]

[extra]
lang = "en"
+++

ESP32 has a wifi adapter inbuilt. It also apparently allows you to send raw wifi packets if you use the ESP-IDF framework and the ieee80211_raw_frame_sanity_check(), an actual bypass that was found after reverse engineering the ESP-IDF source code and binaries. 

The reason I wanna do this is because otherwise people won't be incentivised to click on my honepot, 2 reasons for this

1. It is free and hence less trustworth in the minds of the people
2. People generally don't check available networks (cause most of the times, it automatically connects)

If I can broadcast deauthentication frames posing as my insti AP, and then perform a DoS attack, they will be forced to notice my "iitmwifi_6g" and boom, gotcha!

> TLDR: It did not work, because ESP-IDF won't support sending deauth frames and the working behind the actual raw packet sending is closed source. We will have to use a custom framework and not ESP-IDF, thus a new board like ESP8266. 

I shall do this for another time. If you are `still interested` in going through what I learnt in this frustating process, read through...

## Installing ESP-IDF v5.4 (latest)

- Problems in deauth frames
- Types of frames (testing Action frames and channel switching)
- Deauth support removed from v5.2 onwards apparently

## Installing ESP-IDF v5.2

- deauth frames still not working
- Fucked

## Trying action frames 

- Random switching of channel
- Multiple auth frames in hopes of Denial of Service

## Trying to reverse the ESP-IDF library 

- It's definetly not a hardware issue
- So, if we patch the software -- we can allow deauth frames 
- Jenja has already done that (better than I can do for sure)

### Finding esp_wifi_80211_tx

The problem is mostly in the implementation of `esp_wifi_80211_tx()`. It's stopping us from sending a frame starting with 0xd0 and 0xa0 or something. 

These are all the files that have "esp_wifi_80211_tx" referenced. We'll probably have to look at each of them one by one.

		components/esp_wifi/test_apps/wifi_connect/main/test_wifi_conn.c:        `esp_wifi_80211_tx`(WIFI_IF_AP, ds2ds_pdu, sizeof(ds2ds_pdu), true);
		components/esp_wifi/include/esp_wifi.h:  *            Generally, if `esp_wifi_80211_tx` is called before the Wi-Fi connection has been set up, both
		components/esp_wifi/include/esp_wifi.h:esp_err_t `esp_wifi_80211_tx`(wifi_interface_t ifx, const void *buffer, int len, bool en_sys_seq);

Its present in certain docs as well. This will probably not be very useful 

		docs/en/api-guides/wifi.rst:Meanwhile, :cpp:func:`esp_wifi_80211_tx` is supported at sleep as well.
		docs/en/api-guides/wifi.rst:The :cpp:func:`esp_wifi_80211_tx()` API can be used to:
		docs/en/api-guides/wifi.rst:Preconditions of Using :cpp:func:`esp_wifi_80211_tx()`

		docs/en/api-guides/wifi.rst: - Either ``esp_wifi_set_promiscuous(true)``, or :cpp:func:`esp_wifi_start()`, or both of these APIs return :c:macro:`ESP_OK`. This is because Wi-Fi hardware must be initialized before :cpp:func:`esp_wifi_80211_tx()` is called. In {IDF_TARGET_NAME}, both ``esp_wifi_set_promiscuous(true)`` and :cpp:func:`esp_wifi_start()` can trigger the initialization of Wi-Fi hardware.

		docs/en/api-guides/wifi.rst: - The parameters of :cpp:func:`esp_wifi_80211_tx()` are hereby correctly provided.

		docs/en/api-guides/wifi.rst:Theoretically, if the side-effects the API imposes on the Wi-Fi driver or other stations/APs are not considered, a raw 802.11 packet can be sent over the air with any destination MAC, any source MAC, any BSSID, or any other types of packet. However, robust or useful applications should avoid such side-effects. The table below provides some tips and recommendations on how to avoid the side-effects of :cpp:func:`esp_wifi_80211_tx()` in different scenarios.

		docs/en/api-guides/wifi.rst:       Side-effect example#1 The application calls :cpp:func:`esp_wifi_80211_tx()` to send a beacon with BSSID == mac_x in AP mode, but the mac_x is not the MAC of the AP interface. Moreover, there is another AP, e.g., “other-AP”, whose BSSID is mac_x. If this happens, an “unexpected behavior” may occur, because the stations which connect to the “other-AP” cannot figure out whether the beacon is from the “other-AP” or the :cpp:func:`esp_wifi_80211_tx()`.

		docs/en/api-guides/wifi.rst:       - If :cpp:func:`esp_wifi_80211_tx` is called in station mode, the first MAC should be a multicast MAC or the exact target-device’s MAC, while the second MAC should be that of the station interface.

		docs/en/api-guides/wifi.rst:       - If :cpp:func:`esp_wifi_80211_tx` is called in AP mode, the first MAC should be a multicast MAC or the exact target-device’s MAC, while the second MAC should be that of the AP interface.

Checking `components/esp_wifi/include/esp_wifi.h` and this is the metadata we find

		/**
		  * @brief     Send raw ieee80211 data
		  *
		  * @attention Currently only support for sending beacon/probe request/probe response/action and non-QoS
		  *            data frame
		  *
		  * @param     ifx interface if the Wi-Fi mode is Station, the ifx should be WIFI_IF_STA. If the Wi-Fi
		  *            mode is SoftAP, the ifx should be WIFI_IF_AP. If the Wi-Fi mode is Station+SoftAP, the
		  *            ifx should be WIFI_IF_STA or WIFI_IF_AP. If the ifx is wrong, the API returns ESP_ERR_WIFI_IF.
		  * @param     buffer raw ieee80211 buffer
		  * @param     len the length of raw buffer, the len must be <= 1500 Bytes and >= 24 Bytes
		  * @param     en_sys_seq indicate whether use the internal sequence number. If en_sys_seq is false, the
		  *            sequence in raw buffer is unchanged, otherwise it will be overwritten by WiFi driver with
		  *            the system sequence number.
		  *            Generally, if esp_wifi_80211_tx is called before the Wi-Fi connection has been set up, both
		  *            en_sys_seq==true and en_sys_seq==false are fine. However, if the API is called after the Wi-Fi
		  *            connection has been set up, en_sys_seq must be true, otherwise ESP_ERR_INVALID_ARG is returned.
		  *
		  * @return
		  *    - ESP_OK: success
		  *    - ESP_ERR_WIFI_IF: Invalid interface
		  *    - ESP_ERR_INVALID_ARG: Invalid parameter
		  *    - ESP_ERR_WIFI_NO_MEM: out of memory
		  */


> [NOTE]
> Currently only support for sending beacon/probe request/probe response/action and non-QoS data frame

This is exactly what we want to bypass.

I was being too ambitious. After a bit of researching I found that the implementation of this function is mostly likely close-sourced. Thus, even replicating the certain specifics is going to be difficult as fuck.

## Alternative approach

https://github.com/GANESH-ICMC/esp32-deauther/tree/master

Found this cool github project that supposedly bypasses the `invalid arguments` error and sends the deauth frames anyway without using the in-built `idf.py build` function.

So, this requires us to use `make` instead of `idf.py build`, What exactly is the difference between `idf.py build` and `make`? I don't know. Going through issue#3 tells that

		- Hi Garfius, I'm interested in this project, where can I download the Built v4.1-dev-763-ga45e99853? does it also work with the latest 4.1 dev on the site at https://github.com/espressif/esp-idf/releases/tag/v4.1-dev?

		reply: Yes, it works with idf 4.1

So, there goes another day of installing a new esp-idf version! That's one. Also, the open pull request (#14) suggests a method to use idf.py instead of `make` which is now considered legacy.

This is done by adding this line

		target_link_libraries(${COMPONENT_LIB} -Wl,-zmuldefs)

at the end of the `CMakeLists.txt` inside the `main` directory. 

Quoting the author of the PR:

> In compiled [ESP32 WiFi Stack libraries](https://github.com/espressif/esp32-wifi-lib) there is a function `ieee80211_raw_frame_sanity_check` that blocks some types of raw 802.11 frames from being sent. Using `zmuldefs` linker flag during compilation (see `main/CMakeLists.txt`) this function from WiFi Stack librabries can be overriden to always return `0` which leads to unrestricted raw frame transmission.

So now the procedure becomes

1. Clone the esp-idf v4.1 
2. Install the requirements and build it properly using `esp-idf build`
3. Flash it and monitor (`idf.py flash && idf.py monitor`)

Going through issue#10 in that,

		Hi and thank you for the work provided !
		I built the project with make (I used the exact esp-idf commit you provided in readme), applyed the patch and flashed the device, everything works great (although I had to run "idf.py build" before anything to build the partition_table folders and files..., it may be added to the readme...).
		So I started the device, connected to Putty via Serial where I can see the deauth messages flowing without error ... but nothing else happen...
		I replaced the MAC address of my Wifi AP in main.cpp and let the TARGET address as is (FF:FF:FF:FF:FF:FF).
		I can't see any deauth or deassoc in wireshark (filter "wlan.fc.type_subtype eq 0xc or wlan.fc.type_subtype eq 0xa") and my computer (connected to this AP) shows steady wifi connexion....
		Am I missing something ? How did you debug such case ? Thank you !

From what I can paraphrase, the AP address needs to be changed and the Target address can remain the broadcast. 

I will first have to find the MAC address for the AP I am trying to target. I have a scanning code, I will use that. 

#### Starting 

First, cloning esp-idf 4.1. Alright this uses `python` and not `python3`. We will have the fix the shebang in the `tools/idf_tools.py` file. 

`#!/usr/bin/env python` becomes `#!/usr/bin/env python3`

also fix the bash sheband in the install script to `#!/bin/bash`

Then using `. ./export.sh` to source the local enviornment.

First, lets test the actual [deatuh script](LinkToIt) (with the 0xC0 byte set) to see if this downgraded version allows this or not. If not then we'll try and bypass. 

---

Meanwhile also add supabase setup for the spoofing page. Why is it not connecting to the board! Packing for lunch.

Haha, got 2 more victims in this 1 hour of lunching. Interesting, the girl has a cgpa of 8.23 but interned in the defence agency and PnG? Crazy stuff. Makes one wonder. Running my elective script to stalk this girl with roll number ee22b143 for a friend (really for a friend!)

My honeypot code is below, its really simple actually but quite fun.

---

Alright, unsupported frame type again for 0xC0. I guess they had removed support for 0xC0 in all versions of esp-idf. Testing the GitHub repo patch now.

I don't think its working. Two explanations

1. The code doesn't work
2. The WiFi system is secured against it (which is very very likely cause it might be a standard protocol nowadays)

---

Well, until I figure something else, I guess I will have to make do with my honeypot and hope people notice an "iitmwifi_6g" and click on that. I have opened an issue explaining my dilema. Let's see.

## Important links

1. https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/linux-macos-setup.html
2. https://blog.spacehuhn.com/wifi-deauthentication-frame
3. https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/
4. https://github.com/GANESH-ICMC/esp32-deauther/issues/26

This is still yet to be tested

5. https://github.com/risinek/esp32-wifi-penetration-tool