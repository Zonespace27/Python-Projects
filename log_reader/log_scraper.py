from asyncore import write
from cgitb import text
from fileinput import close
import re
from os import listdir
from os.path import isfile, join

reg_dict = {}
sorted_list = ()

# Cuts out the item using regex
def regex_act(actor):
    rex1 = re.split("purchased\s", actor)
    if len(rex1) != 2:
        return
    rex1_string = rex1[1]
    rex2 = re.split("\sfor", rex1_string)
    if len(rex2) != 2:
        return
    return rex2[0]

# adds the item and how much it's been bought to reg_dict
def add_to_dict(added):
    if added in reg_dict:
        dict_num = reg_dict[added]
        reg_dict[added] = dict_num + 1
    else:
        reg_dict[added] = 1

def write_to_file(to_write):
    writefile = open("log_reader/outputfile.txt", "a")
    str_write = "\n"
    for item in to_write:
        str_write = str_write + ' ' + str(item)
        if str_write == "\n None": #Just getting malformed entries out of the question
            return
    writefile.write(str_write)
    writefile.close()

def per_file_iteration(file_name):
    global sorted_list
    compiled_file = "log_reader/text_inputs/" + file_name
    textoutput = open(compiled_file, "r")
    linelist = textoutput.readlines()

    res = [regex_act(i) for i in linelist]

    output = [add_to_dict(i) for i in res]

    sorted_list = sorted(reg_dict.items(), key=lambda x: x[1], reverse=True)

    textoutput.close()
    return

onlyfiles = [f for f in listdir("log_reader/text_inputs") if isfile(join("log_reader/text_inputs", f))]
the_end = [per_file_iteration(i) for i in onlyfiles]
the_end_actually = [write_to_file(i) for i in sorted_list]