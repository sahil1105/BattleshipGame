import numpy as np


class Ship:
    """
    Class to store the properties of a Ship.
    @author sahil1105
    """
    def __init__(self, start_loc: tuple, length: int, direction: tuple):
        """
        Constructor for Ship class.
        :param start_loc: 2D coordinate location of start block of the ship
        :param length: length of the ship
        :param direction: Direction the ship extends in from the starting location
        """
        self.start_loc = start_loc
        self.length = length
        self.alive = True
        self.direction = direction
        # Set end block location based on given starting location, length and direction of extension
        self.end_loc = compute_end_loc(start_loc, length-1, direction)

    def kill(self):
        """
        Utility function to mark the kill as dead.
        :return: None
        """
        self.alive = False


def compute_end_loc(start_loc: tuple, length: int, direction: tuple) -> tuple:
    """
    Utility function to compute the end location of a ship obtained by computing the block location
    that is length away from the start_loc in the given direction.
    :param start_loc: Start location 2D tuple where to extend from
    :param length: Length to extend by
    :param direction: Direction to extend in
    :return: 2D coordinate location of the end block
    """
    end_loc = np.array(start_loc)
    direction = np.array(direction)
    end_loc = end_loc + length*direction
    end_loc = np.array(end_loc, dtype=int)
    return tuple(end_loc)


def get_ship_blocks(start_loc: tuple, length: int, direction: tuple) -> list:

    ship_blocks = []
    for i in range(length):
        ship_blocks.append(compute_end_loc(start_loc, i, direction))
    return ship_blocks
