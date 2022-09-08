def drop_object(self, player_class, object_class):
    import globals
    current_room = globals.id_to_room[player_class.current_room]
    if object_class not in current_room.items and object_class not in current_room.objects:
        player_class.remove_from_inventory(object_class)
        print('You drop ' + object_class.name + '.')
    else:
        print('You do not seem to have any of that.')

# import globals\nimport object\ncurrent_room = globals.id_to_room[player_class.current_room]\nif object_class not in current_room.items and object_class not in current_room.objects:\n\tplayer_class.inventory.remove(object_class)\n\tif isinstance(object_class, object.Item):\n\t\tcurrent_room.items.append(object_class)\n\telse:\n\t\tcurrent_room.objects.append(object_class)\n\tcurrent_room.all_things.append(object_class)\n\tprint('You drop ' + object_class.name + '.')\nelse:\n\tprint('You do not seem to have any of that.')

def take_object(self, player_class, object_class):
    import object
    import exec
    if object_class in player_class.inventory:
        print('There do not seem to be any of those around.')
        raise exec.ExecInterrupt
    if not isinstance(object_class, object.Item):
        print('You cannot pick this up.')
        raise exec.ExecInterrupt
    player_class.add_to_inventory(object_class)
    print('You pick up ' + object_class.name + ', putting it into your backpack.')

# import object\nimport exec\nif object_class in player_class.inventory:\n\tprint('There do not seem to be any of those around.')\n\traise exec.ExecInterrupt\nif not isinstance(object_class, object.Item):\n\tprint('You cannot pick this up.')\n\traise exec.ExecInterrupt\nplayer_class.add_to_inventory(object_class)\nprint('You pick up ' + object_class.name + ', putting it into your backpack.')

def examine_object(self, player_class, object_class):
    if hasattr(object_class, 'extended_desc'):
        print(object_class.extended_desc)
    else:
        print('You cannot see anything remarkable about this.')

# if hasattr(object_class, 'extended_desc'):\n\tprint(object_class.extended_desc)\nelse:\n\tprint('You cannot see anything remarkable about this.')
