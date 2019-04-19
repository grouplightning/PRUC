from tcp.server import HubServer

class PairHandler:

	def command_callback(self, conn, client_addr, data):
		print(str(data))
		return bytes("OK", "utf-8")

#TODO: add pair command handler

pairing_server = HubServer()
handler = PairHandler()
pairing_server.start()
pairing_server.get_commands(handler)
pairing_server.stop()
