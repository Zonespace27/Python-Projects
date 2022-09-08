# Self-player verb/object combos

def check_health(self, player_class):
    print('You look over your body, getting the feeling your health is ' + str(player_class.health) + '.')

# print('You look over your body, getting the feeling your health is ' + str(player_class.health) + '.')

def check_inventory(self, player_class):
    compiled_string = ''
    for object in player_class.inventory:
        if player_class.inventory.index(object) == len(player_class.inventory) - 1:
            compiled_string += object.name + '.'
            continue
        compiled_string += object.name + ', '
    if len(player_class.inventory) == 0:
        compiled_string = 'nothing at all.'
    print('You look into your backpack, spotting: ' + compiled_string)

# compiled_string = ''\nfor object in player_class.inventory:\n\tif player_class.inventory.index(object) == len(player_class.inventory) - 1:\n\t\tcompiled_string += object.name + '.'\n\t\tcontinue\n\tcompiled_string += object.name + ', '\nif len(player_class.inventory) == 0:\n\tcompiled_string = 'nothing at all.'\nprint('You look into your backpack, spotting: ' + compiled_string)

def look_around(self, player_class):
    import globals
    the_room = globals.id_to_room[player_class.current_room]
    the_room.room_examine()

# import globals\nthe_room = globals.id_to_room[player_class.current_room]\nthe_room.room_examine()
