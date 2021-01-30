import socket
import threading

HOST = '127.0.0.1'
# Replace the above value with the Private IP of the server or leave it empty, it will automatically bind to the correct IP
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET is the type of socket called internet and SOCK_STREAM is another type of socket called TCP socket
server.bind((HOST, PORT))  # Bind/start the server with above specified host and port

server.listen()  # Start listening to tcp requests

clients = []  # Empty list of client to store values later
nicknames = []  # Empty list of nicknames to store values later


# Broadcast Function - Sends the message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle Function - Handles individual connections to the clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)  # Taking the input of message from client
            print(f"{message}")
            # Printing the message of the client to the server
            broadcast(message)  # Broadcasting message to all users
        except:
            # Handles error of the client gets disconnect from the server
            index = clients.index(client)  # Get index of client in clients list
            clients.remove(client)  # Remove client from the list
            client.close()
            nickname = nicknames[index]  # Get the nickname at the index of client that is to be removed
            nicknames.remove(nickname)  # Remove the nickname of disconnected client from the list
            break


# Receive Function - Accepts new connections and joins user to the chat room
def receive():
    while True:
        client, address = server.accept()  # Getting the client name and it's IP address from the server
        print(f"Connected with {str(address)}!")  # Printing the connected status

        client.send("Enter NICKNAME:".encode('utf-8'))  # Asking client for input of it's username
        nickname = client.recv(1024)  # Storing the nickname of the client enter by client itself

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        # Sending the message to be displayed on the server (Just for convenience)
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        # Sending the message to all the users of one new member is added

        client.send("You are now connected to the server!". encode('utf-8'))
        # Sending message to that particular client who just joined the server

        thread = threading.Thread(target=handle, args=(client,))
        # Created a thread whose target function is 'handle()' with parameters passed as 'client'
        # A comma(,) is added after the input of parameter so as to treat it like a tuple
        thread.start()


print("Server is running...")
receive()
