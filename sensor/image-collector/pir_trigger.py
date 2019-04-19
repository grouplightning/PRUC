from gpiozero import MotionSensor
from picamera import PiCamera
import time

pir = MotionSensor(4)
camera = PiCamera()
#camera.capture("image.jpg")
#camera.close()
#exit()


def wait_capture(image_path):
	pir.wait_for_motion()
	camera.capture(image_path)
	pir.wait_for_no_motion()

#camera.close()
