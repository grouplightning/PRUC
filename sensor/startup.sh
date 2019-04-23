#python3 /home/pi/PRUC/sensor_controller.py &

/bin/su pi -c "/usr/bin/screen -dmS controller bash -c 'cd /home/pi/PRUC/sensor; python3 /home/pi/PRUC/sensor/sensor_controller.py; exec bash'"


#python3 /home/pi/PRUC/TBA/image_collection_script &
