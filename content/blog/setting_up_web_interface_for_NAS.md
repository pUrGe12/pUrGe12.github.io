+++
title = "A flask based UI for NAS"
date = 2025-04-14
draft = false

[taxonomies]
categories = ["Hardware" ,"Homelab", "Networking"]
tags = ["NAS", "Flask"]

[extra]
lang = "en"
+++

A simple webserver that allows me to put up multiple files from my client laptop and save them in the samba directory in the NAS server if we're over the same LAN. The only issue is the dynamic IP address of the server, so for now, I was forced to use supabase to store the address and created aliases for each access.

---

The minimalistic look of just uploading files to a folder and seeing it be saved on the old laptop was pretty good in and of itself. But to take it further, I decided to make a nice webUI that I can access with any laptop over the same LAN with authentication and upload files. This might come in handy in the future, as I want to slowly convert this from just a NAS server to a full blown multiple thingie server (I am really not sure what I want to do, but I have let my imaginations run wild).

The code for the server was pretty simple only

```python3
from flask import Flask, request, redirect, url_for, render_template, flash, Response
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess

path = Path("/home/purge/server_files/.env")
load_dotenv(dotenv_path=path)

UPLOAD_FOLDER = '/home/purge/sambashare/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'}

# Basic auth credentials
USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")

app = Flask(__name__)
app.secret_key = os.getenv("secretkey")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Login required.', 401, {'WWW-Authenticate': 'Basic realm="Restricted Area"'})


def parse_result(result):
    """
    This is how the normal result looks like

● smbd.service - Samba SMB Daemon
     Loaded: loaded (/lib/systemd/system/smbd.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2025-04-14 00:27:39 IST; 7min ago
       Docs: man:smbd(8)
             man:samba(7)
             man:smb.conf(5)
    Process: 1209 ExecStartPre=/usr/share/samba/update-apparmor-samba-profile (code=exited, status=0/SUCCESS)
   Main PID: 1229 (smbd)
     Status: "smbd: ready to serve connections..."
      Tasks: 5 (limit: 4511)
     Memory: 19.2M
        CPU: 239ms
     CGroup: /system.slice/smbd.service
             ├─1229 /usr/sbin/smbd --foreground --no-process-group
             ├─1239 /usr/sbin/smbd --foreground --no-process-group
             ├─1240 /usr/sbin/smbd --foreground --no-process-group
             ├─1249 /usr/lib/x86_64-linux-gnu/samba/samba-bgqd --ready-signal-fd=45 --parent-watch-fd=11 --debuglevel=0 -F
             └─1289 /usr/sbin/smbd --foreground --no-process-group

Apr 14 00:27:38 Purge12 systemd[1]: Starting Samba SMB Daemon...
Apr 14 00:27:39 Purge12 systemd[1]: Started Samba SMB Daemon.
Apr 14 00:27:40 Purge12 smbd[1289]: pam_unix(samba:session): session opened for user purge(uid=1000) by (uid=0)
    """
    return result


def get_samba_status():
    try:
        result = subprocess.run(["systemctl", "status", "smbd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return parse_result(result.stdout.strip())
    except Exception:
        return ""

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    samba_status = get_samba_status()
    if request.method == 'POST':
        files = request.files.getlist('file')
        uploaded_files = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                uploaded_files.append(filename)

        if uploaded_files:
            flash(f"Uploaded: {', '.join(uploaded_files)}")
        else:
            flash("No valid files uploaded.")
        return redirect(url_for('upload_file'))
    aliases = """
        <some aliases I defined for myself>
    """

    return render_template('upload.html', samba_status=samba_status, alias = aliases)        # Here add the aliases ive set up too (make life easier)

# Finish this.
@app.route("/work", methods=["GET"])
def show_work():
    work_files = ["Nettacker"]              # I am only going to consider this as work for now
    for work in work_files:
        pass
    return render_template('work.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

I was working on creating more endpoints but more on that later. This is a very basic server, I can go and upload multiple files together and save them in my NAS.

The HTML files are just for styling, I'll leave that out here. I can access this website by visiting

```
http://<NAS_server_private_ip>:5000
```

from any device on the same LAN.

> I did spend a lot of time fixing the UI and making it look aesthetic for no apparent reason.

---

The only issue is, my old laptop (the "NAS") relies on my institute router for DHCP assignments and from the way its een configured, the IP address for the NAS changes every day.

Thats a huge issue because now my aliases don't work, I can't rely on the same link forever and I will have to manually see what the IP is for that day and connect to that. The mounts also change.

There are a few ways I can mitigate this but the simplest one for now (because I don't have money to buy up a router and rpis and create a full substitute for my institute network) is to:

- Reset the server every morning. Run a script to find the current IP address, put it up in pastebin.
- Run the script to connect to the server from the client which will pull the IP from pastebin and mount the samba shared file on that and connect with it via HTTP.

I can't use something like `redis` because for remote connections I will need the private IP of the server which is exactly the issue I am trying to mitigate!

---

pastebin sucks, it will generate a new unique ID for every paste that means I'll have to again manually check out what that id is and then query based on that. Nah. I will use supabase.

So, I am creating a different script that I will add to the `cronjobs` to run every morning once at 5am. It will check the laptop's IP address for that day, and save that in the supabase table. Then my alias here to start the server will basically be something like

1. Run a script that fetches the IP for that day
2. Pipe that into the mount command and the the webserver address
3. Run gchrome.


This code runs every morning in the server:

```py

