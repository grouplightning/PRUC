import uuid

@staticmethod
def get_own_mac():  # getting the remote MAC address requires root, difficult.
	return uuid.getnode()  # get a UUID based on the MAC.  makes several attempts
# TODO: can be random if fails (unable to find the MAC), so we should test this


