import threading
import curses
import physical_object
import globals
import constants as const

class ScreenManager():

    def __init__(self, screen_object):
        self.screen_class = screen_object
        curses.noecho()
        self.coordinate_contents = []
        
        self.rows, self.columns = screen_object.getmaxyx() #on my laptop i get rows 18, columns 157
        # The below two lines are needed; the program ERRs otherwise
        self.rows -= 1
        self.columns -= 2

        for i in range(self.rows * self.columns):
            self.coordinate_contents.append([])       

        for row in range(self.rows):
            for column in range(self.columns):
                screen_object.addstr(row, column, "0")

        new_thread = threading.Thread(target=self.take_player_movement)#, args=())
        new_thread.start()
        self.screen_class.refresh()

    def get_coordinate_list(self, row, column) -> list:
        return self.coordinate_contents[(row * 10) + column]
    
    # For getting an object symbol after deciding the object priority of a tile
    def object_symbol_reset_priority(self, row, column):
        return globals.get_object_symbol(self.decide_object_priority(self.get_coordinate_list(row, column)))

    # If a coordinate set has a dense object, preventing movement
    def tile_has_dense_object(self, row, column) -> bool:
        for object in self.get_coordinate_list(row, column):
            if object.dense:
                return True
        return False

    # For adding an ALREADY CREATED object to the world
    def add_object_to_world(self, object_class, row, column):
        if not isinstance(object_class, physical_object.PhysicalObject):
            raise RuntimeError("add_object_to_world tried to add a non-physical object to the world! (Got " + str(object_class.__class__) + ")")
        self.get_coordinate_list(row, column).append(object_class)
        object_class.coordinates = [row, column]
        self.add_to_screen(row, column, self.object_symbol_reset_priority(row, column))


    # For deciding what object should be shown on a tile. If it's all equal layer priority objects, it relies on the first object in the list
    def decide_object_priority(self, object_list) -> physical_object.PhysicalObject:
        if len(object_list) == 0:
            return None
        highest_priority_object = object_list[0]
        for phys_object in object_list:
            if phys_object.layer_priority <= highest_priority_object.layer_priority:
                continue
            highest_priority_object = phys_object
        return highest_priority_object

    # For adding to the screen with a refresh. Don't use for everything
    def add_to_screen(self, row, column, string):
        self.screen_class.addstr(row, column, string)
        self.screen_class.refresh()
    
    # Move an object from their current coords to the new coords
    def move_from_to(self, object_to_move, move_row, move_column) -> bool:
        if (move_row < 0) or (move_column < 0):
            return False
        if (move_row > (const.MAXIMUM_INTENDED_ROWS - 1)) or (move_column > (const.MAXIMUM_INTENDED_COLUMNS - 1)):
            return False
        if self.tile_has_dense_object(move_row, move_column):
            return False
        self.get_coordinate_list(object_to_move.coordinates[0], object_to_move.coordinates[1]).remove(object_to_move)
        self.screen_class.addstr(object_to_move.coordinates[0], object_to_move.coordinates[1], self.object_symbol_reset_priority(object_to_move.coordinates[0], object_to_move.coordinates[1]))
        self.get_coordinate_list(move_row, move_column).append(object_to_move)
        object_to_move.coordinates = [move_row, move_column]
        self.add_to_screen(move_row, move_column, globals.get_object_symbol(object_to_move))
        return True

    def take_player_movement(self):
        while(True):
            inputted_character = chr(self.screen_class.getch())
            if inputted_character == "w":
                self.move_from_to(globals.player_class, globals.player_class.coordinates[0] - 1, globals.player_class.coordinates[1])
            elif inputted_character == "a":
                self.move_from_to(globals.player_class, globals.player_class.coordinates[0], globals.player_class.coordinates[1] - 1)
            elif inputted_character == "s":
                self.move_from_to(globals.player_class, globals.player_class.coordinates[0] + 1, globals.player_class.coordinates[1])
            elif inputted_character == "d":
                self.move_from_to(globals.player_class, globals.player_class.coordinates[0], globals.player_class.coordinates[1] + 1)
            elif inputted_character == "e":
                self.add_object_to_world(physical_object.PhysicalObject("wall"), globals.player_class.coordinates[0], globals.player_class.coordinates[1])