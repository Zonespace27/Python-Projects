import socket
import threading
import random
import os
import sys
import re
import pickle
import colorama
import termcolor
import file_locations_client as file_locations
import string

class Client():
    def random_line(self, afile):
        lines = open(afile).read().splitlines()
        myline = random.choice(lines)
        return myline

    def recieve_messages(self, socket_class):
        while True:
            try:
                data = socket_class.recv(1024)
            except ConnectionResetError:
                print("Server disconnected.")
                return
            data = pickle.loads(data)
            sanitized_data = re.sub("\'|b\'|\"|b\"", "", data["output"])
            if "color" in data.keys() and data["color"] != "none":
                print(((termcolor.colored(data["name"], data["color"]) + ": ") if ("name" in data.keys()) else "") + sanitized_data + "\n")
            else:
                print(((data["name"] + ": ") if ("name" in data.keys()) else "") + sanitized_data + "\n")

    def __init__(self):
        self.HOST = input("Enter IP address to join: \n")
        self.PORT = int(input("Joining port: \n"))

        # Client display name
        self.name = ""

        colorama.init(autoreset=True)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            os.chdir(os.path.dirname(sys.argv[0]))
            s.connect((self.HOST, self.PORT))
            text_name_part = self.random_line(file_locations.VERBS_STRING_FILE).capitalize() + self.random_line(file_locations.NOUNS_STRING_FILE).capitalize()
            if len(text_name_part) <= 3:
                text_name_part = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
            name = text_name_part + str(random.randint(111, 999))
            listen_thread = threading.Thread(target=self.recieve_messages, args=(s,))  
            listen_thread.start()
            # Registering with the server
            pickle_dict = {"name": name, "input": ""}
            s.sendall(pickle.dumps(pickle_dict))

            while True:
                sent_input = input("")
                pickle_dict = {"name": name, "input": sent_input}
                s.sendall(pickle.dumps(pickle_dict))

if __name__ == "__main__":
    Client()