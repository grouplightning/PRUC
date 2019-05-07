import time
import os
import configparser
from tcp.client import HubClient
from db.db import DB
from image_detection.deep_od_lib import *
from datetime import datetime
#from deep_od_lib import *

db = DB()
client = HubClient()
config = configparser.ConfigParser()
path = os.path.abspath(os.path.dirname(__file__)) #get current path from python script name
os.chdir(path) # set current working directory (path to look in) to same directory as script

ran = False


detections = {"person": 0, "horse": 0, "dog": 0, "car": 0, "bicycle": 0}
def image_detect_collect_counts(object_name,confidence):
	if object_name in detections.keys():
		detections[object_name] += 1

def get_images(sensor_id,ip):
	global detections
	if client.connect(ip, 1234):
		db.updateSensorSeen(sensor_id)
		client.get_sensor_images_discrete()
		client.disconnect()
		image_names = [name for name in os.listdir('images') if os.path.isfile("images/" + name)]
		for image_name in image_names:
			detections = {"person": 0, "horse": 0, "dog": 0, "car": 0, "bicycle": 0}
			try:
				if detect_image(os.path.join("images",image_name), 0.75, image_detect_collect_counts) is None:
					print(" cv2 imread failed")
			except Exception as e:
				print("Error in image detection")
				print(e)
			timestamp_raw = client.get_timestamp_from_image_name(image_name)
			if timestamp_raw is None:
				print("can't find timestamp for image, skipping")
				continue
			timestamp = datetime.utcfromtimestamp(timestamp_raw).strftime("%Y-%m-%d %H:00:00")
			if not db.doesCountsExist(sensor_id,timestamp):
				db.createCountsStub(sensor_id,timestamp)
			db.addCounts(sensor_id, timestamp, detections['person'], detections['horse'], detections['dog'], detections['car'], detections['bicycle'], 0)
		client.delete_all_images()
	else:
		db.recordSensorError(sensor_id)

def get_images_all_sensors():
	"""Requests the sensor id and ip from the database"""
	results = db.query("SELECT id,ip FROM sensors")
	print("Getting images from sensors\n")
	sensors = []
	for row in results:
		id,ip=row
		sensors.append((id,ip))
	for row in sensors:
		sensor_id = row[0]
		ip = row[1]
		print("Getting images from sensor %s\n" % sensor_id)
		try:
			get_images(sensor_id,ip)
		except Exception as e:
			pass


while True:
	print("start")
	t = time.localtime()
	h = t.tm_hour
	m = t.tm_min

	config.read(os.path.join(path,"scheduler.ini")) # refresh config file entries
	test_h = int(config['scheduler']['hour'])
	test_m = int(config['scheduler']['minute'])

	print("%d %d =? %d %d" % (h,m,test_h,test_m))

#	if h==test_h and m == test_m and not ran:
	if m%2==0 and not ran:
		ran=True
		get_images_all_sensors()
#	if (h!=test_h or m != test_m) and ran:
	if m%2!=0 and ran:
		ran=False




	print("sleep")

	time.sleep(1)
	print("end")
