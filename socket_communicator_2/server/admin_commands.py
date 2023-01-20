import client_commands as cli
import file_locations_server as file_locations
from json import load

class AdminCommand(cli.ClientCommand):
    
    def __init__(self, command_name):
        data = load(open(file_locations.ADMIN_COMMANDS_FILE))
        self.__dict__ = data[command_name]

#### As with client_commands.py, these are purely for readability, none of these functions specifically are "in use", the code that is used is in admin_command.json.

# Ban an IP address
def command_ban(executor, server_class, argument):
    import exec
    if executor not in server_class.administrators:
        server_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})
        raise exec.ExecInterrupt
    try:
        socket_object = list(server_class.socket_to_ip.keys())[list(server_class.socket_to_ip.values())[0].index(argument)]
        if socket_object in server_class.administrators:
            server_class.sendall_wrapper(executor, {'output': 'User is an administrator; cannot ban.'})
            raise exec.ExecInterrupt
        server_class.ban_connection(socket_object, executor)
    except ValueError:
        server_class.sendall_wrapper(executor, {'output': 'IP address not found online; banning regardless.'})
        server_class.ban_connection(argument, executor)
    server_class.sendall_wrapper(executor, {'output': 'IP address banned.'})

# "import exec\nif executor not in server_class.administrators:\n\tserver_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})\n\traise exec.ExecInterrupt\ntry:\n\tsocket_object = list(server_class.socket_to_ip.keys())[list(server_class.socket_to_ip.values()).index(argument)]\n\tif socket_object in server_class.administrators:\n\t\tserver_class.sendall_wrapper(executor, {'output': 'User is an administrator; cannot ban.'})\n\t\traise exec.ExecInterrupt\n\tserver_class.ban_connection(socket_object, executor)\nexcept ValueError:\n\tserver_class.sendall_wrapper(executor, {'output': 'IP address not found online; banning regardless.'})\n\tserver_class.ban_connection(argument, executor)\nserver_class.sendall_wrapper(executor, {'output': 'IP address banned.'})"

# Unban an IP address
def command_unban(executor, server_class, argument):
    import exec
    if executor not in server_class.administrators:
        server_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})
        raise exec.ExecInterrupt
    server_class.unban_connection(argument, executor)

# "import exec\nif executor not in server_class.administrators:\n\tserver_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})\n\traise exec.ExecInterrupt\nserver_class.unban_connection(argument, executor)"

# Kick an IP address
def command_kick(executor, server_class, argument):
    import exec
    if executor not in server_class.administrators:
        server_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})
        raise exec.ExecInterrupt
    server_class.kick_connection(argument, executor)

# "import exec\nif executor not in server_class.administrators:\n\tserver_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})\n\traise exec.ExecInterrupt\nserver_class.kick_connection(argument, executor)"

# Set the MOTD of the server
def command_motd(executor, server_class, argument):
    import exec
    if executor not in server_class.administrators:
        server_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})
        raise exec.ExecInterrupt
    server_class.set_motd(executor, argument)

# "import exec\nif executor not in server_class.administrators:\n\tserver_class.sendall_wrapper(executor, {'output': 'Insufficient permissions.'})\n\traise exec.ExecInterrupt\nserver_class.set_motd(executor, argument)"