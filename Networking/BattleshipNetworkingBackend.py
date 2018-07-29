from .client import BattleshipClient
from .server import BattleshipServer
#from Controller.BattleshipController import Battleship_Controller
import time


class BattleshipNetwork:
    """
    Class to represent the networking backend of the Battleship game.
    Reference:
    https://github.com/OskarPersson/Battleship
    http://code.activestate.com/recipes/578802-send-messages-between-computers/
    @author sahil1105
    """
    def __init__(self, controller_ref):
        """
        Constructor for the networking backend. Sets up the server and other constants.
        """
        self.client = None
        self.server = BattleshipServer()
        self.my_server_addr = None
        self.opp_server_addr = None
        self.controller_ref = controller_ref

    def start_game(self):
        """
        Actions to take when a new game is to be started. Actions include starting the server,
        waiting for a connection attempy by the opponent's client with details about
        their server and using our client to connect to thier server.
        :return: None
        """
        self.my_server_addr = self.server.start_server()
        self.opp_server_addr = self.server.find_opp()
        self.client = BattleshipClient(self.server.opp_addr)

    def join_game(self, ip, port):
        """
        Actions to take when the user wants to join a new game. Actions include starting the server,
        sending a message from our client to their server.
        :param ip: IP address of opponent's server
        :param port: Port of opponent's server.
        :return: None
        """
        self.my_server_addr = self.server.start_server()
        self.opp_server_addr = (ip, port)
        self.client = BattleshipClient(self.opp_server_addr)
        self.client.connect_to_server("{},{}".format(self.my_server_addr[0], str(self.my_server_addr[1])))

    def get_move(self):
        """
        Function to be called from the controller to get the next move of the opponent
        :return: None
        """
        opp_move = self.server.get_data()
        return tuple(list(map(int, opp_move.split(","))))

    def send_response(self, response):
        """
        Utility function to send the response of an opponent's move to its server.
        :param response: Response to send
        :return: None
        """
        self.client.send_data(str(response))

    def transmit_move_and_get_response(self, move: tuple):
        """
        Function used to send the player's move to the opponent and wait for the response.
        :param move: The move to send (and ask for response for)
        :return: None
        """
        time.sleep(0.5)
        if self.client.send_data("{},{}".format(move[0], move[1])):
            response = self.server.get_data()
            return int(response)
        return -1

    def end_game(self):
        """
        Utility function for clean up purposes at the end of the game. Shuts down
        the server and the client.
        :return: None
        """
        self.client.shutdown()
        self.server.close_server()
