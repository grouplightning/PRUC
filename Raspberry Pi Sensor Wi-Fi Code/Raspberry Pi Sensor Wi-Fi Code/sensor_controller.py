from sensor_server import SensorServer
import os, os.path

class ResponseHandler:
	def __init__(self):
		self.image_length_size = 4
		self.total_images = 0

	def run_command(self, raw_command):
		#prepare arguments of the command in a list for commands to access
		args = raw_command.split()
		arg_count = len(args)-1
		command = args[0]
		#if there is an argument besides the initial command eg: [command, arg, arg2], pop the initial command string off the front: [arg, arg2]
		if arg_count>0:
			args.pop(0)
		#many commands rely on an integer parameter, this prevents errors from occuring
		try:
			iarg=int(args[0])
		except:
			iarg=0


		print("received command: "+ str(raw_command))
		print(args)
		print(arg_count)
		print(iarg)

		if len(command) == 0:
			print("Received command with no length.")
			return

		if command == "totalImages":
			total_images = len([name for name in os.listdir('images') if os.path.isfile("images/"+name)]) #bugfix couunt not getting image count - don't trust stackoverflow!
			self.total_images = total_images
			print(total_images)
			return bytes(str(total_images),'utf-8')
		elif command=="getImages":
			return self.get_n_images(iarg)
		elif command=="Okay":
			self.process_okay(iarg)
			return bytes("Okay, deleted the images.",'utf-8')
		elif command == "ping":
			return self.ping(args[0])
		print(" unknown command: `"+str(command)+"`")

	def ping(self, arg):
		return bytes("pong "+arg, "utf-8")

	def get_n_images(self,n):
		"""Gets N images and returns it to the hub.

		"""
		#n=int(n)
		counter = 0
		combined_data = bytes('', "utf-8")
		retries = 3
		current_images = self.total_images
		while counter < n and retries > 0:
			print("debug: get iteration "+str(counter)+" "+str(retries)+" "+str(current_images))
			try:
				with open(("images/image" + str(current_images) + ".jpg"), "rb") as image:
					data = image.read()
			except:
				print("Error reading image data, trying %d more times" % retries)
				retries -= 1
				if retries == 0:
					self.delete_image(current_image=current_images)
					current_images-=1 # this line was `counter -= 1` which caused an infinite loop, the counter is not incremented because of the 'continue' however current_images was not being decreased with the deletion
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


	def process_okay(self, images_to_delete):
		"""Run after sending images to hub, deletes processed images.

		:param images_to_delete: THE COMMAND STRING, I am splitting the string for the amount
		of pictures to delete.
		"""
		#images_to_delete = int(images_to_delete)
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
#command_handler.run_command('getImages 10')
#command_handler.run_command('ping xyz')
#command_handler.run_command('Okay 5')

server = SensorServer()
server.start()
server.get_commands(command_handler)
server.stop()


