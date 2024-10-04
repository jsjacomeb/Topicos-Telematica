import socket
import threading
import os
import json
import shutil
from NameNode import NameNode  # Importar la clase NameNode

class Server:
    def __init__(self):
        self.storage_file = 'users.json'
        self.users = self.load_users()
        self.current_user = None
        self.current_folder = None
        self.namenode = NameNode()  # Crear una instancia de NameNode

        # Registrar algunos Datanodes a través del NameNode
        self.namenode.register_datanode("Datanode1", "datanode1_storage")
        self.namenode.register_datanode("Datanode2", "datanode2_storage")
        self.namenode.register_datanode("Datanode3", "datanode3_storage")

    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_users(self):
        """Save users to JSON file"""
        with open(self.storage_file, 'w') as file:
            json.dump(self.users, file)

    def register(self, username, password):
        """Register a new user"""
        if username in self.users:
            return "Username already exists. Please choose a different username."
        else:
            self.users[username] = password
            self.save_users()
            self.create_user_folder(username)
            return "User registered successfully."

    def create_user_folder(self, username):
        """Create a folder for the new user"""
        user_folder_path = os.path.join('user_folders', username)
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
            print(f"Folder created for user {username}")

    def login(self, username, password):
        """Login to the system"""
        if username in self.users and self.users[username] == password:
            return "Login successful."
        else:
            return "Invalid username or password."

    def change_directory(self, folder_name):
        """Change the current folder"""
        if folder_name == "..":
            if self.current_folder != os.path.join('user_folders', self.current_user):
                self.current_folder = os.path.dirname(self.current_folder)
                return f"Folder changed to: {self.current_folder}"
            else:
                return "You are already in your root folder."
        else:
            new_folder_path = os.path.join(self.current_folder, folder_name)
            if os.path.exists(new_folder_path):
                self.current_folder = new_folder_path
                return f"Folder changed to: {self.current_folder}"
            else:
                return "Folder does not exist."

    def upload_file(self, file_name, file_data):
        """Upload a file to the distributed file system using file data received from the client."""
        try:
            # Llamar al NameNode para dividir y distribuir el archivo
            block_locations = self.namenode.divide_and_distribute_file(file_name, file_data)
            return f"File {file_name} uploaded and distributed across Datanodes. Block locations: {block_locations}"
        except Exception as e:
            return f"An error occurred: {e}"


    def list_datanodes(self):
        """Listar los Datanodes registrados en el NameNode"""
        return self.namenode.list_datanodes()
    
    def download_file(self, file_name, client_socket):
        """Download a file by gathering blocks from the Datanodes."""
        # Obtener la lista de bloques y sus ubicaciones desde el NameNode
        block_locations = self.namenode.get_file_blocks(file_name)
        
        if not block_locations:
            return "File does not exist."
        
        try:
            # Recorrer cada bloque en la lista
            for block_id, datanode_ids in block_locations:
                # Seleccionar el primer Datanode para recuperar el bloque (podrías implementar mejor tolerancia a fallos aquí)
                datanode_id = datanode_ids[0]
                datanode = next((dn for dn in self.namenode.datanodes if dn["node_id"] == datanode_id), None)
                
                if not datanode:
                    continue
                
                # Leer el contenido del bloque
                block_path = os.path.join(datanode["storage_path"], block_id)
                with open(block_path, 'rb') as block_file:
                    block_data = block_file.read()
                    # Enviar el contenido del bloque al cliente
                    client_socket.sendall(block_data)
            
            # Enviar señal de fin de archivo
            client_socket.send(b'END')
            return "File sent successfully."

        except Exception as e:
            return f"An error occurred during file download: {e}"


    def create_directory(self, folder_name):
        """Create a new folder in the current folder"""
        new_folder_path = os.path.join(self.current_folder, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            return f"Folder created: {new_folder_path}"
        else:
            return "Folder already exists."

    def delete_directory(self, folder_name):
        """Delete a folder in the current folder"""
        folder_path = os.path.join(self.current_folder, folder_name)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                return f"Folder deleted: {folder_path}"
            except OSError as e:
                return f"Error deleting folder: {e}"
        else:
            return "Folder does not exist."

    def delete_file(self, file_name):
        """Delete a file in the current folder"""
        file_path = os.path.join(self.current_folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"File deleted: {file_path}"
        else:
            return "File does not exist."

    def list_files(self):
        """List files in the current folder"""
        files = os.listdir(self.current_folder)
        return "Files in the current folder:\n" + "\n".join(files)




def handle_client(client_socket, server):
    while True:
        message = client_socket.recv(1024).decode()
        print("Received message:", message)

        if message.startswith("register"):
            _, username, password = message.split()
            response = server.register(username, password)
            client_socket.send(response.encode())
        elif message.startswith("login"):
            _, username, password = message.split()
            response = server.login(username, password)
            client_socket.send(response.encode())
            if response == "Login successful.":
                server.current_user = username
                server.current_folder = os.path.join('user_folders', username)
        elif message.startswith("cd"):
            _, folder_name = message.split()
            response = server.change_directory(folder_name)
            client_socket.send(response.encode())

        elif message.startswith("get"):
            _, file_name = message.split()
            response = server.download_file(file_name, client_socket)
            client_socket.send(response.encode())

        elif message.startswith("put"):
            _, file_name = message.split()
            
            # Responder al cliente que está listo para recibir el archivo
            client_socket.send("Ready to receive".encode())
            
            # Recibir el contenido del archivo
            file_data = b""
            while True:
                content = client_socket.recv(1024)
                if content == b'END':  # Señal de fin de archivo
                    break
                file_data += content
            
            # Almacenar el archivo utilizando el método del servidor
            response = server.upload_file(file_name, file_data)
            client_socket.send(response.encode())
        elif message == "list_datanodes":
            response = server.list_datanodes()
            client_socket.send(response.encode())
            
        elif message.startswith("mkdir"):
            _, folder_name = message.split()
            response = server.create_directory(folder_name)
            client_socket.send(response.encode())
        elif message.startswith("rmdir"):
            _, folder_name = message.split()
            response = server.delete_directory(folder_name)
            client_socket.send(response.encode())
        elif message.startswith("rm"):
            _, file_name = message.split()
            response = server.delete_file(file_name)
            client_socket.send(response.encode())
        elif message == "ls":
            response = server.list_datanodes()
            client_socket.send(response.encode())
        elif message == "exit":
            client_socket.send("Exiting.".encode())
            break


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.1.36", 54321))
    server_socket.listen(5)

    server = Server()

    print("Server started. Waiting for incoming connections...")

    while True:
        client_socket, address = server_socket.accept()
        print("Incoming connection from", address)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, server))
        client_handler.start()

if __name__ == "__main__":
    main()
