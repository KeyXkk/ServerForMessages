import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Сообщение от сервера: {message}")
            else:
                break
        except:
            break

def start_client(host='localhost', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Запускаем поток для получения сообщений
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        message = input("Введите сообщение: ")
        if message.lower() == 'exit':
            break
        client.send(message.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    start_client()
