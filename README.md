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

## Python dependencies
TODO: create requirements.txt
* baresipy (Python)
    * Pip may require some special flags to overwrite system pkgs, which didn`t break anything for me
    * `pip install --break-system-packages baresipy`

## Copy main.py somewhere reasonnable
E.g. your home.

## Make it executeable
`sudo chmod +x main.py`

## crontab for autostart
Edit crontab
`crontab -e`
Add at the end
`@reboot python3 /home/USERNAME/main.py`

# Dealing with the Raspi remotely
## Reboot
`sudo shutdown -r now`
## Check if our app is running
`ps -ef | grep python`

