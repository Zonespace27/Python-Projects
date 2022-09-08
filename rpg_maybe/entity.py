from json import load
import globals

class Entity():
    json_location = 'rpg_maybe/json/entities.json'

    def __init__(self, entity_name):
        data = load(open(self.json_location))
        self.__dict__ = data[entity_name]
        self.health = self.max_health
        # should not ever change
        self.original_name = self.name
        # Do not depend on this for data storage, can change on a dime
        self.temporary_name = self.name
        self.assignment_number = -1
        globals.make_random_id(self)
        self.verbs["attack"] = globals.attack_entity
    
    def on_attack(self, player_class, damage_amount = 0):
        self.health -= damage_amount
        if self.health <= 0:
            self.on_death()
        print("You attack " + self.name + " with " + player_class.equipped_weapon + ".")
    
    def on_death(self):
        pass

class Hostile(Entity):
    json_location = 'rpg_maybe/json/enemies.json'