import unittest
import battleship_simulator
import sys


class TestBattleshipSimulator(unittest.TestCase):
    """
    Class to test the functionality of the game loop.
    @sahil1105
    """

    def setUp(self):
        """
        Change the stdin to a input file.
        :return: None
        """
        self.orig_stdin = sys.stdin
        sys.stdin = open('game_loop_test_input.txt', 'r')

    def test_simulator(self):
        """
        Tests the game loop. If it goes through without crashing, this means
        that the game loop is working.
        :return: None
        """
        battleship_simulator.__main__()

    def tearDown(self):
        """
        Close the input file and restore the stdin to the system's stdin.
        :return:
        """
        sys.stdin.close()
        sys.stdin = self.orig_stdin


if __name__ == '__main__':
    unittest.main()