import unittest
from Model.BattleshipBoard import *
import numpy as np


class TestBattleshipBoard(unittest.TestCase):
    """
    UnitTest class to check functionality of the BattleshipBoard class including the main
    functions such as add_ship, hit, ship_destroyed, update_redundant_squares, all_ships_destroyed
    and __str__.
    @author sahil1105
    """
    def setUp(self):
        """
        Setup the test suite. Initialize a BattleshipBoard instance of dimensions 5x5 and assign a
        certain formation of ships on it to be used in testing.
        :return: None
        """
        self.gameboard = BattleshipBoard((5, 5))  # Initialize the board
        # Assign a certain fleet formation
        self.gameboard.board = np.array([[1,1,1,0,0],
                                         [0,0,0,0,1],
                                         [1,0,1,0,1],
                                         [1,0,0,0,0],
                                         [1,0,1,0,1]])

    def test_add_ship(self):
        """
        Test the functionality of the add_ship function.
        :return: None
        """
        self.gameboard.board = np.zeros((5,5))  # Clear the board.
        assert self.gameboard.add_ship(Ship((0,0), 3, (0,1))) is True  # Valid Add
        # Check that the ship was actually added to the board
        assert self.gameboard.board[0][0] == 1
        assert self.gameboard.board[0][1] == 1
        assert self.gameboard.board[0][2] == 1
        assert self.gameboard.add_ship(Ship((1,1), 1, (0,1))) is False  # Can't add next to an existing ship
        assert self.gameboard.add_ship(Ship((1,3), 3, (1,0))) is False  # Can't add next to an existing ship
        assert self.gameboard.add_ship(Ship((1,4), 5, (1,0))) is False  # Ship out of bounds
        assert self.gameboard.add_ship(Ship((1,4), 5, (0,-1))) is False  # Ship out of bounds
        assert self.gameboard.add_ship(Ship((2,0), 3, (1,0))) is True  # Valid add

    def test_hit(self):
        """
        Test the functionality of the hit function.
        :return: None
        """
        assert self.gameboard.hit((0,1)) == 1  # Valid hit
        assert self.gameboard.board[0,1] == -1  # Ensure the ship at the location was hit
        assert self.gameboard.hit((0,1)) == -1  # Invalid hit. This space has already been hit.
        assert self.gameboard.hit((5,6)) == -1  # Out of bounds
        assert self.gameboard.hit((3,2)) == 0  # Hit but no ship at the location
        assert self.gameboard.board[3,2] == -2  # Ensure it is marked as a hit and miss

    def test_ship_destroyed(self):
        """
        Test the functionality of the ship_destroyed function.
        :return: None
        """
        self.gameboard.hit((0,0))  # Make a valid hit
        assert self.gameboard.ship_destroyed((0,0)) is False  # Ensure that this isn't considered a ship wreck
        self.gameboard.hit((0,1))  # Hit 2nd of 3 parts of the ship
        assert self.gameboard.ship_destroyed((0,1)) is False  # Ensure that this isn't considered a ship wreck
        self.gameboard.hit((0,2))  # Hit the final part of the ship
        assert self.gameboard.ship_destroyed((0,2)) is True  # Ensure that the ship destruction is recognized
        # Try same procedure on another ship
        self.gameboard.hit((2,0))
        self.gameboard.hit((4,0))
        self.gameboard.hit((3,0))
        assert self.gameboard.ship_destroyed((3,0)) is True
        # Ensure this works on a single block ship
        self.gameboard.hit((2,2))
        assert self.gameboard.ship_destroyed((2,2)) is True

    def test_update_redundant_squares(self):
        """
        Test the functionality of the update_redundant_squares function.
        :return: None
        """
        self.gameboard.hit((0,2))  # Valid hit
        assert self.gameboard.update_redundant_squares((5,5)) == -1  # Out of bounds
        assert self.gameboard.update_redundant_squares((3,3)) == -1  # Location not hit
        assert self.gameboard.update_redundant_squares((0,2)) == 1  # Valid update call
        # Ensure the diagonal squares around (0,2) are marked redundant
        assert self.gameboard.board[1,1] == -3
        assert self.gameboard.board[1,3] == -3
        self.gameboard.hit((0,1))
        assert self.gameboard.update_redundant_squares((0,1)) == 1  # Valid update call
        self.gameboard.hit((0,0))  # Destroy whole ship
        # Check functionality when whole ship has been destroyed
        assert self.gameboard.update_redundant_squares((0,0), True) == 1
        assert self.gameboard.board[1,0] == -3
        assert self.gameboard.board[1,1] == -3
        assert self.gameboard.board[1,2] == -3
        assert self.gameboard.board[1,3] == -3
        assert self.gameboard.board[0,3] == -3

    def test_all_ships_destroyed(self):
        """
        Check functionality of the all_ships_destroyed function.
        :return: None
        """
        # Hit ships one by one
        self.gameboard.hit((0, 0))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((2, 2))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((0, 1))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((0, 2))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((1, 4))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((2, 0))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((3, 0))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((2, 4))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((4, 0))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((4, 2))
        assert self.gameboard.all_ships_destroyed() is False  # Ships still exist
        self.gameboard.hit((4, 4))
        assert self.gameboard.all_ships_destroyed() is True  # All ships destroyed

    def test_remove_ship(self):
        """
        Check the functionality of the remove_ship function.
        :return: None
        """
        assert self.gameboard.remove_ship(Ship((0, 0), 6, (1, 0))) is False  # Check for invalid arguments
        assert self.gameboard.remove_ship(Ship((0, 0), 3, (0, 1))) is True  # Valid remove should succeed
        # Ensure that the corresponding boxes were emptied
        assert self.gameboard.board[0, 0] == BattleshipBoard.EMPTY
        assert self.gameboard.board[0, 1] == BattleshipBoard.EMPTY
        assert self.gameboard.board[0, 2] == BattleshipBoard.EMPTY

    def test_move_ship(self):
        """
        Check the functionality of the move_ship function.
        :return: None
        """
        assert self.gameboard.move_ship((5, 5), (7, 7)) is False  # Invalid argument detection
        assert self.gameboard.move_ship((1, 4), (2, 4)) is False  # Invalid move detection
        assert self.gameboard.move_ship((1, 4), (0, 4)) is True  # Valid move
        # Ensure that the corresponding boxes were moved
        assert self.gameboard.board[0][4] == 1
        assert self.gameboard.board[1][4] == 1
        assert self.gameboard.board[2][4] == 0
        # Check that the corresponding helper functions are working correctly
        assert self.gameboard.get_ship_len((1, 4)) == 2
        assert self.gameboard.get_ship_dir((1, 4)) == (1, 0)
        assert self.gameboard.get_ship_dir((2, 2)) == (0, 1)

    def test_rotate_ship(self):
        """
        Check the functionality of the rotate_ship function.
        :return: None
        """
        assert self.gameboard.rotate_ship((5, 5), (0, 1)) is False  # Invalid argument detection
        assert self.gameboard.rotate_ship((2, 2), (1, 0)) is True  # Rotate a size 1 ship
        assert self.gameboard.rotate_ship((0, 0), (1, 0)) is False  # Try an invalid rotate
        assert self.gameboard.remove_ship(Ship((2, 0), 3, (1, 0))) is True  # Clear space to allow the rotation
        assert self.gameboard.rotate_ship((0, 0), (1, 0)) is True  # Now rotation should work
        # Check that the corresponding boxes were updated
        assert self.gameboard.board[0][0] == 1
        assert self.gameboard.board[1][0] == 1
        assert self.gameboard.board[2][0] == 1
        assert self.gameboard.board[0][1] == 0
        assert self.gameboard.board[0][3] == 0

    def test_get_random_board(self):

        # self.gameboard.generate_random_board()
        for _ in range(1):
            temp = np.unique(self.gameboard.board, return_counts=True)

    def test_str(self):
        """
        Checks the functionality of the __str__ function and that it doesn't crash.
        :return: None
        """
        assert self.gameboard.__str__() is not ""  # Ensure that the string representation is not empty


if __name__ == '__main__':
    unittest.main()