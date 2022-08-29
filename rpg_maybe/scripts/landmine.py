def do_explode(self, player_class, object_class):
    print("The landmine goes boom.")
    player_class.adjust_health(-10)
    print(player_class)


# "print('The landmine goes boom.')\nplayer_class.adjust_health(-10)\nprint(player_class.health)\ndel self"