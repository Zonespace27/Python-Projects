import socket
import threading
import re
import pickle
from json import load
import file_locations_server as file_locations
import client_commands
from exec import Exec
import os
import sys
import random
import string
import colorama

class Server():
    HOST = "127.0.0.1" #"127.0.0.1"
    PORT = 65432 #65432

    all_connections = []

    name_to_command = {}

    # List of sockets that have admin perms
    administrators = []

    admin_pass = ""

    socket_to_name = {}

    socket_to_ip = {}

    socket_to_color = {}

    # For exec things, send unencoded text
    def sendall_wrapper(self, target = None, pickle_list = {}):
        pickle_list = pickle.dumps(pickle_list)
        if target == None:
            for connection in self.all_connections:
                connection.sendall(pickle_list)   
            return
        if target in self.all_connections:
            target.sendall(pickle_list)
    
    def add_admin(self, adding_admin):
        self.administrators.append(adding_admin)
        print("Client " + self.get_full_name(adding_admin)  + " has gained admin powers.")
    
    def verify_name(self, executor, name):
        if name in self.socket_to_name.values():
            self.sendall_wrapper(executor, {"output": "That name is already in use."})
            return False
        if len(name) <= 3:
            self.sendall_wrapper(executor, {"output": "This name is too short."})
            return False
        return True

    def recieve_name_change(self, socket, name, silent = False):
        if socket not in self.socket_to_name:
            self.socket_to_name[socket] = name
            print("New client name: " + name)
            self.sendall_wrapper(pickle_list = {"output": name + " has connected."})
            return
        print("Client formerly known as " + self.get_full_name(socket) + " has changed their name to " + name)
        if not silent:
            self.sendall_wrapper(pickle_list = {"output": self.socket_to_name[socket] + " is now known as " + name + "."})
        self.socket_to_name[socket] = name

    def listen_singular(self, conn):
        while True:
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                self.handle_disconnect(conn)
                return
            if not data:
                continue
            data = pickle.loads(data)
            name = data.get("name")
            if conn not in self.socket_to_name:
                self.recieve_name_change(conn, name)
            name = self.socket_to_name[conn]
            text = data.get("input")
            text = re.sub("\'|b\'|\"|b\"", "", text)
            if len(text) <= 0:
                continue
            if text[0] == "/":
                regex_locate = re.search(" ", text)
                if regex_locate == None:
                    argument = ""
                    first_space_position = len(text)
                else:
                    first_space_position = text.find(" ")
                    argument = text[first_space_position + 1:]
                if text[1:first_space_position] in self.name_to_command:
                    gotten_command = self.name_to_command.get(text[1:first_space_position])
                    if gotten_command == None:
                        print("Invalid command.")
                        continue
                    print(self.get_full_name(conn) + " executed command: " + gotten_command.name)
                    Exec(gotten_command.on_exec, {}, {"executor": conn, "server_class": self, "argument": argument})
                continue
            print(f"Recieved: {text} || from {self.get_full_name(conn)}")
            pickle_list = {"name": name, "output": text, "color": self.socket_to_color[conn] if conn in self.socket_to_color.keys() else "none"}
            for connection in self.all_connections:
                self.sendall_wrapper(connection, pickle_list) #TODO: refactor to use a picklelist like client

    def handle_disconnect(self, conn):
        print("Client " + self.get_full_name(conn) + " disconnected.")
        disconnected_name = str(self.socket_to_name[conn])
        self.all_connections.remove(conn)
        self.socket_to_name.pop(conn)
        self.socket_to_ip.pop(conn)
        del(conn)
        # Needs to happen after conn's been removed
        self.sendall_wrapper(pickle_list = {"output": disconnected_name + " has disconnected."})

    def accept_conns(self, socket_class):
        while True:
            conn, addr = socket_class.accept()
            print(f"Connected by {addr}")
            self.all_connections.append(conn)
            self.socket_to_ip[conn] = addr

            new_thread = threading.Thread(target=self.listen_singular, args=(conn,))
            new_thread.start()

    def generate_admin_password(self):
        for i in range(8):
            self.admin_pass += random.choice(string.ascii_letters)
        print("Password is: " + self.admin_pass)
    
    def get_full_name(self, conn):
        return str(self.socket_to_name[conn]) + " (" + str(self.socket_to_ip[conn]) + ")"

    def __init__(self):
        self.HOST = input("Hosting IP address: \n")
        self.PORT = int(input("Hosting port: \n"))
        os.chdir(os.path.dirname(sys.argv[0]))
        colorama.init(autoreset=True)
        global server_class
        server_class = self

        client_command_data = load(open(file_locations.CLIENT_COMMANDS_FILE))
        for command_name in client_command_data:
            client_command = client_commands.ClientCommand(command_name)
            self.name_to_command[client_command.name] = client_command
            
        self.generate_admin_password()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()

            conn_thread = threading.Thread(target=self.accept_conns, args=(s,))
            conn_thread.start()
            conn_thread.join()

if __name__ == "__main__":
    Server()