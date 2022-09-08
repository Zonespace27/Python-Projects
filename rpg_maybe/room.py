from functools import cache
from json import load
import object
import globals
import exec

# Basic, un-inherited room (not that you should need to make a child of it)
class Room():
    desc = ""
    json_location = 'rpg_maybe/json/rooms.json'

    def __init__(self, room_name):
        data = load(open(self.json_location))
        self.__dict__ = data[room_name]
        self.id = globals.max_room_id
        if(self.id in globals.id_to_room):
            raise ValueError("Room ID" + self.id + "already exists in id_to_room, but another tried to override it!")
        globals.id_to_room[self.id] = self
        globals.max_room_id += 1
        self.objects = []
        self.items = []
        self.entities = []
        self.enemies = []
        self.all_things = []
        self.grid_coordinates = []
        for obj_name in self.pre_objects:
            obj_class = object.Object(obj_name)
            self.add_object(obj_class)
        for item_name in self.pre_items:
            self.add_item(object.Item(item_name))

    def on_enter(self, player_class):
        self.room_examine()
        for object in self.all_things:
            if hasattr(object, "on_enter"): # the on/do enter difference is intentional
                object.do_enter(player_class)

    
    def room_examine(self):
        print(self.desc)
        cached_descriptions = {}
        self.recalculate_temporary_assignment(self.all_things)
        for object in self.all_things:
            add_str = ""
            if object.desc in cached_descriptions:
                cached_descriptions[object.desc] += 1
                add_str += " (" + str(cached_descriptions[object.desc]) + ")"
            else:
                cached_descriptions[object.desc] = 0
            if object.original_name == "Door": # This shit is hardcoded sin but I'm too drained to think of anything better
                if globals.player_class.last_used_door == object:
                    add_str += " This was the door you came from."
            print(object.desc + add_str)

    
    def add_item(self, item_class):
        self.objects.append(item_class)
        self.items.append(item_class)
        self.all_things.append(item_class)
        self.recalculate_temporary_assignment(self.all_things)

    def add_object(self, object_class):
        self.objects.append(object_class)
        self.all_things.append(object_class)
        self.recalculate_temporary_assignment(self.all_things)
    
    def add_entity(self, entity_class):
        self.entities.append(entity_class)
        self.all_things.append(entity_class)
        self.recalculate_temporary_assignment(self.all_things)
    
    def add_enemy(self, enemy_class):
        self.entities.append(enemy_class)
        self.enemies.append(enemy_class)
        self.all_things.append(enemy_class)
        self.recalculate_temporary_assignment(self.all_things)
    
    def remove_enemy(self, enemy_class):
        self.entities.remove(enemy_class)
        self.enemies.remove(enemy_class)
        self.all_things.remove(enemy_class)
        self.recalculate_temporary_assignment(self.all_things)

    def remove_entity(self, entity_class):
        self.entities.remove(entity_class)
        self.all_things.remove(entity_class)
        self.recalculate_temporary_assignment(self.all_things)

    def remove_item(self, item_class):
        self.objects.remove(item_class)
        self.items.remove(item_class)
        self.all_things.remove(item_class)
        self.recalculate_temporary_assignment(self.all_things)

    def remove_object(self, object_class):
        self.objects.remove(object_class)
        self.all_things.remove(object_class)
        self.recalculate_temporary_assignment(self.all_things)

    # Depreciated, remove later when there's definitely nothing to recover from this
    def recalc_temp_names(self, list_to_recalc):
        amount_list = globals.object_amounts(list_to_recalc)
        for thing in list_to_recalc:
            if amount_list[thing.name] != 0:
                thing.temporary_name = thing.name + " (" + str(amount_list[thing.name]) + ")"
                thing.assignment_number = amount_list[thing.name]
                amount_list[thing.name] -= 1
            else:
                thing.temporary_name = thing.name
                thing.assignment_number = -1
    
    def recalculate_temporary_assignment(self, obj_list):
        cached_list = {}
        for thing in obj_list:
            if thing.original_name in cached_list:
                cached_list[thing.original_name] += 1
                thing.assignment_number = cached_list[thing.original_name]
                thing.temporary_name = thing.name + " (" + str(cached_list[thing.original_name]) + ")"
            else:
                cached_list[thing.original_name] = 0
                thing.assignment_number = -1
                thing.temporary_name = thing.name
        return cached_list