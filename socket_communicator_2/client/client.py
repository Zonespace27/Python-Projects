import constants as const
import curses
from math import trunc
import os
import pickle
import re
import socket
import string
import sys
import threading

class Client():
    """
    The reciever and sender of the server-to-client connection. \n
    When the client sends a message, the server recieves it and sends it to all other connected clients. \n
    When a client recieves a message, it adds it to the curses-based console screen, scrolling up existing text as much as needed.
    """

    def __init__(self):

        # It's very important this comes first before curses begins to mess w/ input()
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

        ### THE CURSES ZONE
        self.stdscr = curses.initscr()

        # Getting the size of the terminal
        self.y_size, self.x_size = self.stdscr.getmaxyx()

        self.main_screen = curses.newwin(self.y_size, self.x_size, 0, 0)
        curses.noecho()
        curses.curs_set(False) # Change to false to make cursor invisible
        self.main_screen.refresh()

        ### Everything else

        self.text_end = self.y_size - const.TEXTCHAT_END_POS

        # Client display name
        self.name = ""

        # Dict of text on a line + time.time() : text on a line
        # Mid rework to just be text on a line in a list
        self.line_text: list = []

        # The set of currently written out characters
        self.inputted_characters = ""

        # A string containing all valid ascii input text characters
        self.valid_characters = string.printable.replace("\n", "")

        self.add_hud()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            os.chdir(os.path.dirname(sys.argv[0]))
            sock.connect((self.HOST, self.PORT))
            listen_thread = threading.Thread(target=self.recieve_messages, args=(sock,))  
            listen_thread.start()
            # Registering with the server
            sock.sendall(pickle.dumps({"name": "", "input": ""}))

            while True:
                if self.character_act(self.main_screen.getch()):
                    sock.sendall(pickle.dumps({"input": self.inputted_characters}))
                    self.inputted_characters = ""
                    self.update_input_box()


    def recieve_messages(self, socket_class: socket.socket):
        """
        A method that's called on a seperate thread, will always listen for messages from the server and insert them onto the screen.
        """
        while True:
            try:
                data = socket_class.recv(4096)
                
            except ConnectionResetError:
                print("Server disconnected.")
                return

            data = pickle.loads(data)
            sanitized_data = re.sub("\'|b\'|\"|b\"|\\n", "", data["output"])

            self.line_text_multiline_check(((data["name"] + ": ") if ("name" in data.keys()) else "") + sanitized_data + "\n")
            
            self.main_screen.refresh()


    def line_text_multiline_check(self, text_to_check: str) -> list:
        """
        Slightly misleading name. Adds calls add_line_text after checking
        if the text wouldn't fit in one line, and splits it out into multiple messages if so.
        """
        list_of_lines = []
        if len(text_to_check) > self.x_size:
            line_count = trunc(len(text_to_check) / self.x_size)

            for i in range(line_count):
                sliced_text = text_to_check[(self.x_size * i):(self.x_size * min(i + 1, line_count))] # Slices the string within certain bounds determined by line count
                list_of_lines.append(sliced_text)
                self.add_line_text(sliced_text)
            
            # For anything that was rounded off
            sliced_text = text_to_check[(line_count * self.x_size):]
            list_of_lines.append(sliced_text)
            self.add_line_text(sliced_text)
        
        else:
            list_of_lines.append(text_to_check)
            self.add_line_text(text_to_check)
        
        return list_of_lines


    def add_line_text(self, text_to_add: str):
        """
        Adds text to the screen, in addition to adding it to the `line_text` list with a timestamp. \n
        Do not call over `line_text_multiline_check`.
        """
        #unix_stamp_text = f"{text_to_add} {str(time.time())}"
        self.line_text.append(text_to_add)
        if len(self.line_text) > self.text_end:
            self.move_up_lines(1)

        else:
            self.main_screen.addstr(*self.get_yx(self.y_size - self.line_text.index(text_to_add), 0), text_to_add) # The "*" is used for unpacking a tuple into two sequential entries
            
        self.main_screen.refresh()
    

    def move_up_lines(self, move_amount: int):
        """
        Move up the lines on the screen by `move_amount` lines.
        Moved messages are currently entirely deleted.
        """
        #line_text_keys = list(self.line_text.keys())
        #line_text_values = list(self.line_text.values())
        #line_text_keys = line_text_keys[move_amount:] 
        #line_text_values = line_text_values[move_amount:]

        #copy_line_text = self.line_text.copy()[move_amount:]

        self.line_text = self.line_text[move_amount:]
        #for key in copy_line_text:
        #    self.line_text[key] = line_text_values[line_text_keys.index(key)] 
        
        for string in self.line_text:
            self.main_screen.addstr(*self.get_yx(self.y_size - self.line_text.index(string), 0), string) # Newest at bottom, oldest at top

        self.main_screen.refresh()
    

    def add_hud(self, add_messages: bool = False):
        """
        Add all the hud elements to the client. Does not add messages by default (make `add_messages` True) and doesn't clear screen by default.
        """
        for i in range(self.x_size):
            self.main_screen.addch(*self.get_yx(const.BOTTOM_HUDLINE_POS, i), "#")

        self.main_screen.addch(*self.get_yx(const.INPUTLINE_BORDER1_POS, 1), "#")
        self.main_screen.addch(*self.get_yx(const.INPUTLINE_BORDER2_POS, 1), "#")

        for i in range(self.x_size):
            self.main_screen.addch(*self.get_yx(const.BOTTOM_INPUTLINE_POS, i), "#")

        self.main_screen.move(*self.get_yx(const.CURSOR_POS, 0))
        
        # Please clear screen prior to calling with add_messages as True
        if add_messages:
            copy_list = self.line_text.copy()
            self.line_text = []
            for entry in copy_list:
                self.add_line_text(entry)
    

    # Returning True means the message will attempt to send
    def character_act(self, character: str) -> bool:
        """
        Does an action based on client character input. \n
        Due to the shortcomings of `getstr()`, `getch()` is used instead.
        As such, we need to do per-character handling, which this function does.
        """
        # If it's text, handle it early
        ascii_char = chr(character)
        try:
            if self.valid_characters.index(ascii_char) or ascii_char == "0":
                if len(self.inputted_characters) >= (self.x_size * const.INPUT_LINE_AMT):
                    return False

                self.inputted_characters += ascii_char
                self.update_input_box()
                return False

        except ValueError:
            if ascii_char == "\n":
                return True
            
            elif ascii_char == "\x08":
                self.inputted_characters = self.inputted_characters[:(len(self.inputted_characters) - 1)]
                self.update_input_box(rewrite_hud = True)
                return False
            
            return False


    def update_input_box(self, rewrite_hud: bool = False):
        """
        Updates the text in the input box by calling `add_input_box_text()` when appropriate. \n
        If `rewrite_hud` is True or the `inputted_characters` string is empty, then the input box will be cleared.
        """
        if (self.inputted_characters == "") or rewrite_hud:
            self.main_screen.move(*self.get_yx(const.CURSOR_POS, 0))
            self.main_screen.clrtoeol()
            self.main_screen.move(*self.get_yx(const.CURSOR_POS - 1, 0))
            self.main_screen.clrtoeol()
            self.add_hud()

            if self.inputted_characters != "":
                self.add_input_box_text()

            return

        self.add_input_box_text()
        self.main_screen.refresh()
    
    def add_input_box_text(self):
        """
        Adds the inputted-but-not-sent text for the client to the text box.
        """
        line_count: int = trunc(len(self.inputted_characters) / (self.x_size - const.INPUT_LINE_RIGHT_CUTOFF_POS)) + 1
        
        if len(self.inputted_characters):
            if line_count > const.INPUT_LINE_AMT: # Just in case they bypassed the cap anyway
                line_count = const.INPUT_LINE_AMT
                self.inputted_characters[:((self.x_size - const.INPUT_LINE_RIGHT_CUTOFF_POS) * const.INPUT_LINE_AMT)]

        for i in range(line_count):
            const_to_use: int = None
            
            if i == 0:
                const_to_use = const.INPUTLINE_BORDER2_POS

            elif i == 1:
                const_to_use = const.INPUTLINE_BORDER1_POS

            self.main_screen.addstr(*self.get_yx(const_to_use, 0), self.inputted_characters[max((self.x_size - const.INPUT_LINE_RIGHT_CUTOFF_POS) * i, 0):((self.x_size - const.INPUT_LINE_RIGHT_CUTOFF_POS) * (i + 1))])

    def get_yx(self, y_coord: int = None, x_coord: int = None) -> tuple:
        """
        Gets y/x coords from two offsets. Defaults to 0/0 if the appropriate args aren't passed.\n
        Returns a tuple of the y and x coords.
        """
        if not y_coord:
            y_coord = self.y_size
        
        if not x_coord:
            x_coord = self.x_size
        
        return self.y_size - y_coord, self.x_size - x_coord

if __name__ == "__main__":
    # Required because curses modifies the terminal, and we want it to close gracefully if an exception occurs
    # While wrapper() does this, it functions inconsistently with threading, so we're using the manual method instead
    try:
        Client()
    except:
        curses.curs_set(True)
        curses.echo()
        curses.endwin()