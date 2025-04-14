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

- Reset the server every morning. Run a script to find the current IP address, put it up in pastebin or just redis.
- Run the script to connect to the server from the client which will pull the IP from the redis database or pastebin and mount the samba shared file on that and connect with it via HTTP.

