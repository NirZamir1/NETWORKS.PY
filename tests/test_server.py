# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: c:\users\yahel\desktop\server_test.py
# Bytecode version: 3.8.0rc1+ (3413)
# Source timestamp: 2021-01-05 10:42:50 UTC (1609843370)

import select
import random
import socket
global questions  # inserted
global users  # inserted
global messages_to_send  # inserted
global logged_users  # inserted
CMD_FIELD_LENGTH = 16
LENGTH_FIELD_LENGTH = 4
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH
DELIMITER = '|'
DATA_DELIMITER = '#'


PROTOCOL_CLIENT = {'login_msg': 'LOGIN', 'logout_msg': 'LOGOUT', 'getscore_msg': 'MY_SCORE',
                   'getlogged_msg': 'HIGHSCORE', 'gethighscore_msg': 'GET_QUESTION', 'getquestion_msg': 'SEND_ANSWER'}
PROTOCOL_SERVER = {'login_ok_msg': 'LOGIN_OK', 'login_failed_msg': 'ERROR', 'yourscore_msg': 'YOUR_SCORE', 'highscore_msg': 'ALL_SCORE', 'logged_msg': 'LOGGED_ANSWER',
                   'correct_msg': 'CORRECT_ANSWER', 'wrong_msg': 'WRONG_ANSWER', 'question_msg': 'YOUR_QUESTION', 'error_msg': 'ERROR', 'noquestions_msg': 'NO_QUESTIONS'}
ERROR_RETURN = None


def build_message(cmd, data):
    """\n\tGets command name (str) and data field (str) and creates a valid protocol message\n\tReturns: str, or None if error occured\n\t"""  # inserted
    data_length = len(data)
    cmd_length = len(cmd)
    if data_length > MAX_DATA_LENGTH:
        return ERROR_RETURN
    if cmd_length > CMD_FIELD_LENGTH:
        return ERROR_RETURN
    padded_cmd = cmd.strip().ljust(CMD_FIELD_LENGTH)
    padded_length = str(data_length).zfill(LENGTH_FIELD_LENGTH)
    full_msg = f'{padded_cmd}{DELIMITER}{padded_length}{DELIMITER}{data}'
    return full_msg


def parse_message(full_msg):
    """\n\tParses protocol message and returns command name and data field\n\tReturns: cmd (str), data (str). If some error occured, returns None, None\n\t"""  # inserted
    if len(full_msg) < CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1:
        return (ERROR_RETURN, ERROR_RETURN)
    cmd_str = full_msg[0:CMD_FIELD_LENGTH]
    length = full_msg[CMD_FIELD_LENGTH +
                      1:CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH]
    if full_msg[CMD_FIELD_LENGTH] != DELIMITER or full_msg[CMD_FIELD_LENGTH + LENGTH_FIELD_LENGTH + 1] != DELIMITER:
        return (ERROR_RETURN, ERROR_RETURN)
    if not length.strip().isdigit():
        return (ERROR_RETURN, ERROR_RETURN)
    length = int(length)
    data_str = full_msg[MSG_HEADER_LENGTH:MSG_HEADER_LENGTH + length]
    if not len(data_str) == length:
        return (ERROR_RETURN, ERROR_RETURN)
    return (cmd_str.strip(), data_str)


def split_data(msg, expected_fields):
    """\n\tHelper method. gets a string and number of expected fields in it. Splits the string \n\tusing protocol\'s data field delimiter (|#) and validates that there are correct number of fields.\n\tReturns: list of fields if all ok. If some error occured, returns None\n\t"""  # inserted
    splitted = msg.split(DATA_DELIMITER)
    if len(splitted) == expected_fields:
        return splitted
    return None


def join_data(msg_fields):
    """\n\tHelper method. Gets a list, joins all of it\'s fields to one string divided by the data delimiter. \n\tReturns: string that looks like cell1#cell2#cell3\n\t"""  # inserted
    return DATA_DELIMITER.join(msg_fields)


users = {'nir': 'nir123'}
questions = {}
logged_users = {}
messages_to_send = []
ERROR_MSG = 'Error! '
SERVER_PORT = 5678
CORRECT_ANSWER_POINTS = 5
WRONG_ANSWER_POINTS = 0


