import socket
import threading
import time
import os

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        while True:
            try:
                self.client.connect((self.host, self.port))
                print("Connected to server")                    
                break
            except:
                print("Failed to connect to server, trying to reconnect...")
                time.sleep(10)
        username = f"@{input('Write ur username: @')}"
        self.client.send(username.encode('utf-8'))
        threading.Thread(target=self._receive_messages, daemon=True).start()

    def _receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"\nMessage from server: {message}")
                else:
                    break
            except:
                break

    def send_message(self):
        try:
            message = input('Write ur message: ')
            self.client.send(message.encode('utf-8'))
        except:
            print("Failed to send message")
            self.connect_to_server()

def terminal():
    host = '127.0.0.1'
    port = 5555
    client = Client(host, port)

    while True:
        consoleinput = input('Write command, if u dont know type "help": ')
        if consoleinput == 'connect':
            print(f'Trying connect to {host}:{port}')
            client.connect_to_server()
            continue
        elif consoleinput == 'help':
            print("""                    connect - connect to server
                    sendmsg - send message to server
                    changedata - change host or port, after changing u need to reconnect
                    clear - to clear console
                     
                     exit - closing programm""")
            continue
        elif consoleinput == 'sendmsg':
            client.send_message()
            continue
        elif consoleinput == 'changedata':
            oneortwo = input('What do you want to change? 1 - host, 2 - port')
            if oneortwo == '1':
                host = input('Write new host: ')
            else:
                port = input('Write new port: ')
                continue
        elif consoleinput == 'exit':
            print('Closing programm')
            time.sleep(1)
            break
        elif consoleinput == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        else:
            print('Unknown command')
            continue

if __name__ == '__main__':
    terminal()
        


    
