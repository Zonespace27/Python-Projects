hmm = {3 : "foo"}

import sys
import re

class Debug():
    def __init__(self):
        global hmm
        #self.id = [0,0]
#        if(self.id in hmm):
#            raise ValueError("Room ID " + str(self.id) + " already exists in id_to_room, but another tried to override it!")

class Debug2(Debug):
    foo = 2

#x = Debug()

def debug_func(list):
    list[1] += 1

if __name__ == "__main__":
    #main(sys.argv[1:])
    #print(re.sub(r"\b(and|a|or|the|an|is|at)\b", "", "Attack the slime", 0, re.IGNORECASE))
    #print(len(re.findall(r"\S+", "Find all the words")))
    #exec("import testing_grounds\ntesting_grounds.debug_func()")
    pass
