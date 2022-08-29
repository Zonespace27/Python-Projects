from sqlite3 import connect
import room
import primary
import globals
import random
import object

class Room_Manager():
    # Rooms to create ontop of the base one
    rooms_to_create = 20
    rand_room_list = ['Debug', 'Debug2']
    directions = ["North", "East", "South", "West"]
    # [X, Y]
    grid = []
    selected_grid_tile = [0, 0]

    def __init__(self):
        start_room = room.Room('Start')
        self.add_to_grid([0, 0], start_room)

        for i in range(self.rooms_to_create):
            chosen_room = random.choice(self.rand_room_list)
            for room_thing in globals.id_to_room:
                room_thing_actual = globals.id_to_room[room_thing]
                if self.selected_grid_tile == room_thing_actual.grid_coordinates:
                    from_room = room_thing_actual
            allowed_directions = []
            # Finding directions that are valid
            for dir in self.directions:
                check_tile = self.selected_grid_tile.copy()
                check_tile = self.take_step(check_tile, dir)
                if check_tile not in self.grid:
                    allowed_directions.append(dir)
            if len(allowed_directions) == 0:
                raise ValueError("Room manager had no directions to make a room! (Iter " + str(i) + " out of " + str(self.rooms_to_create) + ")")
            chosen_dir = random.choice(allowed_directions)
            self.take_step(self.selected_grid_tile, chosen_dir)
            for room_id in globals.id_to_room:
                room_class = globals.id_to_room[room_id]
                if self.selected_grid_tile != room_class.grid_coordinates:
                    continue
                raise ValueError("Room tried to override the position of another room! (Iter " + str(i) + " out of " + str(self.rooms_to_create) + ")")
            made_room = room.Room(chosen_room)
            self.add_to_grid(self.selected_grid_tile.copy(), made_room)
            
            from_connecting_door = object.Object('Door')
            from_connecting_door.in_room = from_room.id
            from_room.add_object(from_connecting_door)

            made_connecting_door = object.Object('Door')
            made_connecting_door.in_room = made_room.id
            made_room.add_object(made_connecting_door)

            made_connecting_door.matching_door = from_connecting_door
            from_connecting_door.matching_door = made_connecting_door

            #connecting_door = object.Object('Door')
            #connecting_door.connecting_rooms = {str(from_room.id): str(made_room.id), str(made_room.id): str(from_room.id)}
            #made_room.add_object(connecting_door)
            #from_room.add_object(connecting_door)
            
            

                

    def add_to_grid(self, coordinates, room_class):
        self.grid.append(coordinates)
        room_class.grid_coordinates = coordinates

    def take_step(self, grid_list, direction):
        if direction == "North":
            grid_list[1] += 1
        elif direction == "East":
            grid_list[0] += 1
        elif direction == "South":
            grid_list[1] -= 1
        else:
            grid_list[0] -= 1
        return grid_list # redundancy to allow for `list = take_step(list, dir)` or just `take_step(list, dir)``

    def move_room(self, room_id):
        globals.player_class.current_room = room_id
        entering_room = globals.id_to_room[room_id]
        entering_room.on_enter(globals.player_class)


# First, room checks current grid tile for anything
# if nothing, it places then sends the manager the grid tile it occupies
# 