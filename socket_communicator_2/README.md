# Socket Communicator
-----
## Description
The socket communicator is a tool that allows back-and-forth communication between any number of clients and a server, acting similarly to old chat clients such as IRC (Internet Relay Protocol). The server logs every message and command sent through it, in addition to containing a robust list of administrative tools for admins to use.

## Installation

### Server
1. Download the `server` folder onto a computer.
2. Run the `server.bat` file and set the IP and port to connect to, enter nothing to default to 127.0.0.1[^1] and 65432, respectively.
3. If you want the connection to work across different Wi-Fi connections, port forward the entered port on the `both` setting when choosing TCP or UDP protocol.

### Client
1. Download the `client` folder onto the same or a seperate computer as the server.
2. Download the `windows-curses` pip library by entering `python -m pip install windows-curses` into a comand prompt.
3. Run `client.bat` and enter the IP address and port you wish to connect to. Enter nothing to default to 127.0.0.1[^1] and 65432, respectively.



## Use
1. Once the server is running:
- If the server is localhost, only clients on the same machine will be able to connect.
- If the server is using your local IP address without port forwarding, only clients on the same Wi-Fi connection as you will be able to connect[^2].
- If the server is using your local IP address with port forwarding, all clients will be able to connect[^2].
2. Connected clients are able to chat using the keyboard and sending messages with enter.
3. If you want to have administrator powers, use the `/grant_admin` command with the argument being the password printed into the console of the server.
4. If you want to shut down the server, simply close the console of the server and all clients will disonnect.


[^1]: This is localhost, meaning only connections on the same machine will be processed.
[^2]: They will, however, have to connect using your _public_ IP address, not your local one.