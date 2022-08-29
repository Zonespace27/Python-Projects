import object
import room_manager
import player
import room
import globals

# Initializations
def init_game():
    print("World starting")
    globals.initialize()
    globals.player_class = player.Player()
    globals.manager = room_manager.Room_Manager()
    print("World started")
    globals.manager.move_room(0) # hardcoded to start in room 0, sue me.
    globals.player_class.take_input()


if __name__ == "__main__":
    init_game()
