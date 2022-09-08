def do_explode(self, player_class, object_class):
    import globals
    print('The landmine explodes in your face!')
    player_class.adjust_health(-50)
    current_room = globals.id_to_room[player_class.current_room]
    current_room.remove_object(object_class)

# import globals\nprint('The landmine explodes in your face!')\nplayer_class.adjust_health(-50)\ncurrent_room = globals.id_to_room[player_class.current_room]\ncurrent_room.remove_object(object_class)