def build_and_send_message(conn, cmd, data):
    """\n    Builds a new message using chatlib, wanted command and message. \n    Prints debug info, then sends it to the given socket.\n    Paramaters: conn (socket object), cmd (str), data (str)\n    Returns: Nothing\n    """  # inserted
    full_msg = build_message(cmd, data)
    host = conn.getpeername()
    print('[SERVER] ', host, 'msg: ', full_msg)
    messages_to_send.append((conn, full_msg))


def recv_message_and_parse(conn):
    """\n    Recieves a new message from given socket,\n    then parses the message using \n    Paramaters: conn (socket object)\n    Returns: cmd (str) and data (str) of the received message. \n    If error occured, will return None, None\n    """  # inserted
    full_msg = conn.recv(MAX_MSG_LENGTH).decode()
    host = conn.getpeername()
    print('[CLIENT] ', host, 'msg: ', full_msg)
    cmd, data = parse_message(full_msg)
    return (cmd, data)


def load_questions():
    """\n    Loads questions bank from file  ## FILE SUPPORT TO BE ADDED LATER\n    Recieves: -\n    Returns: questions dictionary\n    """  # inserted
    questions = {2313: {'question': 'How much is 2+2', 'answers': ['3', '4', '2', '1'], 'correct': 2}, 4122: {
        'question': 'What is the capital of France?', 'answers': ['Lion', 'Marseille', 'Paris', 'Montpellier'], 'correct': 3}}
    return questions


def load_user_database():
    """\n    Loads users list from file  ## FILE SUPPORT TO BE ADDED LATER\n    Recieves: -\n    Returns: user dictionary\n    """  # inserted
    users = {'test': {'password': 'test', 'score': 0, 'questions_asked': []}, 'abc': {'password': '123',
                                                                                      'score': 50, 'questions_asked': []}, 'master': {'password': 'master', 'score': 200, 'questions_asked': [], }}
    return users


def setup_socket():
    """\n    Creates new listening socket and returns it\n    Recieves: -\n    Returns: the socket object\n    """  # inserted
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', SERVER_PORT)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(1)
    return sock


def send_error(conn, error_msg):
    """\n    Send error message with given message\n    Recieves: socket, message error string from called function\n    Returns: None\n    """  # inserted
    build_and_send_message(
        conn, PROTOCOL_SERVER['error_msg'], ERROR_MSG + error_msg)


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print('\t', c.getpeername())


def create_random_question():
    """\n    Returns a string representing a YOUR_QUESTION command, using random picked question\n    Example: id|question|answer1|answer2|answer3|answer4\n    """  # inserted
    all_questions = list(questions.keys())
    rand_question_id = random.choice(all_questions)
    chosen_question = questions[rand_question_id]
    question_text, answers = (
        chosen_question['question'], chosen_question['answers'])
    q_string = join_data([str(rand_question_id), question_text,
                         answers[0], answers[1], answers[2], answers[3]])
    return q_string


def create_high_scores():
    data = ''
    users_and_scores = []
    for user in users.keys():
        users_and_scores.append((user, users[user]['score']))
    users_and_scores.sort(key=lambda x: x[1], reverse=True)
    for user, score in users_and_scores:
        data += '%s: %d\n' % (user, score)
    return data


def handle_question_message(conn):
    """\n    Sends to the socket QUESTION message with new question generated by create_random_question\n    Recieves: socket \n    Returns: None (sends answer to client)\n    """  # inserted
    question_str = create_random_question()
    build_and_send_message(conn, PROTOCOL_SERVER['question_msg'], question_str)


def handle_answer_message(conn, username, data):
    """\n    Check is user answer is correct, adjust user\'s score and responds with feedback\n    Recieves: socket, username and message data\n    Returns: None\n    """  # inserted
    splitted = split_data(data, 2)
    if not splitted:
        return
    id, answer = (int(splitted[0]), int(splitted[1]))
    answer_is_correct = questions[id]['correct'] == answer
    if answer_is_correct:
        users[username]['score'] += CORRECT_ANSWER_POINTS
        build_and_send_message(conn, PROTOCOL_SERVER['correct_msg'], '')
    else:  # inserted
        users[username]['score'] += WRONG_ANSWER_POINTS
        build_and_send_message(
            conn, PROTOCOL_SERVER['wrong_msg'], str(questions[id]['correct']))


