
import socket
import threading

IP = "127.0.0.1"
PORT = 5555
chat_id = 1
FORMAT = 'utf-8'
active_chat_list = []


class Chat:
    def __init__(self, password):
        self.clients = []
        self.group_id = get_auto_id()
        self.password = password


def get_auto_id():
    global chat_id
    chat_id += 1
    return chat_id - 1


def broadcast_message(message, conn, chat_room):
    name = None
    for client in chat_room.clients:
        if client["connection"] == conn:
            name = client["name"]
            break
    if name is not None:
        for client in chat_room.clients:
            try:
                client["connection"].send(f'{name}: {message}'.encode(FORMAT))
            except:
                print("CONNECTION INTERRUPTED")


def join_chat_room(conn, addr):
    global active_chat_list
    id_check = False
    password_check = False
    conn.send("Please enter your name".encode(FORMAT))
    name = conn.recv(1024).decode(FORMAT)
    conn.send(f"Hello {name}, Please enter the wanted group ID:".encode(FORMAT))
    group_id = conn.recv(1024).decode(FORMAT)
    try:
        group_id = int(group_id)
    except:
        conn.send("Group ID Must be a Number, try again:\n".encode(FORMAT))
        handle_new_user(conn, addr)
    for chat_room in active_chat_list:
        if chat_room.group_id == group_id:
            id_check = True
            conn.send(f"{id_check}".encode(FORMAT))
            conn.send("Please enter the password:".encode(FORMAT))
            password = conn.recv(1024).decode(FORMAT)
            if chat_room.password == password:
                password_check = True
                chat_room.clients.append({"connection": conn, "name": name})
                conn.send(f"welcome {name} to group '{chat_room.group_id}' - you can send message".encode(FORMAT))
                break
            else:
                conn.send(f"Incorrect password, you are being sent back to the main menu\n".encode(FORMAT))
                break
    if not id_check:
        conn.send("false".encode(FORMAT))
        conn.send(f"Incorrect chat ID, you are being sent back to the main menu\n".encode(FORMAT))
        handle_new_user(conn, addr)
    elif not password_check:
        handle_new_user(conn, addr)
    while True:
        message = conn.recv(1024).decode(FORMAT)
        broadcast_message(message, conn, chat_room)


def create_chat_room(conn):
    global active_chat_list
    conn.send("Please enter your name".encode(FORMAT))
    name = conn.recv(1024).decode(FORMAT)
    conn.send("Please enter a password :".encode(FORMAT))
    password = conn.recv(1024).decode(FORMAT)
    new_chat_room = Chat(password)
    new_chat_room.clients.append({"connection": conn, "name": name})
    active_chat_list.append(new_chat_room)
    conn.send(f"Welcome {name} to group '{new_chat_room.group_id}' - you can send messages".encode(FORMAT))
    while True:
        message = conn.recv(1024).decode(FORMAT)
        broadcast_message(message, conn, new_chat_room)


def handle_new_user(conn, addr):
    conn.send("Hello client, please choose an option:\n" "1. Connect to a group chat.\n"
              "2. Create a group chat.\n" "3. Exit the server.\n".encode(FORMAT))
    user_choice = conn.recv(1024).decode(FORMAT)
    if user_choice == "1":
        join_chat_room(conn, addr)
    elif user_choice == "2":
        create_chat_room(conn)
    elif user_choice == "3":
        print(f"Client at {addr[0]} has disconnected.")
        conn.close()
    else:
        conn.send("please enter a valid option".encode(FORMAT))
        handle_new_user(conn, addr)


def chat_room_app():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr[0]} connected.")
        thread = threading.Thread(target=handle_new_user, args=(conn, addr))
        thread.start()


chat_room_app()
