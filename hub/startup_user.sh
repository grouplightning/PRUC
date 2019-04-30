#!/bin/bash
#commands and services that need to be ran as the user after hub startup
#the path to this script must be added to configuration that will run it *after* the desktop environment is loaded
#for example, for LXDE, you would add it to /etc/xdg/lxsession/LXDE/autostart
screen -dmS scheduler bash -c 'cd /home/pi/PRUC/hub/; python3 /home/pi/PRUC/hub/scheduler.py'

cd /home/pi/PRUC/hub
python3 /home/pi/PRUC/hub/ui.py &
