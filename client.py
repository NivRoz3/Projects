import socket
import threading

SERVER_IP = "127.0.0.1"  # Replace with the IP address of the server
SERVER_PORT = 5555  # Replace with the port number of the server
ENCODING = 'utf-8'


def main_menu():
    # Receive message from the server and decode it
    message_from_server = client_socket.recv(1024).decode(ENCODING)
    print(message_from_server)

    # Get the user's choice
    choice = input()

    # Keep asking for a valid choice until one is provided
    while choice != "1" and choice != "2" and choice != "3":
        print("Please enter a valid option")
        choice = input()

    # Take the appropriate action based on the choice
    if choice == "1":
        joining_chat()
    elif choice == "2":
        creating_chat()
    elif choice == '3':
        # Close the client's connection with the server
        client_socket.close()
        print("\ndisconnecting from the server")


def creating_chat():
    # Send choice "2" to the server
    client_socket.send("2".encode(ENCODING))
    # Receive name request message from the server and decode it
    name_request = client_socket.recv(1024).decode(ENCODING)
    print(name_request)
    # Get the user's name
    name = input()
    # Send the name to the server
    client_socket.send(name.encode(ENCODING))
    # Receive password request message from the server and decode it
    password_request = client_socket.recv(1024).decode(ENCODING)
    print(password_request)
    # Get the user's password
    password = input()
    # Send the password to the server
    client_socket.send(password.encode(ENCODING))
    # Start handling messages from the server
    message_handler()


def joining_chat():
    client_socket.send("1".encode(ENCODING))
    # Receive request for chat name from the server and decode it
    name_request = client_socket.recv(1024).decode(ENCODING)
    print(name_request)
    # Get the user's input for the chat name
    name = input()
    # Send the chat name to the server
    client_socket.send(name.encode(ENCODING))
    # Receive request for chat ID from the server and decode it
    id_request = client_socket.recv(1024).decode(ENCODING)
    print(id_request)
    # Get the user's input for the chat ID
    group_id = input()
    # Send the chat ID to the server
    client_socket.send(group_id.encode(ENCODING))
    response = client_socket.recv(1024).decode(ENCODING)
    # If the chat ID is valid, request the password from the user
    if response == "True":
        password_request = client_socket.recv(1024).decode(ENCODING)
        print(password_request)
        password = input()
        client_socket.send(password.encode(ENCODING))
        password_response = client_socket.recv(1024).decode(ENCODING)
        # If the password is correct, start handling messages from the server
        if password_response.startswith("welcome"):
            print(password_response)
            message_handler()
        # If the password is incorrect, print the error message and go back to the main menu
        else:
            print(password_response)
            main_menu()
    # If the chat ID is written in letters, prints a error message and go back to the main menu
    elif response.startswith("Group"):
        print(response)
        main_menu()
    # If the chat ID is not valid/doesn't exist, print a error message and go back to the main menu
    else:
        valid_id_response = client_socket.recv(1024).decode(ENCODING)
        print(valid_id_response)
        main_menu()


def message_handler():
    # Start a new thread to send messages
    thread_send = threading.Thread(target=message_sender)
    thread_send.start()
    # Start a new thread to receive messages
    thread_get = threading.Thread(target=receive_messages)
    thread_get.start()
    # Wait for the threads to complete
    thread_send.join()
    thread_get.join()


# once a client has entered a chat room this function takes the client input and sends it to the server
# so it can be sent to all clients in the same chat room
def message_sender():
    while True:
        message = input()
        client_socket.send(message.encode(ENCODING))


# once a client has entered a chat room this function receives the messages sent by other clients in the same chat room
# and prints them to the client
def receive_messages():
    while True:
        print(client_socket.recv(1024).decode(ENCODING))


# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

main_menu()