def handle_getscore_message(conn, username):
    """\n    Sends to the socket YOURSCORE message with the user\'s score.\n    Recieves: socket and username (str)\n    Returns: None (sends answer to client)\n    """  # inserted
    score = users[username]['score']
    build_and_send_message(conn, PROTOCOL_SERVER['yourscore_msg'], str(score))


def handle_highscore_message(conn):
    """\n    Sends to the socket HIGHSCORE message.\n    Recieves: socket\n    Returns: None (sends answer to client)\n    """  # inserted
    highscore_str = create_high_scores()
    build_and_send_message(
        conn, PROTOCOL_SERVER['highscore_msg'], highscore_str)


def handle_logged_message(conn):
    """\n    Sends to the socket LOGGED message with all the logged users\n    Recieves: socket and username (str)\n    Returns: None (sends answer to client)\n    """  # inserted
    all_logged_users = logged_users.values()
    logged_str = ','.join(all_logged_users)
    build_and_send_message(conn, PROTOCOL_SERVER['logged_msg'], logged_str)


def handle_logout_message(conn):
    """\n    Closes the given socket, and removes the current user from the logged_users dictionary\n    Recieves: socket\n    Returns: None\n    """  # inserted
    client_hostname = conn.getpeername()
    if client_hostname in logged_users.keys():
        del logged_users[client_hostname]
    conn.close()


def handle_login_message(conn, data):
    """\n    Gets socket and message data of login message. Checks  user and pass exists and match.\n    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users\n    Recieves: socket and message data\n    Returns: None (sends answer to client)\n    """  # inserted
    client_hostname = conn.getpeername()
    username, password = split_data(data, 2)
    if username not in users.keys():
        send_error(conn, 'Username does not exist')
        return
    if users[username]['password'] != password:
        send_error(conn, 'Password does not match!')
        return
    logged_users[client_hostname] = username
    build_and_send_message(conn, PROTOCOL_SERVER['login_ok_msg'], '')


def handle_client_message(conn, cmd, data):
    """\n    Gets message command and data and calls the right function to handle command\n    Recieves: socket, message command and data\n    Returns: None\n    """  # inserted
    hostname = conn.getpeername()
    hostname_logged_in = hostname in logged_users.keys()
    if not hostname_logged_in:
        if cmd == PROTOCOL_CLIENT['login_msg']:
            handle_login_message(conn, data)
    else:  # inserted
        username = logged_users[hostname]
        if cmd == PROTOCOL_CLIENT['logout_msg']:
            handle_logout_message(conn)
        else:  # inserted
            if cmd == PROTOCOL_CLIENT['getscore_msg']:
                handle_getscore_message(conn, username)
            else:  # inserted
                if cmd == PROTOCOL_CLIENT['gethighscore_msg']:
                    handle_highscore_message(conn)
                else:  # inserted
                    if cmd == PROTOCOL_CLIENT['getlogged_msg']:
                        handle_logged_message(conn)
                    else:  # inserted
                        if cmd == PROTOCOL_CLIENT['getquestion_msg']:
                            handle_question_message(conn)
                        else:  # inserted
                            if cmd == PROTOCOL_CLIENT['sendanswer_msg']:
                                handle_answer_message(conn, username, data)
                            else:  # inserted
                                send_error(conn, ERROR_MSG +
                                           'Unsupported message!')
                                return


def main():
    global users  # inserted
    global questions  # inserted
    users = load_user_database()
    questions = load_questions()
    print('Welcome to Trivia Server!')
    server_socket = setup_socket()
    client_sockets = []
    while True:  # inserted
        rlist, wlist, xlist = select.select(
            [server_socket] + client_sockets, client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                client_socket, client_address = server_socket.accept()
                print('New client joined!', client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:  # inserted
                cmd, data = recv_message_and_parse(current_socket)
                if cmd == None or cmd == PROTOCOL_CLIENT['logout_msg']:
                    handle_logout_message(current_socket)
                    client_sockets.remove(current_socket)
                    print('Connection closed')
                    print_client_sockets(client_sockets)
                else:  # inserted
                    handle_client_message(current_socket, cmd, data)
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist and current_socket in client_sockets:
                current_socket.sendall(data.encode())
        messages_to_send.clear()


if __name__ == '__main__':
    main()
