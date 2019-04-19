import socket
import os
import time
import struct

class HubClient:
	def __init__(self):
		self.socket = None
		self.remote_address = None
		self.chunk = 1024
		self.image_length_size = 4
		self.total_images = 0
		self.park_open = 0

	def connect(self, addr, port):
		"""Connects to a remote sensor socket."""
		try:
			self.remote_address = (addr, port)
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect(self.remote_address)
			print("Connecting to {} port {}".format(*self.remote_address))
			return True
		except:
			print("UNABLE TO CONNECT TO SENSOR!!!!")
			return False

	def disconnect(self):
		"""Closes the socket connection"""
		self.socket.close()

	def add_one_total_images(self):
		"""Adds one to the total image variable"""
		self.total_images += 1

	def send_command(self,command, timeout = 0.0):
		"""
		Send a command string, padded to the length required by the Sensor Server buffer.
		:param command: The command string to be sent to the sensor.
		:param timeout: (OPTIONAL) the length of socket timeout for sending the command, in seconds; the timeout is not changed if it is set to 0.
		"""
		try:
			command_bin = bytes(command, "utf-8")
			remaining_bytes = 32 - len(command_bin)
			padding = b'\x20' * remaining_bytes #creating bytes of length 32-N all set to space
			if timeout!=0.0: self.socket.settimeout(timeout)
			self.socket.sendall(command_bin + padding)
			print("Sent command: " + command)
			return True
		except:
			print("Unable to send command %s" % command)
			return False


	def execute_command(self, command):
		"""Sends a command to a sensor and receives the sensor's response

		:param command: The command string to be sent to the sensor.
		:return: The data response from the sensor
		"""
		data = bytes('', "utf-8")

		if not self.send_command(command,0.25): return False

		while True:
			try:
				response = self.socket.recv(self.chunk)
			except:
				response = bytes('',"utf-8")
			data += response
			if len(response) == 0:
				break
		return data

	def execute_command_images(self, number_of_images):
		"""Requests a number of images from the sensor and save those images.

		This function is made specifically for receiving and decoding multiple images.
		:param number_of_images: This is the number of images we want save
		:return: Bool of whether or not the function succeeded.
		"""
		command = "getImages "+str(number_of_images)
		if not self.send_command(command,1): return False

		while number_of_images > 0:
			try:
				response = self.socket.recv(self.image_length_size)
			except:
				print("Unable to get image length.")
				return False
			image_len = int.from_bytes(response,'big')
			print(" image len = "+str(response)+" -> "+str(image_len))
			image_data = bytes('',"utf-8")
			while True:
				try:
					data = self.socket.recv(image_len)
				except:
					data = bytes('',"utf-8")
				image_data += data
				if len(data)==0:
					print("Done reading "+str(len(data)))
					break
				image_len -= len(data)
				print(" read "+str(len(data)))

			if not image_len == 0:
				print("Error reading in image.")
				return False

			print(" received image len = "+ str(len(image_data)))
			image_name = "image" + str(self.total_images + 1) + ".jpg"

			try:
				image = open(os.path.join("images",image_name), "wb")
				image.write(image_data)
			except:
				print("Error saving image data")
				return False

			print("Saved an image named: [" + image_name + "] to the hub.")

			self.total_images += 1
			number_of_images -= 1

		return True

	@staticmethod
	def bytes_to_mtime(bytes):
		"""
		Converts a portable byte array into a modification timestamp (seconds since EPOCH).
		This array will have length 4 by default.  NOTE: may require updating to 8 bytes before 2038.
		:param bytes: the timestamp to convert, represented in bytes
		:return: the timestamp in seconds
		"""
		values = struct.unpack(">i", bytes)
		return int(values[0])

	def get_image_amount(self):
		"""Gets the number of images that the sensor needs to send to the hub.

		:return: Integer representing the amount of pictures the sensor has to send.
		"""
		amountb = self.execute_command(command="totalImages")
		amountstr = amountb.decode('utf-8')
		print(str(amountb)+ " -> "+str(amountstr))
		try:
			amount = int(amountstr)
			print(str(amountstr) + " -> "+str(amount))
		except Exception as e:
			print("Cant convert response. "+str(e))
			amount=0
		return amount

	def get_n_images(self, number_of_images):
		"""Gets and saves N images from a sensor.

		:return: Bool of whether or not we got 5 images from the sensor.
		"""
		retries = 3
		success = False
		while retries > 0 and not success:
			success = self.execute_command_images(number_of_images)
		return success

	def get_sensor_timestamp(self):
		ts = self.execute_command("time "+str(time.time()))
		ts = ts.decode('utf-8')
		return float(ts)

	def transfer_n_images(self, number_of_images):
		if not self.get_n_images(number_of_images): return False
		self.send_okay_signal(number_images_to_delete=number_of_images)
		return True


	def send_okay_signal(self, number_images_to_delete):
		"""This sends an okay to the sensor with the number of images to delete.

		:param number_images_to_delete: Number of images that the sensor will then delete.
		"""
		self.execute_command(command=("Okay " + str(number_images_to_delete)))

	def send_cleanup_signal(self):
		"""This sends a final cleanup command to the sensor.

		Deletes any excess images, resets time clock, any other cleanup tasks
		"""
		self.execute_command(command="Cleanup")


	def get_sensor_images(self):
		"""Gets and saves all images currently stored on the sensor.

		:return: Bool of whether or not we got all sensor images.
		"""
		# update this
		total_images = self.get_image_amount()
		print("total images =  "+str(total_images))
		if total_images==0:
			print("No images available or error")
			return False

		number_of_ten_loops = int(total_images / 10)
		images_remaining = total_images - (number_of_ten_loops * 10)

		number_of_five_loops = int(images_remaining / 5)
		images_remaining = images_remaining - (number_of_five_loops * 5)

		number_of_one_loops = images_remaining

		for number in range(0, number_of_ten_loops):
			if not self.transfer_n_images(10): return False

		for number in range(0, number_of_five_loops):
			if not self.transfer_n_images(5): return False

		for number in range(0, number_of_one_loops):
			if not self.transfer_n_images(1): return False

		self.send_cleanup_signal()

		print("All images saved successfully.")
		return True

	def delete_all_images(self):
		"""Deletes all saved images on the hub."""
		while self.total_images > 0:
			image_name = "image" + str(self.total_images + 1) + ".jpg"
			os.remove(image_name)
			self.total_images -= 1
		print("All images deleted.")

	# TODO: What other commands do we want to send
	# Implement function that calls detection algorithm (see scheduler)


	def hub_main_cycle(self):
		""" The is the main sequence that the hub will repeatedly loop through."""
		# TODO: Look into how sensor IP's are set; we want them to be static
		# TODO: Implement multiple sensor capabilities
		# Check time on loop to know when to request images. (handled by scheduler)
		# TODO: Implement a stored variable with all sensor's network information (add to DB during pairing, read by scheduler)
		# Handle exceptions for loss of signal (should be more or less handled)



#--------------------------------------------------------------------------------------------------


"""
client = HubClient()
#client.connect("10.3.141.54", 1234)
client.connect("127.0.0.1", 1234)
client.get_sensor_images()
client.disconnect()

"""
