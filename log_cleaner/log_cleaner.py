from asyncore import write
from cgitb import text
from fileinput import close
import re
from os import listdir
from os.path import isfile, join
from sre_compile import isstring

reg_dict = {}
sorted_list = ()
output_location = "log_cleaner/output.txt"

# Cuts out the item using regex
def regex_act(actor):
    rex1 = re.split("\s\(", actor)
    rex3 = 0
    if len(rex1) == 1:
        rex3 = re.split("([0-9]+)\n", rex1[0])
    else:
        rex2 = re.split("\)\s", rex1[1])
        rex3 = re.split("([0-9]+)\n", rex2[1])
    if len(rex3) == 1:
        if rex1[0] == '':
            return
        return (rex1[0], rex3[0])
    else:
        if rex3[0] == '':
            return (rex1[0], rex3[1])
        else:
            return (rex3[0], rex3[1])

# adds the item and how much it's been bought to reg_dict
def add_to_dict(added, value):
    try:
        test = int(value)
    except:
        return
    if not re.search("\s$", added):
        added = added + ' '
    if added in reg_dict:
        dict_num = reg_dict[added]
        reg_dict[added] = int(dict_num) + int(value)
    else:
        reg_dict[added] = int(value)
    return

def write_to_file(to_write):
    writefile = open(output_location, "a")
    str_write = "\n"
    for item in to_write:
        str_write = str_write + ' ' + str(item)
        if str_write == "\n None": #Just getting malformed entries out of the question
            return
    writefile.write(str_write)
    writefile.close()

def per_file_iteration(file_name):
    global sorted_list
    compiled_file = "log_cleaner/text_inputs/" + file_name
    textoutput = open(compiled_file, "r")
    linelist = textoutput.readlines()

    res = [regex_act(i) for i in linelist]

    output = [add_to_dict(i[0], i[1]) for i in res]

    sorted_list = sorted(reg_dict.items(), key=lambda x: x[1], reverse=True)

    textoutput.close()

onlyfiles = [f for f in listdir("log_cleaner/text_inputs") if isfile(join("log_cleaner/text_inputs", f))]
the_end = [per_file_iteration(i) for i in onlyfiles]
the_end_actually = [write_to_file(i) for i in sorted_list]

