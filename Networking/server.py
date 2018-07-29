import os
from socket import *


class BattleshipServer:
    """
    Class to represent the server side i.e. the message receiving side of the
    Battleship Networking backend.
    @sahil1105
    """
    def __init__(self):
        """
        Constructor for the BattleshipServer.
        Sets up the socket for the server. Chooses a random open port to initialize on.
        Uses UDP.
        """
        self.host = ""
        self.port = 0
        self.buffer = 1024
        self.addr = (self.host, self.port)
        self.opp_addr = None
        self.data = None
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)

    def get_ip(self):
        """
        Utility static function to get the IP of the current network.
        :return: String representing the current IP address.
        """
        return gethostbyname(gethostname())

    def start_server(self):
        """
        Function to start the server. Binds the socket to a port on the
        network.
        :return: The IP and port details of the server.
        """
        self.udp_socket.bind(self.addr)
        self.host = self.get_ip()
        self.port = self.udp_socket.getsockname()[1]
        self.addr = (self.host, self.port)
        print("My server details:", self.addr)
        return self.addr

    def find_opp(self):
        """
        Function to find the opponent by waiting for its client to connect
        to this server. The one-time message contains the IP and Port of the
        opponent's server. This information is used by our client
        to send data to the opponent.
        :return: The IP and Port address of the opponent's server.
        """
        opp_addr, _ = self.udp_socket.recvfrom(self.buffer)  # Get a message from opponent
        opp_addr = opp_addr.decode()
        opp_addr = opp_addr.split(',')
        opp_ip = opp_addr[0]  # IP
        opp_port = int(opp_addr[1])  # Port
        self.opp_addr = (opp_ip, opp_port)
        print("My opponent's details:", self.opp_addr)
        return self.opp_addr

    def get_data(self):
        """
        Utility function which starts listening on the UDP socket
        until a message is received. When it is, it decodes the data and returns it.
        :return: The decoded message received.
        """
        self.data, _ = self.udp_socket.recvfrom(self.buffer)
        print("received:", self.data.decode())
        return self.data.decode()

    def close_server(self):
        """
        Utility function to close the server. Essentially closes the socket
        on which this server exists and make it available for re-use.
        :return: None
        """
        self.udp_socket.close()

