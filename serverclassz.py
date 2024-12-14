import socket
import threading
import os
from datetime import datetime

clients = {}

class Server:
    def __init__(self, host, port, max_clients):
        self.maxclients = max_clients
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isserverstart = False
        self.username = ''
    
    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.isserverstart = True
        print(self.server)
        print(f"Server start on {self.host}:{self.port}, waiting clients")
        client_handler = threading.Thread(target=self.handle_client)
        client_handler.start()

    # def stop_server(self):
    #     self.server.close()

    def handle_client(self):
        while True:
            client_socket, addr = self.server.accept()
            self.username = client_socket.recv(1024).decode('utf-8')
            
            if self.username.startswith('@') and self.username not in clients:
                clients[self.username] = client_socket  # Сохраняем сокет клиента
                print(f"Client {self.username} joined from {addr}")
                messages_handler = threading.Thread(target=self.handle_messages, args=(client_socket, self.username))
                messages_handler.start()
            else:
                print(f"Username {self.username} is already taken or invalid.")
                client_socket.close()  # Закрываем сокет, если никнейм занят
         
    def handle_messages(self, client_socket, username):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Message from {username}: {message}")
            except ConnectionResetError:
                print(f"Client {username} has disconnected.")
                del clients[username]  # Удаляем клиента из словаря
                break
        
    def send_message(self):
        if self.isserverstart:
            try:
                message = input('Write your message: ')
                print(self.username)
                if self.username in clients:
                    clients[self.username].send(message.encode('utf-8'))
                else:
                    print("Username not found in clients.")
            except Exception as e:
                print(f"Failed to send message: {e}")
        else:
            print("You need to start the server")

    def is_connected(self):
            try:
        # Отправляем пустой пакет (можно использовать любой другой)
                self.server.send(b'')
                return True
            except socket.error:
                return False
            

def handle_console():
    MyServer = Server(host='127.0.0.1', port=5555, max_clients=25)    
    while True:
        command = input()

        if command.lower() == 'start':
            startcommandtime = datetime.now()
            print('starting')
            MyServer.start_server()
            endstartingcommandtime = datetime.now()
            elapsedtimetostart = endstartingcommandtime - startcommandtime
            print(f'Started. Elapsed time: {elapsedtimetostart}')
            continue
        elif command.lower() in ['h', 'help', '--h']:
            print("""Server commands:\n
                  Start - starting server on localhost, port 5555
                  Change - you can change your host and port
                  Send - send message to client
                  Checkconn - checking connection with client\n
                  To exit write 'exit' or 'esc'\n
                  Version 0.2""")
            continue
        elif command.lower() == 'change':
            oneortwo = input('What do you want to change? 1 - host, 2 - port')
            if oneortwo == '1':
                host = input('Enter new host: ')
                MyServer.host = host
                continue
            elif oneortwo == '2':
                port = input('Enter new port: ')
                MyServer.port = port
                continue
            else:
                continue
        elif command.lower() == 'send':
            MyServer.send_message()
            continue
        # elif command.lower() == 'stop':
        #     MyServer.stop_server()
        #     continue
        elif command.lower() == 'checkconn':
            if MyServer.is_connected():
                print('Client connected')
                continue
            else:
                print('Client dont connected')
                continue
        elif command.lower() == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command.lower in ['exit', 'esc']:
            break
            
if __name__ == "__main__":
    handle_console()