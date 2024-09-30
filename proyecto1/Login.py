import json
import os
import tkinter as tk
from tkinter import filedialog
import shutil

class AuthenticationSystem:
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.users = self.load_users()
        self.current_user = None
        self.current_folder = None

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
            print("Username already exists. Please choose a different username.")
        else:
            self.users[username] = password
            self.save_users()
            print("User registered successfully.")
            
            # Create a folder for the new user
            user_folder_path = os.path.join('user_folders', username)
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)
                print(f"Folder created for user {username}")

    def login(self, username, password):
        """Login to the system"""
        if username in self.users and self.users[username] == password:
            print("Login successful.")
            self.current_user = username
            self.current_folder = os.path.join('user_folders', username)
            self.navigate_folder()
        else:
            print("Invalid username or password.")

    def navigate_folder(self):
        """Navigate and manage files within the user's folder"""
        while True:
            print(f"\nYou are currently in folder: {self.current_folder}")
            command = input("Enter a command (ls, cd, put, get, mkdir, rmdir, rm, exit): ")
            if command == "ls":
                self.list_files()
            elif command == "cd":
                self.change_directory()
            elif command == "put":
                self.upload_file()
            elif command == "get":
                self.download_file()
            elif command == "mkdir":
                self.create_directory()
            elif command == "rmdir":
                self.delete_directory()
            elif command == "rm":
                self.delete_file()
            elif command == "exit":
                break
            else:
                print("Invalid command. Please try again.")

    def list_files(self):
        """List files in the current folder"""
        files = os.listdir(self.current_folder)
        print("Files in the current folder:")
        for file in files:
            print(file)

    def change_directory(self):
        """Change the current folder"""
        folder_name = input("Enter the folder name: ")
        if folder_name == "..":
            # Navigate up one level, but only within the user's folder
            if self.current_folder != os.path.join('user_folders', self.current_user):
                self.current_folder = os.path.dirname(self.current_folder)
                print(f"Folder changed to: {self.current_folder}")
            else:
                print("You are already in your root folder.")
        else:
            new_folder_path = os.path.join(self.current_folder, folder_name)
            if os.path.exists(new_folder_path):
                self.current_folder = new_folder_path
                print(f"Folder changed to: {self.current_folder}")
            else:
                print("Folder does not exist.")

    def upload_file(self):
        """Upload a file to the current folder"""
        file_name = input("Enter the file name: ")
        try:
            with open(file_name, 'r+b') as file:
                content = file.read()
            with open(os.path.join(self.current_folder, file_name), 'w+b') as file:
                file.write(content)
            print(f"File uploaded to: {self.current_folder}")
        except PermissionError:
            print("Permission denied. Please check the file permissions and try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def download_file(self):
        """Download a file from the current folder"""
        file_name = input("Enter the file name: ")
        file_path = os.path.join(self.current_folder, file_name)
        if os.path.exists(file_path):
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=file_name)
            if save_file_path:
                with open(file_path, 'rb') as file:
                    content = file.read()
                with open(save_file_path, 'wb') as file:
                    file.write(content)
                print(f"File saved to: {save_file_path}")
            else:
                print("Download cancelled.")
        else:
            print("File does not exist.")

    def create_directory(self):
        """Create a new folder in the current folder"""
        folder_name = input("Enter the folder name: ")
        new_folder_path = os.path.join(self.current_folder, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder created: {new_folder_path}")
        else:
            print("Folder already exists.")

    def delete_directory(self):
        """Delete a folder in the current folder"""
        folder_name = input("Enter the folder name: ")
        folder_path = os.path.join(self.current_folder, folder_name)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Folder deleted: {folder_path}")
            except OSError as e:
                print(f"Error deleting folder: {e}")
        else:
            print("Folder does not exist.")

    def delete_file(self):
        """Delete a file in the current folder"""
        file_name = input("Enter the file name: ")
        file_path = os.path.join(self.current_folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            print("File does not exist.")

def main():
    storage_file = 'users.json'
    auth_system = AuthenticationSystem(storage_file)

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            auth_system.register(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            auth_system.login(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()