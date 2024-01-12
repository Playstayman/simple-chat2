import socket
import threading
import time
import json


def handle_client(client_socket, clients):
    last_heartbeat_time = time.time()
    while True:
        if time.time() - last_heartbeat_time > 5:
            break
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            if "[HEARTBEAT]" in message:
                last_heartbeat_time = time.time()
            elif "[DOWN]" in message:
                break
            else:
                data_package = json.loads(message)
                message = data_package["username"] + ": " + data_package["message"]
                print(f"Received message: {message}")
                for client in clients:
                    try:
                        if client_socket != client:
                            message = json.dumps(data_package)
                            client.send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending message to a client: {e}")
        except Exception as e:
            print(f"Error: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()
    print("someone left")
    for client in clients:
        try:
            message_data = {"username": "server", "message": "someone left, bye"}
            message = json.dumps(message_data)
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to a client: {e}")


def accept_connections(server_socket, clients):
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients))
        client_thread.start()
        for client in clients:
            try:
                if client_socket != client:
                    message_data = {"username": "server", "message": "someone joined, hi"}
                    message = json.dumps(message_data)
                    client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to a client: {e}")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_ip = socket.gethostbyname(socket.gethostname())
    print(public_ip)
    server_socket.bind((public_ip, 5555))
    server_socket.listen(5)

    clients = []

    accept_thread = threading.Thread(target=accept_connections, args=(server_socket, clients))
    accept_thread.start()
    accept_thread.join()


if __name__ == "__main__":
    main()
