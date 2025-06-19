import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

print("Client started. Connecting to server...")


def build_and_send_message(conn: socket.socket, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    message = chatlib.build_message(code, data)
    print(f"Sending message: {message}")
    conn.sendall(message.encode('utf-8'))


def recv_message_and_parse(conn: socket.socket):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..
    try:
        conn.settimeout(1)  # Set a timeout for receiving data
        data = ""
        while True:
            new_data = conn.recv(1024).decode('utf-8')
            print(f"Received data: {new_data}")
            if len(new_data) == 0:
                break
            data += new_data

    except Exception as e:
        if not isinstance(e, socket.timeout):
            return None, None
    finally:
        cmd, data = chatlib.parse_message(data)
    return cmd, data


def connect():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((SERVER_IP, SERVER_PORT))

    except socket.error as e:
        error_and_exit(
            f"Could not connect to server at {SERVER_IP}:{SERVER_PORT}. Error: {e}")
    finally:
        return soc


def error_and_exit(error_msg):
    """Prints an error message and exits the program."""
    raise Exception(error_msg)


def login(conn):
    if not conn:
        error_and_exit("Connection is not established. Cannot login.")
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        build_and_send_message(
            conn, chatlib.PROTOCOL_CLIENT["login_msg"], f"{username}#{password}")
        cmd, data = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Login successful!")
            return
        elif cmd == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
            print("Login failed. Please try again.")
        else:
            error_and_exit(f"Unexpected response from server: {cmd}, {data}")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def main():
    socket_conn = connect()
    login(socket_conn)
    logout(socket_conn)
    socket_conn.close()


if __name__ == '__main__':
    main()
