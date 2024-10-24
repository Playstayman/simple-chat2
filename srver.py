import socket
import threading
import time
import json
import requests
import ssl


def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        ip_data = response.json()
        return ip_data.get('origin')
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_ipv4_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None


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
        ssl_client = ssl.wrap_socket(client_socket, server_side=True, certfile="certificate.crt", keyfile="server.key",
                                     ssl_version=ssl.PROTOCOL_TLS)
        clients.append(ssl_client)
        client_thread = threading.Thread(target=handle_client, args=(ssl_client, clients))
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
    print("ip for local server: " + public_ip + "\n")
    print(f"if you got your router set up you can use this {get_public_ip()}")
    server_socket.bind((public_ip, 5555))
    server_socket.listen(5)

    clients = []

    accept_thread = threading.Thread(target=accept_connections, args=(server_socket, clients))
    accept_thread.start()
    accept_thread.join()


if __name__ == "__main__":
    main()
