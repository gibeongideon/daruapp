
## Specifications
1. Deploying Django Channels with Daphne & Systemd (running the ASGI app)
    1. Starting the daphne service
    1. Writing a bash script that tells daphne to start
    1. Configuring systemd to execute bash script on server boot


# Create Digital Ocean Droplet with SSH login

#### Create a new droplet

#### Droplet configuration

#### SSH key
Make sure to choose the SSH key option for authentication. Otherwise hackers can simply try passwords to log into your server. This is very bad. Using an SSH key is much, much more secure.

To create an SSH key just click the button "New SSH key" and follow the instructions. **Make sure to save a backup of the private key and public key**. I usually save on an external drive along with on my PC.


#### Your IP
Write down your server ip somewhere. You'll need this for logging into your server.

#### Choose SSH
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/ssh_session.PNG">
</div>
<br>

#### SSH Settings
1. Set the server ip
1. set "root" as username
1. Under "Advanced SSH settings":
    1. click "use private key" and choose the location of where you saved your private key.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/session_settings.PNG">
</div>
<br>

#### Connected
Now connect and it should look like this. There's an FTP on the left and SSH on the right.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/logged_in.PNG">
</div>
<br>

# Install Server Dependencies
Run these commands in the SSH terminal.

`passwd` Set password for root. I'm not sure what the default is.

`sudo apt update`

`sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl`

`sudo -u postgres psql`

CREATE DATABASE darius_db;
CREATE USER darius WITH PASSWORD 'darius!passcode';
ALTER ROLE darius SET client_encoding TO 'utf8';
ALTER ROLE darius SET default_transaction_isolation TO 'read committed';
ALTER ROLE darius SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE darius_db TO darius;
`\q`

`sudo -H pip3 install --upgrade pip`

`sudo -H pip3 install virtualenv`

`sudo apt install git-all`

`sudo apt install libgl1-mesa-glx` Resolve cv2 issue

`adduser django`

`su django`

`cd /home/darius/`

`mkdir daruapp` You can replace "daruapp" with your project name. 

`cd daruapp`

`virtualenv venv`

`source venv/bin/activate`

`mkdir daruapp`

## Update 'prod' branch
Make the necessary changes to the prod branch.

#### settings.py
Top of the file:
```python
from pathlib import Path
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["<ip_from_digital_ocean>",]

ROOT_URLCONF = f'{config("PROJECT_NAME")}.urls'

WSGI_APPLICATION = f'{config("PROJECT_NAME")}.wsgi.application'

ASGI_APPLICATION = f'{config("PROJECT_NAME")}.routing.application'

```

Bottom of the file:
```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = config('AWS_LOCATION')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
TEMP = os.path.join(BASE_DIR, 'temp')
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'darius Team <noreply@codingwithmitch.com>'


BASE_URL = "http://<ip_from_digital_ocean>"
```

#### Create settings.ini file in root directory
```
[settings]
DEBUG=False
SECRET_KEY=e9lgp7glzo&n(l3v&jkwhyt8ye*!o=cwh7y6o@b2a^$muup!#1

DB_NAME=django_db
DB_USER=django
DB_PASSWORD=password

EMAIL_HOST_USER=<some-email@gmail.com>
EMAIL_HOST_PASSWORD=<password>

PROJECT_NAME=daruapp
```

#### Update header.html
The WebSockets will be communicating through port 8001 (we will configure this later). So make sure in all the Javascript WebSockets you are referencing port 8001.
```javascript
var ws_path = ws_scheme + '://' + window.location.host + ":8001/"; // PRODUCTION
````



# Install and Setup Redis
Redis is used as a kind of "messaging queue" for django channels. Read more about it here [https://channels.readthedocs.io/en/stable/topics/channel_layers.html?highlight=redis#redis-channel-layer](https://channels.readthedocs.io/en/stable/topics/channel_layers.html?highlight=redis#redis-channel-layer)

`sudo apt install redis-server`

Navigate to `/etc/redis/`

open `redis.conf`

`CTRL+F` to find 'supervised no'

change 'supervised no' to 'supervised systemd'

`SAVE`

`sudo systemctl restart redis.service`

`sudo systemctl status redis`

Should see this:
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/redis_status.PNG">
</div>
<br>

`CTRL+C` to exit.

`sudo apt install net-tools`

Confirm Redis is running at 127.0.0.1. Port should be 6379 by default.

`sudo netstat -lnp | grep redis`

`sudo systemctl restart redis.service`


# ASGI for Hosting Django Channels as a Separate Application
From the Django channels docs:
> ASGI (Asynchronous Server Gateway Interface), is the specification which Channels are built upon, designed to untie Channels apps from a specific application server and provide a common way to write application and middleware code.

`su django`

Create file named `asgi.py` in `/home/django/daruapp/src/daruapp` with this command:

`cat > asgi.py` 'django' must be the owner of this file.

Paste in the following:
```
"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from decouple import config
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django.setup()
application = get_default_application()

