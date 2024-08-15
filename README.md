# basement-calling
Simple basement alarm system for Raspberry PI (5) alarming via SIP calls. Detection based on a simple door sensor.

# Hardware

## Required
* Raspi 5 - similar "Credit card computers" should work too
* (Magnet Switch) Contact closing when door is closed - Connected between Ground and the selected GPIO set to pull up

## Recommended
* Wired Connection Between Raspi and the Fritz Box (or a similar SIP server) - Powerline LAN worked for me

# Setup
## Raspbian convenience
* Enable SSH + create user already during card flashing.
* I used Raspbian Bookworm (May 2024).

## System dependencies
### Pip
`sudo apt-get install python3-pip`

### Updated GPIO for Raspi 5
Incompatible Version is shipped with Raspbian (as of May 2024)
`sudo apt remove python3-rpi.gpio`
`sudo apt install python3-rpi-lgpio`

### SIP client
`sudo apt-get install baresip`

#### Configuration
in `~/.baresip/accounts`

## Python dependencies
TODO: create requirements.txt
* baresipy (Python)
    * Pip may require some special flags to overwrite system pkgs, which didn`t break anything for me
    * `pip install --break-system-packages baresipy`

## Copy main.py somewhere reasonnable
E.g. your home.

## Insert your sip user/password into the respective lines in main.py
`user=""`
`pswd=""`

## Make it executeable
`sudo chmod +x main.py`

## crontab for autostart (only if you dont like/have systemd)
Edit crontab
`crontab -e`
Add at the end
`@reboot python3 /home/USERNAME/main.py`

## systemd for autostart
Change `User=` to your username set up on the raspi. Also change `WorkingDirectory=` to your users home.
Change the path in ExecStart to `/home/USER/main.py`.

Copy `basement_calling.service` to `/etc/systemd/system/`. (Or create the file anew using `sudo nano /etc/systemd/system/basement_calling.service`)

Change the file permissions `sudo chmod 644 /etc/systemd/system/basement_calling.service`

Reload systemd to index the new service `sudo systemctl daemon-reload`

Enable the new service on startup `sudo systemctl enable basement_calling.service`

### Get logs
`sudo journalctl -u basement_calling.service`

# Dealing with the Raspi remotely
## Reboot
`sudo shutdown -r now`
## Check if our app is running
`ps -ef | grep python`

