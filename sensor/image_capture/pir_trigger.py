from gpiozero import MotionSensor
from picamera import PiCamera
import time

pir = MotionSensor(4)
camera = PiCamera()
#camera.capture("image.jpg")
#camera.close()
#exit()

def pir_wait():
	pir.wait_for_motion()


def pir_capture_wait(image_path):
	camera.capture(image_path)
	pir.wait_for_no_motion()

#camera.close()