```

`CTRL+D` to save.

You can open the file to confirm everything looks good.

`ls -l` to check ownership. `django` needs to be the owner.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/daruapp_ownership.PNG">
</div>
<br>

# Deploying Django Channels with Daphne & Systemd
Gunicorn is what we use to run the WSGI application - which is our django app. To run the ASGI application we need something else, an additional tool. **[Daphne](https://github.com/django/daphne)** was built for Django channels and is the simplest. We can start daphne using a systemd service when the server boots, just like we start gunicorn and then gunicorn starts the django app.

Here are some references I found helpful. The information on this is scarce:
1. [https://channels.readthedocs.io/en/latest/deploying.html](https://channels.readthedocs.io/en/latest/deploying.html)
1. [https://stackoverflow.com/questions/50192967/deploying-django-channels-how-to-keep-daphne-running-after-exiting-shell-on-web](https://stackoverflow.com/questions/50192967/deploying-django-channels-how-to-keep-daphne-running-after-exiting-shell-on-web)

`su root`

`apt install daphne`

Navigate to `/etc/systemd/system/`

Create `daphne.service`. Notice the port is `8001`. This is what we need to use for our `WebSocket` connections in the templates.
```
[Unit]
Description=WebSocket Daphne Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/django/daruapp/src
ExecStart=/home/django/daruapp/venv/bin/python /home/django/daruapp/venv/bin/daphne -b 0.0.0.0 -p 8001 daruapp.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`systemctl daemon-reload`

`systemctl start daphne.service`

`systemctl status daphne.service`

You should see something like this. If you don't, go back and redo this section. Check that your filepaths are all **exactly the same as mine in `daphne.service`**. That is the #1 reason people have issues.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/daphe_status.PNG">
</div>
<br>

`CTRL+C`

# Starting the daphne Service when Server boots
With gunicorn and the WSGI application, we created a `gunicorn.socket` file that tells gunicorn to start when the server boots (at least this is my understanding). I couldn't figure out how to get this to work for daphne so instead I wrote a bash script that will run when the server boots. 

#### Create the script to run daphne
Navigate to `/root`

create `boot.sh`
```
#!/bin/sh
sudo systemctl start daphne.service
```

Save and close.

Might have to enable it to be run as a script (not sure if this is needed)
`chmod u+x /root/boot.sh`

