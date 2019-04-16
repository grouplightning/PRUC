#!/bin/bash
#commands and services that need to be ran as Root on hub startup
#the path to this can be ideally just added to /etc/rc.local
python3 /home/pi/PRUC/battery_backup/BatterySens.py &
