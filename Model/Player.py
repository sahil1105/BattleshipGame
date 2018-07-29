from Model.BattleshipBoard import BattleshipBoard
from Model.Ship import Ship


class Player:
    """
    Class to save the player details and the GameBoards (your own and the opponents as information is updated based
    on hits).
    @author sahil1105
    """
    def __init__(self, name: str='player', game_board_dims: tuple=(10, 10)):
        """
        Constructor for Player class.
        :param name: Name of the player. Defaults to 'player'.
        :param game_board_dims: Dimensions of the GameBoards to use. Defaults to (10,10)
        """
        self.name = name
        # Board with your ships
        self.my_board = BattleshipBoard(game_board_dims)
        # Board to update as information about opponent's ships is collected
        self.opp_board = BattleshipBoard(game_board_dims)
        # Dictionary containing mapping from ship length to number of your ships of that length
        self.my_ships_counter = {}
        # Dictionary containing mapping from ship length to number of your opponent's ships of that length
        self.opp_ships_counter = {}

    def add_my_ship(self, ship: Ship) -> bool:
        """
        Utility function to add a ship type to your set of lists.
        :param ship: Ship object to add to your game board.
        :return: True if successfully added, False otherwise.
        """
        if self.my_board.add_ship(ship):  # Add to my board
            if ship.length not in self.my_ships_counter:  # Update list of my ship types and frequency
                self.my_ships_counter[ship.length] = 0
            self.my_ships_counter[ship.length] += 1
            return True
        return False

    def add_opp_ship(self, ship_length: int):
        """
        Utility function to add a ship type to known opponent ships.
        :param ship_length: Length of the ship
        :return: None
        """
        if ship_length not in self.opp_ships_counter:  # Update known ship types and frequency of opponent's fleet
            self.opp_ships_counter[ship_length] = 0
        self.opp_ships_counter[ship_length] += 1
