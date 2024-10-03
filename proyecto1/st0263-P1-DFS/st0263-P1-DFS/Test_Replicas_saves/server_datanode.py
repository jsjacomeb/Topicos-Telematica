import socket
import threading
import time
import os

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.client_names = []
        self.client_counter = 0
        self.receiver_replica_map = {}

    def request_folder(self, client_socket, client_name):
        client_socket.send("send_folder".encode())
        folder_path = client_socket.recv(1024).decode()
        files = []
        while True:
            file_name = client_socket.recv(1024).decode()
            if file_name == 'done':
                break
            files.append(file_name)

        # Send the list of files to the other clients
        for i, client in enumerate(self.clients):
            if client != client_socket:
                client.sendall(f'folder {folder_path}'.encode())
                for file in files:
                    client.sendall(f'file {file}'.encode())
                client.sendall('done'.encode())

    def display_clients(self):
        print("Connected clients:")
        for i, client_name in enumerate(self.client_names):
            print(f"{i+1}. {client_name}")

    def display_replica_maps(self):
        print("Replica maps:")
        for receiver, replica in self.receiver_replica_map.items():
            print(f"{receiver} -> {replica}")


    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print("Server is listening on", self.host, "port", self.port)

        while True:
            client_socket, address = self.server_socket.accept()
            print("Connection from", address)

            self.client_counter += 1
            if self.client_counter % 2 == 1:
                client_name = f"receiver{self.client_counter // 2 + 1}"
                self.receiver_replica_map[client_name] = f"replica{self.client_counter // 2 + 1}"


            else:
                client_name = f"replica{self.client_counter // 2}"


            self.clients.append(client_socket)
            self.client_names.append(client_name)

            print(f"Client {client_name} connected")

            # Send client name to client
            client_socket.send(client_name.encode())

            threading.Thread(target=self.handle_client, args=(client_socket, client_name)).start()


    def handle_client(self, client_socket, client_name):
        last_message_time = time.time()

        def check_timer():
            while True:
                if time.time() - last_message_time > 30:
                    if "receiver" in client_name:
                        replica_name = self.receiver_replica_map[client_name]
                        for i, client in enumerate(self.clients):
                            if self.client_names[i] == replica_name:
                                # Request a folder from the replica
                                client.send(b"request_folder")
                                print(f"Requested folder from {replica_name}")

                                # Receive the folder path from the replica
                                folder_path = client.recv(1024).decode(errors='ignore')
                                print(f"Receiving folder: {folder_path}")

                                # Ensure the folder exists locally
                                os.makedirs(folder_path, exist_ok=True)

                                while True:
                                    # Receive the name of the file
                                    file_name = client.recv(1024).decode(errors='ignore')
                                    if file_name == 'done':
                                        break

                                    print(f"Receiving file: {file_name}")

                                    # Receive the file size
                                    file_size = int(client.recv(1024).decode(errors='ignore'))
                                    received_size = 0

                                    # Open the file for writing in binary mode
                                    with open(os.path.join(folder_path, file_name), 'wb') as f:
                                        while received_size < file_size:
                                            file_data = client.recv(min(4096, file_size - received_size))
                                            if not file_data:
                                                break
                                            f.write(file_data)
                                            received_size += len(file_data)

                                        print(f"File {file_name} received successfully")

                                # Send the folder to the other clients
                                for j, other_client in enumerate(self.clients):
                                    if other_client != client and self.client_names[j] != client_name:
                                        other_client.sendall(f'folder {folder_path}'.encode())
                                        for file in os.listdir(folder_path):
                                            file_path = os.path.join(folder_path, file)
                                            other_client.sendall(f'file {file}'.encode())

                                            # Send the file size first
                                            file_size = os.path.getsize(file_path)
                                            other_client.sendall(str(file_size).encode())

                                            # Send the file content
                                            with open(file_path, 'rb') as f:
                                                while True:
                                                    file_data = f.read(4096)
                                                    if not file_data:
                                                        break
                                                    other_client.sendall(file_data)
                                        
                                        other_client.sendall(b'done')

        threading.Thread(target=check_timer).start()

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received data from {client_name}: {data} (elapsed time: {time.time() - last_message_time:.2f} seconds)")
                current_time = time.time()
                elapsed_time = current_time - last_message_time
                last_message_time = current_time

                if data == b"I am working" and "receiver" in client_name:
                    # Send data to replica
                    pass
            except Exception as e:
                print(f"An error occurred: {e}")
                break



    def send_start_message(self):
        for i, client in enumerate(self.clients):
            client.send("start".encode())
            print(f"Sent start message to {self.client_names[i]}")
            # Wait for clients to receive the start message


def main():
    server = Server('192.168.1.3', 50000)  # replace with the server's IP address
    threading.Thread(target=server.start_server).start()

    while True:
        user_input = input("Enter 'start' to send start message to all clients: ")
        if user_input.lower() == 'start':
            server.send_start_message()
        if user_input.lower() == 'list':
            server.display_clients()
        elif user_input.lower() == 'stop':
            server.display_clients()
            client_index = int(input("Enter the number of the client to stop: ")) - 1
            if client_index < len(server.clients):
                server.clients[client_index].send("stop".encode())
                print(f"Sent stop message to client {server.client_names[client_index]}")
            else:
                print("Invalid client index")
        elif user_input.lower() == 'maps':
            server.display_replica_maps()
if __name__ == '__main__':
    main()