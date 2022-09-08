from json import load
import exec
import globals

# A thing you can hold, interact with, whatever.
class Object():
    name = ""
    desc = ""
    json_location = 'rpg_maybe/json/objects.json'

    def __init__(self, obj_name):
        data = load(open(self.json_location))
        self.__dict__ = data[obj_name]
        # should not ever change
        self.original_name = self.name
        # Do not depend on this for data storage, can change on a dime
        self.temporary_name = self.name
        self.assignment_number = -1
        globals.make_random_id(self)
    
    # What the object performs when you enter the room (besides description)
    def do_enter(self, player_class):
        exec.Exec(self.on_enter, {}, {"player_class": player_class, "object_class": self})
            

# Subclass, only objects you can hold and store
class Item(Object):
    name = "Item Parent"
    desc = "Use your imagination!"
    verbs = {}
    json_location = 'rpg_maybe/json/items.json'

# Subclass of a subclass, used for things that you can use as melee weaponry
class Weapon(Item):
    name = "Weapon Parent"
    desc = "Use your imagination!"
    json_location = 'rpg_maybe/json/weapons.json'

#if __name__ == "__main__":
#    y = player.Player()
#    x = Object('Landmine')
#    x.do_enter(y)
