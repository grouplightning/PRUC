import os
from image_capture.pir_trigger import *
import time
from threading import Thread,Event



def get_image_list():
	"""
	Retrieves the current list of images in the images/ directory
	:return: list of image filenames, relative to the images/ directory
	"""
	return [name for name in os.listdir('images') if
			os.path.isfile("images/" + name)]  # bugfix couunt not getting image count - don't trust stackoverflow!

def wait_for_image():
	# test
	print("running capture")
	# camera.capture("image"+self.images_num+".jpg")
	pir_wait()

	image_list = get_image_list()
	print(image_list)
	image_num = len(get_image_list()) + 1
	print(image_num)
	pir_capture_wait("images/image" + str(image_num) + ".jpg")

class ImageThread(Thread):
	def __init__(self,event):
		Thread.__init__(self)
		self.stopped = event

	def run(self):
		pir_start()
		while True:
			if not self.stopped.is_set():
				pir_wait()
			if not self.stopped.is_set():
				pir_capture()
			if not self.stopped.is_set():
				pir_waitafter()
			time.sleep(0.05)

		print("closing pir")
		pir_close()
		print("closed pir")

	# my_gui.images_num += 1;
	#        detect_image("image.jpg",0.7,gui_callback)

#while True:
#	wait_for_image()
#	time.sleep(0.05)