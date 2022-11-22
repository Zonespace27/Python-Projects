from json import load

# Akin to /atom in DM, this is any object that has physical presence
class PhysicalObject():
    json_location = 'curses_test/json/physical_object.json'

    def __init__(self, object_id = ""):
        object_id = object_id.lower()
        # Where the object thinks it is currently
        self.coordinates = [None, None]
        # The visible name of the object. Unimplemented
        self.name = "Physical Object"
        # The visible desc of the object. Unimplemented
        self.desc = "It's really an object, isn't it?"
        # Higher numbers should layer over lower numbers
        self.layer_priority = 0
        # If things should be able to go through or not
        self.dense = False
        # The back-end ID of the object for making an icon and such
        if object_id != "":
            self.internal_id = object_id
        else:
            self.internal_id = self.__class__.__name__.lower()
        # Json loading
        data = load(open(self.json_location))
        for variable in data[object_id]:
            self.__dict__[variable] = data[object_id][variable]