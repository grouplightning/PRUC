from gpiozero import MotionSensor
from picamera import PiCamera
import time


def pir_start():
	global pir
	global camera
	pir = MotionSensor(4)
	camera = PiCamera()
	#camera.capture("image.jpg")
	#camera.close()
	#exit()

def pir_wait():
	global pir
	pir.wait_for_motion()

def pir_capture(image_path):
	global camera
	camera.capture(image_path)

def pir_waitafter():
	global pir
	pir.wait_for_no_motion()

def pir_close():
	global pir
	global camera
	camera.close()
	pir.close()
	pir = None
	camera = None

