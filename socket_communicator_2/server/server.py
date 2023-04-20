import admin_commands
import client_commands
import file_locations_server as file_locations
from json import load
import message_handler as messageHandler
import os
import pickle
import random
import socket
import string
import sys
import threading

class Server():
    HOST = "127.0.0.1" #"127.0.0.1"
    PORT = 65432 #65432

    all_connections = []

    name_to_command = {}

    # List of sockets that have admin perms
    administrators = []

    # The password that clients must enter to gain admin powers
    admin_pass = ""

    # Dict of socket object to the socket's name
    socket_to_name = {}

    # Dict of socket object to the socket's IP
    socket_to_ip = {}

    # Ref to the message queue handler
    message_handler: messageHandler.MessageHandler = None

    # What message to show clients when they connect
    message_of_the_day = "Thank you for connecting, use \"/help\" for commands you can execute."

    # For exec things, send unencoded text
    def sendall_wrapper(self, target: socket.socket = None, pickle_list: dict = {}):
        """
        Wrapper for sendall() that does extra handling with pickle and such.
        """
        pickle_list = pickle.dumps(pickle_list)
        if not target:
            for connection in self.all_connections:
                connection.sendall(pickle_list)   

            return

        if target in self.all_connections:
            target.sendall(pickle_list)


    def listen_singular(self, conn: socket.socket):
        """
        Listen for messages coming from a specific socket, and then forward them to the message handler.
        """
        while True:
            try:
                data = conn.recv(1024)

            except ConnectionResetError:
                self.handle_disconnect(conn)
                return

            if not data:
                continue
            
            data = pickle.loads(data) # This converts the data into a dict, {"input": CLIENT INPUT HERE}, with "name":"" as well if the client is initially registering with the server
            data["connection"] = conn

            if conn in self.socket_to_name.keys():
                data["name"] = self.socket_to_name[conn]
                
            self.message_handler.add_message(data)

    def handle_disconnect(self, conn: socket.socket):
        """
        Disconnects a socket object from the server forcefully.
        """
        print("Client " + self.get_full_name(conn) + " disconnected.")
        disconnected_name = str(self.socket_to_name[conn])

        self.all_connections.remove(conn)
        self.socket_to_name.pop(conn)
        self.socket_to_ip.pop(conn)

        conn.close()
        del(conn)

        # Needs to happen after conn's been removed
        self.sendall_wrapper(pickle_list = {"output": disconnected_name + " has disconnected."})


    def accept_conns(self, socket_class: socket.socket):
        """
        Await incoming connections, and initialize them when they come along.
        """
        while True:
            conn, addr = socket_class.accept()

            with open(file_locations.BAN_FILE) as file:
                ban_lines = [line.rstrip() for line in file]
                file.close()

            if addr[0] in ban_lines:
                print(f"Banned IP address {addr} attempted to connect.")
                conn.close()
                del(conn)
                continue

            print(f"Connected by {addr}")
            self.all_connections.append(conn)
            self.socket_to_ip[conn] = addr
            self.sendall_wrapper(conn, {"output": self.message_of_the_day})

            # Spin up a new thread for every connected client
            new_thread = threading.Thread(target=self.listen_singular, args=(conn,))
            new_thread.start()


    def generate_admin_password(self) -> str:
        """
        Generate a random, 8-length password and assign it to admin_pass.\n
        Returns the created password.
        """
        for i in range(8):
            self.admin_pass += random.choice(string.ascii_letters)
        print("Password is: " + self.admin_pass)

        return self.admin_pass
    

    def get_full_name(self, conn: socket.socket) -> str:
        """
        Gets the name and ip/port of a socket and formats it to "NAME (IP, PORT)"
        """
        return str(self.socket_to_name[conn]) + " (" + str(self.socket_to_ip[conn]) + ")"


    def random_file_line(self, afile) -> str:
        """
        Gets a random line from a given file.\n
        Returns a string containing the contents of the line.
        """
        lines: list = open(afile).read().splitlines()
        myline = random.choice(lines)
        return myline

    ## Below are functions for player commands


    def add_admin(self, adding_admin: socket.socket):
        """
        Back-end handling for adding someone to the admin list.
        """
        self.administrators.append(adding_admin)
        print("Client " + self.get_full_name(adding_admin)  + " has gained admin powers.")
    

    def verify_name(self, executor: socket.socket, name: str) -> bool:
        """
        Verification that a name is valid and meets all requirements.\n
        Returns True if it passes, False if otherwise.
        """
        if name in self.socket_to_name.values():
            self.sendall_wrapper(executor, {"output": "That name is already in use."})
            return False

        if len(name) <= 3:
            self.sendall_wrapper(executor, {"output": "This name is too short."})
            return False

        return True


    def receive_name_change(self, socket: socket.socket, name: str, silent: bool = False):
        """
        Server-side handling when someone attempts to change their name.
        """
        if not name: # This happens when the client's first registering with the server
            text_name_part: str = self.random_file_line(file_locations.VERBS_STRING_FILE).capitalize() + self.random_file_line(file_locations.NOUNS_STRING_FILE).capitalize()
            
            # Fallback
            if len(text_name_part) <= 3:
                text_name_part = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
            
            name = text_name_part + str(random.randint(111, 999))

        if socket not in self.socket_to_name:
            self.socket_to_name[socket] = name
            print("New client name: " + name)
            self.sendall_wrapper(pickle_list = {"output": name + " has connected."})
            return

        print("Client formerly known as " + self.get_full_name(socket) + " has changed their name to " + name)
        if not silent:
            self.sendall_wrapper(pickle_list = {"output": self.socket_to_name[socket] + " is now known as " + name + "."})
        self.socket_to_name[socket] = name

    ## Below are functions for admin commands
    
    def ban_connection(self, conn, administrator: socket.socket) -> bool:
        """
        Ban an IP address from connecting, and force disconnect them if they are.\n
        Supports passing a string (ip address) or socket object.
        """
        if isinstance(conn, str):
            ban_file = open(file_locations.BAN_FILE, "a")
            ban_file.write(conn + "\n")
            ban_file.close()
            print(f"{conn} has been banned by {self.get_full_name(administrator)} while not connected.")
            return True

        else:            
            if conn in self.administrators: # No banning other admins!
                return False

            ban_file = open(file_locations.BAN_FILE, "a")
            ban_file.write(self.socket_to_ip[conn] + "\n")
            ban_file.close()
            try:
                filled_name = self.get_full_name(conn)
                self.handle_disconnect(conn)
                print(f"{filled_name} has been banned by {self.get_full_name(administrator)} and forcibly disconnected.")

            except:
                print(f"{conn} has been banned by {self.get_full_name(administrator)} while not connected.")

            return True
    

    def unban_connection(self, conn_ip: str, administrator: socket.socket) -> bool:
        """
        Unban an IP address, allowing them to connect again if they were banned.\n
        Only supports passing in a string (ip address).
        """
        with open(file_locations.BAN_FILE, 'r') as file:
            # read a list of lines into data
            ban_lines = file.readlines()

        try:
            ban_lines[ban_lines.index(conn_ip + "\n")] = ""
            with open(file_locations.BAN_FILE, 'w') as file:
                file.writelines(ban_lines)
            self.sendall_wrapper(administrator, {"output": "IP address unbanned."})
            print(f"{conn_ip} has been unbanned by {self.get_full_name(administrator)}.")
            return True

        except IndexError:
            self.sendall_wrapper(administrator, {"output": "IP address not found in the ban list."})
            return False

        except KeyError:
            self.sendall_wrapper(administrator, {"output": "IP address not found in the ban list."})
            return False

        except ValueError:
            self.sendall_wrapper(administrator, {"output": "IP address not found in the ban list."})
            return False

    
    def kick_connection(self, conn_ip: str, administrator: socket.socket) -> bool:
        """
        Kick an IP address from the server without banning them.\n
        Only supports passing in a string (ip address).
        """
        socket_object = None
        try:
            socket_object = list(self.socket_to_ip.keys())[list(self.socket_to_ip.values())[0].index(conn_ip)]

        except ValueError:
            pass

        if socket_object in self.administrators:
            self.sendall_wrapper(administrator, {"output": "You cannot kick an administrator."})
            return False

        self.sendall_wrapper(socket_object, {"output": "You have been kicked by an administrator."})
        self.sendall_wrapper(administrator, {"output": "User kicked successfully."})
        print(f"{self.get_full_name(socket_object)} has been kicked by {self.get_full_name(administrator)}.")
        self.handle_disconnect(socket_object)
        return True
    
    def set_motd(self, administrator: socket.socket, setting_message: str) -> bool:
        """
        Sets the on-connect message of the server.
        """
        print(f"{self.get_full_name(administrator)} has set the MOTD to \"{setting_message}\".")
        self.sendall_wrapper(administrator, {"output": "MOTD set."})
        self.message_of_the_day = setting_message


    def __init__(self):
        # Setup of IP and port
        host_input = input("Enter IP address to join (empty/invalid input will default to localhost): \n")

        if not host_input:
            self.HOST = "127.0.0.1"

        else:
            self.HOST = host_input

        port_input = input("Joining port (empty/invalid input will default to localhost): \n")

        if not port_input.isnumeric():
            self.PORT = 65432
            
        else:
            self.PORT = int(port_input)

        # Backend message handler init and related data
        self.message_handler = messageHandler.MessageHandler(self)
        os.chdir(os.path.dirname(sys.argv[0]))
        global server_class
        server_class = self

        # Initialize all the commands for clients and admins
        client_command_data = load(open(file_locations.CLIENT_COMMANDS_FILE))
        for command_name in client_command_data:
            client_command = client_commands.ClientCommand(command_name)
            client_command.admin_only = False
            self.name_to_command[client_command.name] = client_command
        
        admin_command_data = load(open(file_locations.ADMIN_COMMANDS_FILE))
        for command_name in admin_command_data:
            admin_command = admin_commands.AdminCommand(command_name)
            admin_command.admin_only = True
            self.name_to_command[admin_command.name] = admin_command
            
        # Generate the randomized admin password
        self.generate_admin_password()

        # Start the socket portion of the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as new_socket:
            new_socket.bind((self.HOST, self.PORT))
            new_socket.listen()

            # Spin up a thread for accepting new connections
            conn_thread = threading.Thread(target=self.accept_conns, args=(new_socket,))
            conn_thread.start()
            conn_thread.join()




if __name__ == "__main__":
    Server()