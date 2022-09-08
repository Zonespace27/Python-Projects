def enter_door(self, player_class, object_class):
    import globals
    print('You go through the door.')
    player_class.last_used_door = object_class.matching_door
    globals.manager.move_room(object_class.matching_door.in_room)

# import globals\nprint('You go through the door.')\nplayer_class.last_used_door = object_class.matching_door\nglobals.manager.move_room(object_class.matching_door.in_room)
