from exec import Exec
import re
import threading
import time

class MessageHandler():
    """
    The class for handling all the server's messages. \n
    When the server recieves a message, it inserts it into the message handler's queue. 
    Every 0.1 seconds, it processes the queue, which will broadcast each unsent message to all connected clients after handling commands. \n
    While this method does induce a <=0.1s delay to all messages, testing has shown that it's imperceptable to users.
    """
    message_queue = []

    server = None

    def __init__(self, server_reference):
        self.server = server_reference

        new_thread = threading.Thread(target=self.begin_handling_loop)
        new_thread.start()
    
    def begin_handling_loop(self):
        """
        Takes a look at the list of accumulated messages every 1/10th of a second and cleans them all out
        """
        while True:
            time.sleep(0.1)
            if self.message_queue: # checking for the list instead of letting it `for` over an empty list seems to save about 30ns per loop, which is a "lot" when we're doing this 10x a second
                self.handle_queue()

    def handle_queue(self):
        """
        Iterate over every message in the queue, split out the commands from the messages.\n
        If it's a command, execute it and don't tell other clients.\n
        If it's a message, send it to all other clients.
        """
        for data in self.message_queue:
            name = data.get("name")
            conn = data.get("connection")
            if conn not in self.server.socket_to_name:
                self.server.recieve_name_change(conn, name)

            name = self.server.socket_to_name[conn]
            # TODO: document regex more
            input_data = data.get("input")
            if(isinstance(input_data, bytes)):
                input_data = input_data.decode()
            text = re.sub("\'|b\'|\"|b\"", "", input_data)

            if len(text) <= 0:
                self.message_queue.remove(data)
                continue
                
            if text[0] == "/":
                regex_locate = re.search(" ", text)

                if regex_locate == None:
                    argument = ""
                    first_space_position = len(text)

                else:
                    first_space_position = text.find(" ")
                    argument = text[first_space_position + 1:]

                # Client command handling
                if text[1:first_space_position] in self.server.name_to_command:
                    gotten_command = self.server.name_to_command.get(text[1:first_space_position])
                    if gotten_command == None:
                        print("Invalid command.")
                        self.message_queue.remove(data)
                        continue
                    try:
                        print(self.server.get_full_name(conn) + " executed command: " + gotten_command.name)
                        
                    except ValueError:
                        print("An unexpectedly disconnected client unsuccessfully executed command: " + gotten_command.name)
                        self.message_queue.remove(data)
                        continue                        
                    Exec(gotten_command.on_exec, {}, {"executor": conn, "server_class": self.server, "argument": argument})
                    self.message_queue.remove(data)
                    continue
                
                elif text[0] == "/":
                    self.server.sendall_wrapper(conn, {"output": "Invalid command."})
                    self.message_queue.remove(data)
                    continue
                            
            try:
                print(f"Recieved: {text} || from {self.server.get_full_name(conn)}")
                pickle_list = {"name": name, "output": text}
                for connection in self.server.all_connections:
                    self.server.sendall_wrapper(connection, pickle_list)
                
                self.message_queue.remove(data)

            except KeyError:
                # Considering we *can't* check if there's a name attached, we just don't send it
                print(f"Recieved: {text} || from an unexpectedly disconnected client.")

    
    def add_message(self, message_to_add: str):
        """
        Add a string to the message queue.
        """
        self.message_queue.append(message_to_add)