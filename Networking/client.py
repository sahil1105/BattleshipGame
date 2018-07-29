import os
from socket import *


class BattleshipClient:
    """
    Class to represent the client side that is the message sending side
    of a Battleship player.
    @sahil1105
    """
    def __init__(self, opp_addr):
        """
        Constructor for the BattleshipClient.
        Sets up the socket and other other information.
        :param opp_addr: The IP and Port of the opponent's server.
        """
        self.host = opp_addr[0]
        self.port = opp_addr[1]
        self.opp_addr = (self.host, self.port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)

    def connect_to_server(self, my_server_addr):
        """
        Function to establish the initial connection between the client
        and the opponent's server. Sends a short-burst containing information
        about the player's server's IP and Port information, to the opponent's
        server.
        :param my_server_addr: IP and Port number of the player's own server.
        :return: None
        """
        self.udp_socket.sendto(my_server_addr.encode(), self.opp_addr)

    def send_data(self, data):
        """
        Utility function to send data from this client to the opponent's
        server. Encodes the data and sends it to the opponent's
        server.
        :param data: Data to encode and send to the opponent's server.
        :return: True if the transmission was successful, False otherwise.
        """
        print("Sending:", data)
        bytes_sent = self.udp_socket.sendto(data.encode(), self.opp_addr)
        if bytes_sent > 0:
            return True
        return False

    def shutdown(self):
        """
        Utility function to shutdown the client.
        Basically closes the UDP socket and makes it available for re-use.
        :return: None
        """
        self.udp_socket.close()