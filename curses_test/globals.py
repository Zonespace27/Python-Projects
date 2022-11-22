from types import NoneType
import screen_manager
import player

def initialize(screen_obj):
    global main_screen
    main_screen = screen_obj

    global object_to_symbol

    object_to_symbol = {
        "player": "*",
        "wall": "#",
        "nonetype": "0"
    }

    global screen_man
    screen_man = screen_manager.ScreenManager(screen_obj)

    global player_class
    player_class = player.Player()


def get_object_symbol(object) -> str:
    if isinstance(object, NoneType):
        return object_to_symbol["nonetype"]
    return object_to_symbol[object.internal_id]