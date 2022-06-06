import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(3)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)



def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, adress = server.accept()
        print(f"Connected with {str(adress)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"{nickname.decode('utf-8')} - is your nickname")
        broadcast(f"{nickname.decode('utf-8')} is now connected\n".encode('utf-8'))
        client.send("Connected to server".encode('utf-8'))

        client_thread = threading.Thread(target=handle, args=(client,))
        client_thread.start()


print("Server start")
receive()