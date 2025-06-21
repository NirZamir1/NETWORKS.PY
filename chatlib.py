from socket import socket, timeout
# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"error_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	# Implement code ...
	command = f"{cmd}" + " " * (CMD_FIELD_LENGTH - len(cmd))
	length = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
	return f"{command}{DELIMITER}{length}{DELIMITER}{data}" if len(data) <= MAX_DATA_LENGTH and len(cmd) <= CMD_FIELD_LENGTH else None


def parse_message(data: str):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	arr = data.split(DELIMITER)

	if len(arr) != 3:
		return None, None
	[cmd, length_str, msg] = arr
	if(len(cmd) != CMD_FIELD_LENGTH or len(length_str) != LENGTH_FIELD_LENGTH or not length_str.isdigit() or len(msg) !=int(length_str)):
		return None, None
	for i in range(0, LENGTH_FIELD_LENGTH):
		if ord(length_str[i]) not in range(48,58):
			return None, None
	return cmd.strip(), msg

	
def split_data(msg: str, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	# Implement code ...
	data =msg.split("#")
	if len(data) != expected_fields:
		return [None]
	return data


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	return "#".join(msg_fields)

def recv_message_and_parse(conn: socket):
	"""
	Receives a new message from the given socket,
	then parses the message using chatlib.
	Parameters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If an error occurred, will return None, None
	"""
	data = conn.recv(1042).decode('utf-8')
	cmd, data = parse_message(data)
	return cmd, data