
def initialize():

    # Player globals

    global player_class

    # Class that contains the player
    player_class = 0

    # Room globals

    global max_room_id
    global id_to_room
    global manager

    # Maximum current room ID num, will tick up as more rooms are created
    max_room_id = 0
    # Dictionary of ID : Room
    id_to_room = {}
    # Room manager class
    manager = 0

    # Object globals

    global default_drop_verb
    global default_take_verb
    global default_examine_verb

    # The one-line code for dropping objects (scripts/default_obj.py)
    default_drop_verb = "import globals\nimport object\ncurrent_room = globals.id_to_room[player_class.current_room]\nif object_class not in current_room.items and object_class not in current_room.objects:\n\tplayer_class.inventory.remove(object_class)\n\tif isinstance(object_class, object.Item):\n\t\tcurrent_room.items.append(object_class)\n\telse:\n\t\tcurrent_room.objects.append(object_class)\n\tcurrent_room.all_things.append(object_class)\n\tprint('You drop ' + object_class.name + '.')\nelse:\n\tprint('You do not seem to have any of that.')"
    # The code for picking up objects (scripts/default_obj.py)
    default_take_verb = "import object\nimport exec\nif object_class in player_class.inventory:\n\tprint('There do not seem to be any of those around.')\n\traise exec.ExecInterrupt\nif not isinstance(object_class, object.Item):\n\tprint('You cannot pick this up.')\n\traise exec.ExecInterrupt\nplayer_class.add_to_inventory(object_class)\nprint('You pick up ' + object_class.name + ', putting it into your backpack.')"
    # Code for close-examining objects (scripts/default_obj.py)
    default_examine_verb = "if hasattr(object_class, 'extended_desc'):\n\tprint(object_class.extended_desc)\nelse:\n\tprint('You cannot see anything remarkable about this.')"

    global default_obj_verbs
    # Verbs that apply to all objects
    default_obj_verbs = {
        # Dropping
        "drop": default_drop_verb,
        "remove": default_drop_verb,
        # Taking
        "take": default_take_verb,
        "grab": default_take_verb,
        "obtain": default_take_verb,
        "pick up": default_take_verb,
        # Examine
        "examine": default_examine_verb,
        "look": default_examine_verb,
    }
    
    # Self globals

    global self_inventory_check
    global self_health_check
    global self_room_check

    # Verb for checking your backpack
    self_inventory_check = "compiled_string = ''\nfor object in player_class.inventory:\n\tif player_class.inventory.index(object) == len(player_class.inventory) - 1:\n\t\tcompiled_string += object.name + '.'\n\t\tcontinue\n\tcompiled_string += object.name + ', '\nif len(player_class.inventory) == 0:\n\tcompiled_string = 'nothing at all.'\nprint('You look into your backpack, spotting: ' + compiled_string)"
    # Verb for checking your health
    self_health_check = "print('You look over your body, getting the feeling your health is ' + str(player_class.health) + '.')"
    # Verb for re-checking the room you're in
    self_room_check = "import globals\nthe_room = globals.id_to_room[player_class.current_room]\nthe_room.room_examine()"

    # Entity globals
    
    global attack_entity

    # Verb for attacking enemies
    attack_entity = ""

def object_amounts(the_list):
    cached_names = {}
    for object in the_list:
        if object.original_name in cached_names:
            cached_names[object.original_name] += 1
            continue
        cached_names[object.original_name] = 0
    return cached_names

def make_random_id(to_id):
    from random import randint
    to_id.unique_id = ""
    for i in range(8): # probably a safe number
        to_id.unique_id += str(randint(0, 9))
    to_id.unique_id = int(to_id.unique_id)
