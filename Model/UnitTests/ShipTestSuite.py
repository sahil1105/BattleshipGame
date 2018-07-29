import unittest
from Model.Ship import *


class TestShip(unittest.TestCase):
    """
    UnitTest class to test the functionality of the Ship class and its functions such
    as kill and compute_end_loc.
    @author sahil1105
    """

    def setUp(self):
        """
        Setup the test suite. Declare a Ship instance at the edge of length 3.
        Ensure that the constructor doesn't crash.
        :return: None
        """
        self.ship = Ship((0,0),3,(1,0))

    def test_kill(self):
        """
        Test the functionality of the kill function.
        :return: None
        """
        self.ship.kill()  # Mark the ship as dead
        assert self.ship.alive is False  # Ensure that the change has been made

    def test_compute_end_loc(self):
        """
        Test the functionality of the compute_end_loc function.
        This is basically supposed to be vector addition.
        :return: None
        """
        # Test some basic examples
        assert compute_end_loc((0,0), 3, (1,0)) == (3,0)
        assert compute_end_loc((0,1), 1, (1,0)) == (1,1)


if __name__ == '__main__':
    unittest.main()
