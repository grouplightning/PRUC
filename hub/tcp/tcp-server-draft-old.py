import socket

# TODO: SAVE FOR MAC ADDRESS ISSUE
class SensorServer:
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.address = ('0.0.0.0', 4444)
		self.queue = 1

	def start(self):
		self.socket.bind(self.address)
		self.socket.listen(self.queue)
		print("Listening on {} port {}".format(*self.address))

	def stop(self):
		self.socket.close()

	def get_commands(self, handler):
		while True:
			conn, client_addr = self.socket.accept()
			try:
				print("new connection: ", client_addr)
				while True:
					data = conn.recv(32)
					if data:
						response = handler.command_callback(conn, client_addr, data)
						if response is not None:
							conn.sendall(response)
							conn.close()
							return
					else:
						break
			finally:
				print("connection closed by peer")
				conn.close()


class DummyHandler:

	def command_callback(self, conn, client_addr, data):
		print(str(data))
		return bytes("OK", "utf-8")


cmd_handler = DummyHandler()
serv = SensorServer()
serv.start()
serv.get_commands(cmd_handler)
serv.stop()

