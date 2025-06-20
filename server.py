##############################################################################
# server.py
##############################################################################

import socket
import chatlib

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    # copy from client
    message = chatlib.build_message(code, msg)
    conn.sendall(message.encode())
    print("[SERVER] ", message)	  # Debug print


def recv_message_and_parse(conn):
    # copy from client
    data = ""
    while True:
        try:
            new_data = conn.recv(1024).decode('utf-8')
            if len(new_data) == 0:
                break
            data += new_data
        except Exception as e:
            if not isinstance(e, socket.timeout):
                send_error(conn, "Error receiving data from client.")
                return None, None
            else:
                break
    cmd, data = chatlib.parse_message(data)
    return cmd, data


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
    sock.settimeout(1)

    return sock


def send_error(conn: socket.socket, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["error_msg"], f"{ERROR_MSG} {error_msg}")

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
    hostname = conn.getpeername()[0]
    logged_users.pop(hostname)
    conn.close()
    print(f"[SERVER] Client {hostname} logged out and connection closed.")


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later

    username, password = chatlib.split_data(data, 2)

    if username is None or password is None:
        send_error(conn, "Invalid login data format.")
        return

    if username not in users:
        send_error(conn, "Username does not exist.")
        return

    if users[username]["password"] != password:
        send_error(conn, "Incorrect password.")
        return

    hostname = conn.getpeername()[0]
    logged_users[hostname] = username
    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
    print(f"[SERVER] User {username} logged in")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later

    # Implement code ...


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")

    # Implement code ...


if __name__ == '__main__':
    main()