If you want to read more about shell scripting, I found this helpful:
[https://ostechnix.com/fix-exec-format-error-when-running-scripts-with-run-parts-command/](https://ostechnix.com/fix-exec-format-error-when-running-scripts-with-run-parts-command/).


#### Tell systemd to run the bash script when the server boots

Navigate to `/etc/systemd/system`

create `on_boot.service`
```
[Service]
ExecStart=/root/boot.sh

[Install]
WantedBy=default.target
```
Save and close.

`systemctl daemon-reload`

##### Start it
`sudo systemctl start on_boot` 

##### Enable it to run at boot
`sudo systemctl enable on_boot` 

##### Allow daphne service through firewall
`ufw allow 8001` 

##### Restart the server
`sudo shutdown -r now`

##### Check the status of `on_boot.service`
`systemctl status on_boot.service`

Should see this. If not, check logs: `sudo journalctl -u on_boot.service`
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/on_boot_service_status.PNG">
</div>
<br>

##### Check if the daphne service started when the server started:
`systemctl status daphne.service`

Should see this. If not, check logs: `sudo journalctl -u daphne.service`
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/daphne_service_status.PNG">
</div>
<br>

#### Where are the logs?
journalctl is my general go-to. You can filter specifically for a service like this:
```
sudo journalctl -u on_boot.service // for on_boot.service
sudo journalctl -u daphne.service // for daphne.service
```

# Domain Setup
If you want a custom domain name (which probably everyone does), this section will take you through how to do that.

#### Purchasing a domain
I like to use [namecheap.com](https://www.namecheap.com/) but it doesn't matter where you buy it from. 

#### Point DNS to Digital Ocean

On the home screen, click the "manage" button on the domain you purchased.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/namecheap_home.PNG">
</div>
<br>

In the "nameservers" section, select "custom DNS" and point to digital ocean.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/nameservers.PNG">
</div>
<br>

#### Add the Domain in Digital Ocean

Select your project in digital ocean and click "add domain" on the right.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/add_a_domain.PNG">
</div>
<br>

Fill in your domain name.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/add_a_domain_1.PNG">
</div>
<br>

Add the following DNS records. Replace `open-chat.xyx` with your domain name. And you can ignore the CDN.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/dns_records.PNG">
</div>
<br>

#### Update Nginx config
Earlier we configured Nginx to proxy pass to gunicorn. We need to add the new domain to that configuration.

visit `/etc/nginx/sites-available`

Update `daruapp`
```
server {
    server_name 157.245.134.6 open-chat-demo.xyz www.open-chat-demo.xyz;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/django/daruapp/src;
    }
    
     location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

`sudo systemctl reload nginx`

Make sure nginx configuration is still good.

`sudo nginx -t`

#### Update `ALLOWED_HOSTS`

Navigate to `/home/django/daruapp/src/daruapp/`

Update `settings.py` with the domain you purchased. Also make sure your ip is correct.
```
ALLOWED_HOSTS = ["157.245.134.6", "open-chat-demo.xyz", "www.open-chat-demo.xyz"]
```

Apply the changes

`service gunicorn restart`

## TIME TO WAIT...
It can take some time to see your website available at the custom domain. I don't really know how long this will actually take. I waited about an hour and it was working for me.

#### How do you know it's working?
Visiting your domain you should see this **OR you should see your project live and working**.
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/welcome_to_nginx.PNG">
</div>
<br>

# HTTPS (If you have a domain registered and it's working)
**Do not do this step unless you're able to visit your website using the custom domain.** See [How do you know it's working?](How-do-you-know-its-working?)

#### Install certbot
HTTPS is a little more difficult to set up when using Django Channels. Nginx and Daphne require some extra configuring.

`sudo apt install certbot python3-certbot-nginx`

`sudo systemctl reload nginx`

Make sure nginx configuration is still good.
```
sudo nginx -t
```

#### Allow HTTPS through firewall

`sudo ufw allow 'Nginx Full'`

`sudo ufw delete allow 'Nginx HTTP'` Block standard HTTP  


#### Obtain SSL certificate

`sudo certbot --nginx -d <your-domain.whatever> -d www.<your-domain.whatever>`

For me:
```
sudo certbot --nginx -d open-chat-demo.xyz -d www.open-chat-demo.xyz
```

#### Verifying Certbot Auto-Renewal

`sudo systemctl status certbot.timer`

#### Test renewal process
`sudo certbot renew --dry-run`

You should see this
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/verify_certbot.PNG">
</div>
<br>

#### Update CORS in digital ocean
Update for HTTPS in spaces settings
<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/CORS.PNG">
</div>
<br>


#### Update settings.py
Set `BASE_URL` variable in `settings.py` to your domain name.


## Update nginx config
We need to tell nginx to allow websocket data to move through port 8001. I'm not really sure how to explain this. I don't understand it fully. Similar to how we allow gunicorn to proxy pass nginx.

Navigate to `/etc/nginx/sites-available`

Update `daruapp`
```
server {

    ...
    
    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001;
    }

    ...
}
```

## Update `daphne.service`
Tell daphne how to access our https cert.

Navigate to `/etc/systemd/system`

Update `daphne.service`
```
[Unit]
Description=WebSocket Daphne Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/django/daruapp/src
ExecStart=/home/django/daruapp/venv/bin/python /home/django/daruapp/venv/bin/daphne -e ssl:8001:privateKey=/etc/letsencrypt/live/open-chat-demo.xyz/privkey.pem:certKey=/etc/letsencrypt/live/open-chat-demo.xyz/fullchain.pem daruapp.asgi:application  
Restart=on-failure

[Install]
WantedBy=multi-user.target
```


# Create a superuser
Before you test the server create a superuser.

`su django`

`cd /home/django/daruapp/`

`source venv/bin/activate`

`cd src`

`python manage.py createsuperuser`


# Finishing up
Restart the server and visit your website to try it out. Everything should be working now.

**If you followed my course remember to create a public chat room from the admin with the title "General".**

Thanks for reading and feel free to contribute to this document if you have a better way of explaining things. I am by no means a web expert. 


# FAQ
Here are some things I wish I knew when doing this for the first time.

### If you change a file or pull a code update to the project, do you need to do anything?
Yes.

If you only change code that is *not related to django channels* then you only need to run `service gunicorn restart`.

But if you change any code related to django channels, **then you must also restart the daphne service**: `service daphne restart`.

To be safe, I always just run both. It can't hurt.
```
service gunicorn restart
service daphne restart
```
<br>

### Service Status Errors
Throughout this document we periodically check the status of the services that we set up. Things like:
1. `sudo systemctl status gunicorn`
1. `sudo systemctl status redis`
1. `systemctl status daphne.service`
1. `systemctl status on_boot.service`
1. `sudo systemctl status certbot.timer`

If any of these fail, it's not going to work and you've done something wrong. The most common problem is the directory structure does not match up. For example you might use `/home/django/django_project/src/` instead of `/home/django/daruapp/src/`. You need to look very carefully at your directory structures and make sure the naming is all correct and correlates with the `.service` files you build. 

When you make a change to a `.service` file, **Always run `sudo systemctl daemon-reload`**. Or to be safe, just restart the damn server `sudo shutdown -r now`. Restarting the server is the safe way, but also the slowest way. 


### CORS error in web console
You are getting an error in web console saying: "No 'Access-Control-Allow-Origin' header is present on the requested resource".

Fix this by adding CORS header in spaces settings.
See [This image](https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/CORS.PNG) for the configuration.

# References
1. [https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04)
1. [https://channels.readthedocs.io/en/latest/](https://channels.readthedocs.io/en/latest/)
1. [https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04)
1. [https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django](https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django)
1. [https://stackoverflow.com/questions/61101278/how-to-run-daphne-and-gunicorn-at-the-same-time](https://stackoverflow.com/questions/61101278/how-to-run-daphne-and-gunicorn-at-the-same-time)
1. [https://github.com/conda-forge/pygridgen-feedstock/issues/10](https://github.com/conda-forge/pygridgen-feedstock/issues/10)
1. [https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04)