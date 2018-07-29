import unittest
from Model.Player import *


class TestPlayer(unittest.TestCase):
    """
    UnitTest class to test functionality of the Player class and its functions such as
    add_my_ship and add_opp_ship.
    @author sahil1105
    """
    def setUp(self):
        """
        Set up the test suite by initializing an instant of the Player class.
        :return: None
        """
        self.player = Player('Sahil', (5,5))

    def test_add_my_ship(self):
        """
        Test the functionality of the add_my_ship function.
        :return: None
        """
        assert self.player.add_my_ship(Ship((0,1), 3, (1,0))) is True  # Valid add
        assert self.player.my_ships_counter[3] == 1  # Check that the counter was incremented
        assert self.player.add_my_ship(Ship((5,0), 6, (-1,0))) is False  # Invalid add
        assert 6 not in self.player.my_ships_counter  # Ensure counter was not incremented
        assert self.player.add_my_ship(Ship((0,4), 3, (1,0))) is True  # Valid add
        assert self.player.my_ships_counter[3] == 2  # Check that the counter was incremented

    def test_add_opp_ship(self):
        """
        Test the functionality of the add_opp_ship function.
        :return: None.
        """
        self.player.add_opp_ship(3)  # Valid add
        assert self.player.opp_ships_counter[3] == 1  # Check that the counter was incremented
        self.player.add_opp_ship(3)  # Valid add
        assert self.player.opp_ships_counter[3] == 2  # Check that the counter was incremented


if __name__ == '__main__':
    unittest.main()