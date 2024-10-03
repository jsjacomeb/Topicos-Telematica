import socket
import time
import threading
import os

def send_message(client_socket):
    stop_event = threading.Event()
    def receive_message():
        while True:
            try:
                data = client_socket.recv(1024).decode()
            except ConnectionResetError:
                stop_event.set()
                break
            if not data:
                stop_event.set()
                break
            if data == "stop":
                stop_event.set()

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

    while not stop_event.is_set():
        time.sleep(5)  # wait for 5 seconds
        try:
            client_socket.send("I am working".encode())
        except ConnectionResetError:
            stop_event.set()
    print("Stopping...")

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

    while not stop_event.is_set():
        time.sleep(5)  # wait for 5 seconds
        client_socket.send("I am working".encode())
    print("Stopping...")

def send_folder(client_socket, folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Send the folder path
    client_socket.sendall(f'folder {os.path.basename(folder_path)}'.encode())
    
    # Send each file in the folder
    for file in files:
        file_path = os.path.join(folder_path, file)
        file_size = os.path.getsize(file_path)
        
        # Send the file name and size
        client_socket.sendall(f'file {file} {file_size}'.encode())
        
        with open(file_path, 'rb') as file_data:
            while True:
                file_chunk = file_data.read(4096)
                if not file_chunk:
                    break
                client_socket.sendall(file_chunk)
                
    # Notify that all files are sent
    client_socket.sendall(b'done')


def receive_files(client_socket, folder_path):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if data.startswith("folder"):
            folder_name = data.split(" ")[1]
            folder_path = os.path.join(folder_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
        elif data.startswith("file"):
            _, file_name, file_size = data.split()
            file_size = int(file_size)
            
            with open(os.path.join(folder_path, file_name), 'wb') as file:
                received_size = 0
                while received_size < file_size:
                    file_data = client_socket.recv(4096)
                    if not file_data:
                        break
                    file.write(file_data)
                    received_size += len(file_data)
        elif data == 'done':
            break


def create_receivers_folder(client_name):
    """Create a folder for the new user"""
    receivers = os.path.join('receivers', client_name)
    if not os.path.exists(receivers):
        os.makedirs(receivers)
        print(f"Folder created for user {client_name}")

def create_replicates_folder(client_name):
    """Create a folder for the new user"""
    replicates = os.path.join('replicates', client_name)
    if not os.path.exists(replicates):
        os.makedirs(replicates)
        print(f"Folder created for user {client_name}")

def client_program(ip, port, client_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    # Receive client name from server
    received_client_name = client_socket.recv(1024).decode()
    print(f"Client name: {received_client_name}")

    if "receiver" in received_client_name:
        create_receivers_folder(received_client_name)
    else:  
        create_replicates_folder(received_client_name) 

    # Wait for start message from server
    start_message = client_socket.recv(1024).decode()
    print("Received start message from server:", start_message)

    if "receiver" in received_client_name:
        thread = threading.Thread(target=send_message, args=(client_socket,))
        thread.start()

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if data.startswith("folder"):
            folder_path = os.path.join('receivers', received_client_name) if "receiver" in received_client_name else os.path.join('replicates', received_client_name)
            receive_files(ip, port, folder_path)
        elif data == "request_folder":
            folder_path = os.path.join('replicates', received_client_name)
            send_folder(client_socket, folder_path)

 
if __name__ == '__main__':
    ip = '192.168.1.3'  # replace with the server's IP address
    port = 50000

    for i in range(4):
        threading.Thread(target=client_program, args=(ip, port, f"Client {i+1}")).start()