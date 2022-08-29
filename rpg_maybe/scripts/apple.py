
def eat_verb(self, player_class, object_class):
    print('You eat the apple.')
    player_class.adjust_health(5)
    if object_class in player_class.inventory:
        player_class.inventory.remove(object_class)

# print('You eat the apple.')\nplayer_class.adjust_health(5)\ndel object_class