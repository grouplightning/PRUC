from sensor_server import SensorServer
import os, os.path

class ResponseHandler:
	def __init__(self):
		self.image_length_size = 4
		self.total_images = 0

	def run_command(self, command):
		print("received command: "+ str(command))
		if len(command) == 0:
			print("Received command with no length.")
			return

		if command == "totalImages":
			total_images = len([name for name in os.listdir('images') if os.path.isfile(name)])
			self.total_images = total_images
			return bytes(str(total_images),'utf-8')
		elif command == "getOneImage":
			return self.get_one_image()
		elif command == "getFiveImages":
			return self.get_five_images()
		elif command == "getTenImages":
			return self.get_ten_images()
		elif "Okay" in command:
			self.process_okay(command)
			return bytes("Okay, deleted the images.",'utf-8')
		elif command == "ping":
			return self.ping(command)
		print(" unknown command: `"+str(command)+"`")

	def ping(self, arg):
		return bytes("pong "+arg, "utf-8")

	def get_one_image(self):
		"""Gets one image and returns it to the hub."""
		retries = 3
		current_images = self.total_images
		image_name = "images/image" + str(current_images) + ".jpg"
		while retries > 0:
			try:
				with open(image_name, "rb") as image:
					data = image.read()
					# TODO: Implement function to delete image
					# TODO: Update master variable
				return data
			except:
				print("Error reading image data, trying %d more times" % retries)
				retries -= 1
				if retries == 0:
					self.delete_image(current_image=current_images)
					retries = 3
					print("%s was unable to be sent to the hub. DELETING IMAGE." % image_name)

	def get_five_images(self):
		"""Gets five images and returns it to the hub.

		"""
		counter = 0
		combined_data = bytes('', "utf-8")
		retries = 3
		current_images = self.total_images
		while counter < 5 and retries > 0:
			try:
				with open(("images/image" + str(current_images) + ".jpg"), "rb") as image:
					data = image.read()
			except:
				print("Error reading image data, trying %d more times" % retries)
				retries -= 1
				if retries == 0:
					self.delete_image(current_image=current_images)
					counter -= 1
					retries = 3
					print("%s was unable to be sent to the hub. DELETING IMAGE." %
						  ("image" + str(current_images) + ".jpg"))
				continue

			current_images -= 1
			retries = 3
			counter += 1
			combined_data += int.to_bytes(len(data),4, byteorder='big') + data
		# TODO: When will we update the master variable and delete the images sent?
		# TODO: How will we get the timestamp information?
		return combined_data

	def get_ten_images(self):
		"""Gets five images and returns it to the hub.

		"""
		counter = 0
		combined_data = bytes('', "utf-8")
		retries = 3
		current_images = self.total_images
		while counter < 10 and retries > 0:
			try:
				with open(("images/image" + str(current_images) + ".jpg"), "rb") as image:
					data = image.read()
			except:
				print("Error reading image data, trying %d more times" % retries)
				retries -= 1
				if retries == 0:
					self.delete_image(current_image=current_images)
					counter -= 1
					retries = 3
					print("%s was unable to be sent to the hub. DELETING IMAGE." %
						  ("image" + str(current_images) + ".jpg"))
				continue

			current_images -= 1
			retries = 3
			counter += 1
			combined_data_lenb = int.to_bytes(len(data),4,byteorder='big')
			combined_data += combined_data_lenb + data
		print("sending image data len = "+str(len(combined_data)))
		print("   "+ str(combined_data_lenb))
		# When will we update the master variable and delete the images sent?
		# TODO: How will we get the timestamp information?
		return combined_data

	def process_okay(self, images_to_delete):
		"""Run after sending images to hub, deletes processed images.

		:param images_to_delete: THE COMMAND STRING, I am splitting the string for the amount
		of pictures to delete.
		"""
		images_to_delete = int(images_to_delete.split()[1])
		print("Obtained okay message from hub. Deleting %s images." % images_to_delete)
		for _ in range(0, images_to_delete):
			self.delete_image(current_image=self.total_images)

	def delete_image(self, current_image):
		"""Deletes a specified images.

		:param current_image: The number of the image to delete.
		:return: None
		"""
		image_name = ("images/image" + str(current_image) + ".jpg")
		try:
			os.remove(image_name)
			print("Deleted image %s." % image_name)
			self.total_images -= 1
		except:
			print("Unable to delete image %s. Does it exist?" % image_name)





command_handler = ResponseHandler()
command_handler.run_command('Okay 1')
"""
server = SensorServer()
server.start()
server.get_commands(command_handler)
server.stop()
"""

