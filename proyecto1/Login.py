import socket


def create_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def register_user(client_socket):
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    message = "register " + username + " " + password
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(response)

def login_user(client_socket):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    message = "login " + username + " " + password
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(response)
    if response == "Login successful.":
        while True:
            command = input("Enter a command (cd, put, get, mkdir, rmdir, rm, ls, exit): ")
            if command.startswith("cd"):
                folder_name = input("Enter the folder name: ")
                client_socket.send(("cd " + folder_name).encode())
            elif command.startswith("put"):
                file_name = input("Enter the file name: ")
                client_socket.send(("put " + file_name).encode())

            elif command.startswith("get"):
                file_name = input("Enter the file name: ")
                client_socket.send(("get " + file_name).encode())
                response = client_socket.recv(1024).decode()
                if response == "File does not exist.":
                    print(response)
                else:
                    save_location = input("Enter the save location: ")
                    if not save_location.endswith('\\') and not save_location.endswith('/'):
                        save_location += '\\'
                    save_location += file_name
                    with open(save_location, 'wb') as file:
                        while True:
                            content = client_socket.recv(1024)
                            if content == b'END':  # Check if the signal has been received
                                break
                            file.write(content)
                    print("File downloaded successfully.")
                continue

            elif command.startswith("mkdir"):
                folder_name = input("Enter the folder name: ")
                client_socket.send(("mkdir " + folder_name).encode())
            elif command.startswith("rmdir"):
                folder_name = input("Enter the folder name: ")
                client_socket.send(("rmdir " + folder_name).encode())
            elif command.startswith("rm"):
                file_name = input("Enter the file name: ")
                client_socket.send(("rm " + file_name).encode())
            elif command == "ls":
                client_socket.send("ls".encode())
            elif command == "exit":
                client_socket.send("exit".encode())
                break
            else:
                print("Invalid command. Please try again.")
            response = client_socket.recv(1024).decode()
            print(response)

def main():
    client_socket = create_socket()
    client_socket.connect(("192.168.1.3", 54321))

    while True:
        print("Options:")
        print("1. Register a new user")
        print("2. Login with existing user")
        print("3. Quit")
        option = input("Choose an option: ")

        if option == "1":
            register_user(client_socket)
        elif option == "2":
            login_user(client_socket)
        elif option == "3":
            break
        else:
            print("Invalid option. Please try again.")

    client_socket.close()

if __name__ == "__main__":
    main()
