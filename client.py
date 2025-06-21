import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

print("Client started. Connecting to server...")


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
        chatlib.build_and_send_message(
            conn, chatlib.PROTOCOL_CLIENT["login_msg"], chatlib.join_data([username, password]))

        cmd, data = chatlib.recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Login successful!")
            return
        elif cmd == chatlib.PROTOCOL_SERVER["error_msg"]:
            print(f"{cmd}")
        else:
            error_and_exit(f"Unexpected response from server: {cmd}, {data}")


def logout(conn):
    chatlib.build_and_send_message(
        conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def main():
    socket_conn = connect()
    login(socket_conn)
    logout(socket_conn)
    socket_conn.close()


if __name__ == '__main__':
    main()
