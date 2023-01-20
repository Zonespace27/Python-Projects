from json import load
import file_locations_server as file_locations

class ClientCommand():
    
    def __init__(self, command_name):
        data = load(open(file_locations.CLIENT_COMMANDS_FILE))
        self.__dict__ = data[command_name]

#### Below are the equivalent of commands in function form for readability

# Displays commands
def command_help(executor, server_class, argument):
    compiled_string = ''
    for command_name in server_class.name_to_command:
        command_class = server_class.name_to_command.get(command_name)
        if command_class.admin_only:
            continue
        compiled_string += command_class.name + ': ' + command_class.desc + (', ' if command_name != list(server_class.name_to_command)[len(server_class.name_to_command) - 1] else '')
    server_class.sendall_wrapper(executor, {'output': compiled_string})

# "compiled_string = ''\nfor command_name in server_class.name_to_command:\n\tcommand_class = server_class.name_to_command.get(command_name)\n\tif command_class.admin_only:\n\t\tcontinue\n\tcompiled_string += command_class.name + ': ' + command_class.desc + (', ' if command_name != list(server_class.name_to_command)[len(server_class.name_to_command) - 1] else '')\nserver_class.sendall_wrapper(executor, {'output': compiled_string})"

# Displays admin commands
def command_adminhelp(executor, server_class, argument):
    compiled_string = ''
    for command_name in server_class.name_to_command:
        command_class = server_class.name_to_command.get(command_name)
        if not command_class.admin_only:
            continue
        compiled_string += command_class.name + ': ' + command_class.desc + (', ' if command_name != list(server_class.name_to_command)[len(server_class.name_to_command) - 1] else '')
    server_class.sendall_wrapper(executor, {'output': compiled_string})

# "compiled_string = ''\nfor command_name in server_class.name_to_command:\n\tcommand_class = server_class.name_to_command.get(command_name)\n\tif not command_class.admin_only:\n\t\tcontinue\n\tcompiled_string += command_class.name + ': ' + command_class.desc + (', ' if command_name != list(server_class.name_to_command)[len(server_class.name_to_command) - 1] else '')\nserver_class.sendall_wrapper(executor, {'output': compiled_string})"

# For being granted superuser perms to ban and what have you
def command_admin_access(executor, server_class, argument):
    import exec
    if executor in server_class.administrators:
        server_class.sendall_wrapper(executor, {'output': 'Administrator perms already granted.'})
        raise exec.ExecInterrupt
    if argument == server_class.admin_pass:
        server_class.add_admin(executor)
        server_class.sendall_wrapper(executor, {'output': 'Permissions granted.'})
    else:
        server_class.sendall_wrapper(executor, {'output': 'Invalid password.'})

# "import exec\nif executor in server_class.administrators:\n\tserver_class.sendall_wrapper(executor, {'output': 'Administrator perms already granted.'})\n\traise exec.ExecInterrupt\nif argument == server_class.admin_pass:\n\tserver_class.add_admin(executor)\n\tserver_class.sendall_wrapper(executor, {'output': 'Permissions granted.'})\nelse:\n\tserver_class.sendall_wrapper(executor, {'output': 'Invalid password.'})"

# For changing your name
def command_name_change(executor, server_class, argument):
    import re
    import exec
    cleaned_name = re.sub('\"|b\"| ', '', argument)[:20]
    if server_class.verify_name(executor, cleaned_name) == False:
        raise exec.ExecInterrupt
    server_class.receive_name_change(executor, cleaned_name)
    server_class.sendall_wrapper(executor, {'output': 'Your name has been changed to: ' + cleaned_name + '.'})

# "import re\nimport exec\ncleaned_name = re.sub('\"|b\"| ', '', argument)[:20]\nif server_class.verify_name(executor, cleaned_name) == False:\n\traise exec.ExecInterrupt\nserver_class.receive_name_change(executor, cleaned_name)\nserver_class.sendall_wrapper(executor, {'output': 'Your name has been changed to: ' + cleaned_name + '.'})"

# List all connected clients
def command_who(executor, server_class, argument):
    compiled_string = ''
    server_class.sendall_wrapper(executor, {'output': 'Total connected: ' + str(len(server_class.socket_to_name))})
    for name in server_class.socket_to_name.values():
        compiled_string += name + (', ' if name != list(server_class.socket_to_name.values())[len(server_class.socket_to_name) - 1] else '')
    server_class.sendall_wrapper(executor, {'output': compiled_string})

# "compiled_string = ''\nserver_class.sendall_wrapper(executor, {'output': 'Total connected: ' + str(len(server_class.socket_to_name))})\nfor name in server_class.socket_to_name.values():\n\tcompiled_string += name + (', ' if name != list(server_class.socket_to_name.values())[len(server_class.socket_to_name) - 1] else '')\nserver_class.sendall_wrapper(executor, {'output': compiled_string})"

# View the MOTD
def command_motd(executor, server_class, argument):
    server_class.sendall_wrapper(executor, {'output': server_class.message_of_the_day})

# "server_class.sendall_wrapper(executor, {'output': server_class.message_of_the_day})"