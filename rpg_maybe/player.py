import re
from os import system
import globals
import object as object_module
import exec

class Player():
    health = 50
    max_health = 100
    inventory = []
    current_room = -1 # ID-based
    self_verbs = {
        "check": ["health", "backpack", "inventory"],
        "look": ["room", "around"],
        "examine": ["room", "around"]
    }
    last_used_door = None
    dead = False


    def __init__(self):
        # Must be in init to prevent immediate runtiming
        self.self_verb_actions = {
            "check_health": globals.self_health_check,
            "check_backpack": globals.self_inventory_check,
            "check_inventory": globals.self_inventory_check,
            "look_room": globals.self_room_check,
            "look_around": globals.self_room_check,
            "examine_room": globals.self_room_check,
            "examine_around": globals.self_room_check,
        }

    def take_input(self):
        if self.dead == True:
            return
        self.parse_string(input("What would you like to do?\n"))
        system('cls')

    def parse_string(self, input_text):
        santized_text = re.sub(r"\b(and|a|or|the|an|is|at|to)\b", "", input_text, 0, re.IGNORECASE)
        words = re.findall(r"\S+", santized_text)
        if len(words) <= 0:
            print("No words found")
            self.take_input()
            return
        object = None
        room_class = globals.id_to_room[self.current_room]
        maybe_selector = re.findall(r"\(\d\)", words[len(words) - 1])
        the_digit = -1
        if len(words) <= 1:
            print("Not enough words")
            return self.take_input()
        if len(maybe_selector) != 0:
            the_digit = int(re.findall(r"\d", maybe_selector[0])[0]) # Error: Doesn't work with > 10 of the same object in the room
            object = words[len(words) - 2]
        else:
            if len(words) > 1:
                object = words[len(words) - 1]
        verb = ""
        exclusion_num = 2 if len(maybe_selector) != 0 else 1
        for word in words:
            if word == words[len(words) - exclusion_num] or word == words[len(words) - 1]: # THE TECHNICAL DEBT GROWS
                continue
            verb += word.lower()
            #verb += ' ' if word != words[len(words) - 2] else ''
        verb = verb.lower()
        object = object.lower()
        # Priority: Self verbs, inventory item verbs, room (objects in it) verbs
        if verb in self.self_verbs:
            if object in self.self_verbs[verb]:
                exec.Exec(self.self_verb_actions[verb + "_" + object], {}, {"player_class": self})
                return self.take_input()
        for inv_obj in self.inventory:
            if object == inv_obj.name.lower():
                if the_digit != -1:
                    if inv_obj.assignment_number != the_digit:
                        continue
                for default_verb in globals.default_obj_verbs:
                    if re.search(r'\b' + verb + r'\b', default_verb):
                        if verb == "take": # unfucken later
                            continue
                        if isinstance(inv_obj, object_module.Object):
                            exec.Exec(globals.default_obj_verbs[verb], {}, {"player_class": self, "object_class": inv_obj})
                            return self.take_input()
                        else:
                            print("One of those doesn't seem to exist.")
                        break
                for verb_obj in inv_obj.verbs:
                    if verb.find(verb_obj) != -1:
                        exec.Exec(inv_obj.verbs[verb_obj], {}, {"player_class": self, "object_class": inv_obj})
                        return self.take_input()
        for room_obj in room_class.all_things:
            if object == room_obj.name.lower():
                if the_digit != -1:
                    if room_obj.assignment_number != the_digit:
                        continue
                for default_verb in globals.default_obj_verbs:
                    if re.search(r'\b' + verb + r'\b', default_verb):
                        if isinstance(room_obj, object_module.Object):
                            exec.Exec(globals.default_obj_verbs[verb], {}, {"player_class": self, "object_class": room_obj})
                            return self.take_input()
                        else:
                            print("One of those doesn't seem to exist.")
                        break
                if isinstance(room_obj, object_module.Item):
                    if room_obj not in self.inventory:
                        print("You need to hold the item to interact with it.")
                        break
                for verb_room in room_obj.verbs:
                    if verb.find(verb_room) != -1:
                        exec.Exec(room_obj.verbs[verb_room], {}, {"player_class": self, "object_class": room_obj})
                        return self.take_input()
                

        self.take_input()
    
    def adjust_health(self, amount):
        self.health = max(0, min(self.max_health, self.health + amount))
        if self.health <= 0:
            self.process_death()
        return self.health
    
    def process_death(self):
        self.dead = True
        print("You have died!")
    
    def add_to_inventory(self, item_class):
        current_room = globals.id_to_room[self.current_room]
        self.inventory.append(item_class)
        current_room.remove_item(item_class)
    
    def remove_from_inventory(self, item_class):
        current_room = globals.id_to_room[self.current_room]
        self.inventory.remove(item_class)
        current_room.add_item(item_class)
    
    def unique_id_list(self):
        compiled_list = []
        for item in self.inventory:
            compiled_list.append(item.unique_id)
        return compiled_list