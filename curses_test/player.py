import physical_object
import globals

class Player(physical_object.PhysicalObject):
    
    def __init__(self):
        super().__init__("player")
        globals.screen_man.add_object_to_world(self, 1, 1)