from supabase import create_client, Client
import subprocess

# Supabase to send and save IP everytime
url: str = ""
key: str = ""

supabase: Client = create_client(url, key)
command = "ip -o -4 addr list | awk '{print $4}' | grep -v 127"

try:
	result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, shell=True)
	ip_addr = str(result.stdout.strip().split("/")[0])
	print(ip_addr)
except Exception:
	ip_addr = ""	# Something's wrong, but it shouldn't be
info = {"IP": ip_addr}
response = supabase.table("IPs").insert(info).execute()
```

I ran this using a `cron_script.sh` and defined that inside my cronjobs using `crontab -e`. For redundancy, I am running this on every boot as well in case I miss the cronjob because my laptop was plugged out or something.

Now in the client side what I need is, everytime I turn my laptop on, or every morning at 10am (and then 12pm cause I will have defently opened my laptop and kept it running by them, like 100% sure), query the database, get the latest ip, update the aliases and boom.

The aliases I have defined are for

1. mounting the NAS directory in the client
2. unmounting the directory
3. Starting the webserver in a new tab using google chrome

So, I created a different file called ".custom_aliases" which I will be sourcing into .zshrc all the time. This is effectively the same thing but this makes it more persistent.

```sh
echo '[ -f ~/.custom_alises ] && source ~/.custom_alises' >> ~/.zshrc
```

This is to source it on every terminal startup. To write to it,

```py
from supabase import Client, create_client
import os

url: str = ""
key: str = ""

supabase: Client = create_client(url, key)

response = supabase.table("IPs").select("IP").order("id", desc=True).limit(1).execute().data
IP_addr = str(response[0].get("IP"))

nas_alias = f'alias get_nas="sudo mount -t cifs //{IP_addr}/sambashare /mnt/nas -o username=<your_username>,uid=$(id -u),gid=$(id -g),rw,vers=3.0"'
start_server_alias = f'alias start_server="google-chrome --new-window http://{IP_addr}:5000/"'

alias_file_path = os.path.expanduser("~/.custom_aliases")

if os.path.exists(alias_file_path):
	with open(alias_file_path, "r") as f:
		lines = f.readlines()
else:
	lines = []

def update_or_append(lines, alias_name, new_line):
	updated = False
	for i, line in enumerate(lines):
		if line.startswith(f"alias {alias_name}="):
			lines[i] = new_line + "\n"
			updated = True
			break
	if not updated:
		lines.append(new_line + "\n")

	return lines

lines = update_or_append(lines, "get_nas", nas_alias)
lines = update_or_append(lines, "start_server", start_server_alias)

with open(alias_file_path, "w") as f:
	f.writelines(lines)

print("updated aliases")
```

Now all I have to do is define this as a cronjob. 

```sh
@reboot /home/username/Desktop/nas_alias_creator.sh
0 10 * * * * /home/username/Desktop/nas_alias_creator.sh
0 12 * * * * /home/username/Desktop/nas_alias_creator.sh
```

---

So, how will accessing this work? Simple, once a day I will have to run

0. `remove_nas` (an alias for unmounting)
1. `get_nas`
2. `start_server`

That's it for that day. The start_server is good enough but get_nas is a pain because I don't want to unmount remount! This is for another day though because the next step to mitigate the issue of dynamic addresses is getting my own router.