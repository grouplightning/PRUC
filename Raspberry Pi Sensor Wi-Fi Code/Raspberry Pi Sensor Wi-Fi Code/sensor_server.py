import socket
import time


class SensorServer:
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.address = ('0.0.0.0', 1234)
		self.queue = 1

	def start(self):
		""" Listens for connection from hub."""
		self.socket.bind(self.address)
		self.socket.listen(self.queue)
		print("Listening on {} port {}".format(*self.address))

	def stop(self):
		"""Closes connection with hub."""
		self.socket.close()

	def get_commands(self, handler):
		while True:
			conn, client_addr = self.socket.accept()
			try:
				print("New connection:: ", client_addr)
				while True:
					# TODO Is this enough bytes?
					try:
						data = conn.recv(32)
					except:
						conn.close()
						break
					if data:
						command = data.decode('utf-8')
						print("forwarding command to handler: "+command)
						response = handler.run_command(command)
						if response is not None:
							try:
								conn.sendall(response)
							except:
								print("The sensor response failed to send. Closing connection.")
								conn.close()
					else:
						print("No command received.")
						break
					time.sleep(0.25)
			finally:
				print("Connection to {} closed.".format(client_addr))
				conn.close()


class DummyHandler:

	def command_callback(self, conn, client_addr, data):
		print(str(data))
		return bytes("OK", "utf-8")


#response_handler = ResponseHandler()
#serv = SensorServer()
#serv.start()
#serv.get_commands(cmd_handler)
#serv.stop()

