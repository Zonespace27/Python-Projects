import re
from os import listdir
from os.path import isfile, join
from glob import glob

reg_dict = {}
sorted_list = ()
all_files = []
output_location = "log_reader/outputfile.txt"

# Cuts out the item using regex
def regex_act(actor):
    rex1 = re.split("\spurchased\s", actor)
    if len(rex1) != 2:
        return
    rex1_string = rex1[1]
    rex2 = re.split("\sfor\s", rex1_string)
    if len(rex2) != 2:
        return
    return rex2[0]

# Adds the item and how much it's been bought to reg_dict
def add_to_dict(added):
    if added in reg_dict:
        dict_num = reg_dict[added]
        reg_dict[added] = dict_num + 1
    else:
        reg_dict[added] = 1

# Writes to the output file with the data and the number provided
def write_to_file(to_write):
    write_file = open(output_location, "a")
    str_write = "\n"
    for item in to_write:
        str_write = str_write + ' ' + str(item)
        if str_write == "\n None": #Just getting malformed entries out of the question
            return
    write_file.write(str_write)
    write_file.close()

# Do the regex and list sorting on each file iteration
def per_file_iteration(file_name):
    global sorted_list
    reg_check = re.search("uplink\.log", file_name)
    if reg_check is None:
        return
    text_output = open(file_name, "r")
    line_list = text_output.readlines()

    res = [regex_act(i) for i in line_list]

    output = [add_to_dict(i) for i in res]

    sorted_list = sorted(reg_dict.items(), key=lambda x: x[1], reverse=True)

    text_output.close()

recurse_dir = glob("**/", recursive = True)

file_clear = open(output_location, "w")
file_clear.close()

for dir in recurse_dir:
    only_files = [f for f in listdir(dir) if isfile(join(dir, f))]
    compiled_files = []
    for file in only_files:
        file = dir + str(file)
        compiled_files.append(file)
    all_files.extend(compiled_files)

the_end = [per_file_iteration(i) for i in all_files]
the_end_actually = [write_to_file(i) for i in sorted_list]