def eat_apple(self, player_class, object_class):
    print('You eat the apple. You feel a bit refreshed.')
    player_class.adjust_health(5)
    player_class.inventory.remove(object_class)

# print('You eat the apple. You feel a bit refreshed.')\nplayer_class.adjust_health(5)\nplayer_class.inventory.remove(object_class)

def eat_orange(self, player_class, object_class):
    print('You eat the orange. You do not feel much better, though.')
    player_class.inventory.remove(object_class) # fuck youuuuu it's not an apple

# print('You eat the orange. You do not feel much better, though.')\nplayer_class.inventory.remove(object_class)

def drink_exp_potion(self, player_class, object_class):
    print('You drink the potion, gaining some experience.')
    player_class.add_exp(10)
    player_class.inventory.remove(object_class)

# print('You drink the potion, gaining some experience.')\nplayer_class.add_exp(10)\nplayer_class.inventory.remove(object_class)