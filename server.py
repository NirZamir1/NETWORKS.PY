##############################################################################
# server.py
##############################################################################

import socket
import chatlib
from select import select

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
client_sockets = []
messages = []  # a list of messages to be sent to clients - will be used later
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS


def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"], "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test":	{"password": "test", "score": 0, "questions_asked": []},
        "yossi":	{"password": "123", "score": 50, "questions_asked": []},
        "master":	{"password": "master", "score": 200, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    print(f"[SERVER] Listening on {SERVER_IP}:{SERVER_PORT}...")
    return sock


def send_error(conn: socket.socket, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    add_message_to_send(
        conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)
# MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    # Implement this in later chapters


def handle_logout_message(conn: socket.socket):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """

    global logged_users
    hostname = conn.getpeername()
    user = logged_users.pop(hostname)
    conn.close()
    client_sockets.remove(conn)
    print(
        f"[SERVER] Client {hostname} User {user} logged out and connection closed.")


def add_message_to_send(conn, cmd, data):
    messages.append(
        {"sock": conn, "cmd": cmd, "msg": data})


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later

    [username, password] = chatlib.split_data(data, 2)

    if username is None or password is None:
        send_error(conn, "Invalid login data format.")
        return

    if username not in users.keys():
        send_error(conn, "Username does not exist.")
        return

    if users[username]["password"] != password:
        send_error(conn, "Incorrect password.")
        return

    hostname = conn.getpeername()
    logged_users[hostname] = username
    add_message_to_send(
        conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")

    print(f"[SERVER] User {username} logged in")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later
    host = conn.getpeername()
    if host not in logged_users:
        if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
            handle_login_message(conn, data)
    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"] or (cmd is None and data is None):
        handle_logout_message(conn)
    # Implement code ...


def accept_connection(server_socket):
    try:
        conn, addr = server_socket.accept()
        print(f"[SERVER] New connection from {addr}")
        return conn
    except socket.timeout:
        return None


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    server_socket = setup_socket()
    users = load_user_database()
    while True:
        read_list, write_list, exception_list = select(
            [server_socket] + client_sockets, client_sockets, [])
        for sock in read_list:
            if sock is server_socket:
                conn = accept_connection(server_socket)
                if conn:
                    client_sockets.append(conn)
            else:
                cmd, data = chatlib.recv_message_and_parse(sock)
                handle_client_message(sock, cmd, data)

        for message in messages:
            conn = message["sock"]
            cmd = message["cmd"]
            data = message["msg"]
            if conn in write_list:
                chatlib.build_and_send_message(conn, cmd, data)
                messages.remove(message)


if __name__ == '__main__':
    main()
