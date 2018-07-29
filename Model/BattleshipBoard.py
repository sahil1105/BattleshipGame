import numpy as np
import pandas as pd
from Model.Ship import Ship, compute_end_loc, get_ship_blocks
from random import randint


class BattleshipBoard:
    """
    BattleshipBoard class simulates the Battleship Board. It can serve as both the active player's
    board with knowledge of the player's ships or the board to indicate your hits
    on the opponent's board. The functions are modular enough to replicate the functionality
    when used in the right way.
    The underlying data-structure stores integers where they mean:
     0: Nothing
     1: Ship
    -1: Hit a ship
    -2: Hit an empty location
    -3: Redundant
    Forms the 'brains' of the model for the Battleship game.
    @author sahil1105
    """
    # Block describer constants
    EMPTY = 0
    SHIP = 1
    SHIP_HIT = -1
    EMPTY_HIT = -2
    REDUNDANT = -3

    def __init__(self, board_dims: tuple =(10, 10), ships: list = []):
        """
        Constructor for Battleship Board.
        :param board_dims: Dimensions of the board. 2D Tuple of natural numbers expected.
        :param ships: List of Ship objects to add to the board. Defaults to an empty list
                      allowing later addition of Ships to the board.
        """
        self.board = np.zeros(board_dims, dtype=int)  # Initialize the array representing the game board.
        for ship in ships:  # Add the ships if positions are valid
            added_successfully = self.add_ship(ship)
            if not added_successfully:
                print("Invalid Ship Locations given.")
                break

    def add_ship(self, ship: Ship) -> bool:
        """
        Function to add a Ship to the GameBoard.
        Additions can fail if one of the positions the ship needs is already occupied,
        or if it is being put within one block of an existing ship.
        :param ship: Ship object to add to the board.
        :return: True if addition was successful, False otherwise.
        """
        # Check that the locations given are within bounds of this board.
        if len(ship.start_loc) != len(self.board.shape) or not self.within_bounds(ship.start_loc) \
                or not self.within_bounds(ship.end_loc):
            return False
        # Compute the positions on the board that need to be assigned to this ship.
        locs_to_mark = get_ship_blocks(ship.start_loc, ship.length, ship.direction)
        # Check that none of the positions are already marked.
        if self.already_marked(locs_to_mark):
            return False
        # Check that the ship is not within one block of an existing ship
        if self.surrounding_ship_exists(locs_to_mark):
            return False
        # Mark the positions as containing the ship
        self.mark_as_ship(locs_to_mark)

        return True

    def clear_board(self):
        """
        Utility function to clear the board.
        :return: None
        """
        self.board = np.zeros(self.board.shape, dtype=int)

    def generate_random_board(self, ship_types: dict={4: 1, 3: 2, 2: 3, 1: 4}):
        """
        Function to generate a random arrangement of the ships as indicated in
        ship_types on the current game board.
        The game board is cleared and the ships in ship_types are then randomly added
        to the game board. The output arrangement is a valid gameboard arrangement,
        i.e. a piece is only added in a certain position if it satisfies the constraints
        of the Battleship game.
        :param ship_types: Dictionary of ship lenghts to number of ships of that length.
        :return: None
        """
        rows, cols = self.board.shape  # Get shape of the board.
        self.clear_board()  # Clear the board.
        ships = []
        for ship_len, freq in ship_types.items():  # Add the ship_lens, freq times to the list.
            for _ in range(freq):
                ships.append(ship_len)
        ships = sorted(ships, reverse=True)  # Reverse sort to ensure that larger pieces are added first (heuristic)

        while len(ships) > 0:  # Until ships to add
            ship_length_to_add = ships.pop(0)
            added = False
            while not added:  # Keep trying to add to the board until successful
                # Get a random board position and direction for the ship
                x, y, dir_ = get_random_coord_and_dir(rows, cols)
                if self.add_ship(Ship((x, y), ship_length_to_add, dir_)):  # Try adding to the board.
                    added = True

    def remove_ship(self, ship: Ship) -> bool:
        """
        Function to remove a Ship from the GameBoard.
        Removal can fail if the ship does not exist or some of the parameters are wrong.
        Finds the corresponding ship on the board and marks the corresponding boxes as unmarked.
        :param ship: Ship object to remove from the board.
        :return: True if the removal was successful, False otherwise.
        """
        # Check that the locations are within bounds
        if len(ship.start_loc) != len(self.board.shape) or not self.within_bounds(ship.start_loc) \
                or not self.within_bounds(ship.end_loc):
            return False
        # Compute the positions on the board that need to be removed as ship
        locs_to_unmark = get_ship_blocks(ship.start_loc, ship.length, ship.direction)
        # If there is a ship in those spots, remove it
        for pos in locs_to_unmark:
            if self.board[pos] == BattleshipBoard.SHIP:
                self.board[pos] = BattleshipBoard.EMPTY
        return True

    def move_ship(self, init_loc: tuple, final_loc: tuple) -> bool:
        """
        Function to move a ship with a piece currently at init_loc to final_loc, keeping the same
        orientation. The new ship starts at the final_loc, i.e. it extends either downwards or rightwards
        from final_loc. The length is preserved. The move is only executed if it doesn't
        passes the addition constraints.
        :param init_loc: The location where a part of the ship lies.
        :param final_loc: The location to move to.
        :return: True if the move was successful, False otherwise
        """
        # Check that the coordinates are within bounds
        if self.within_bounds(init_loc) and self.within_bounds(final_loc):
            if self.board[init_loc] == BattleshipBoard.SHIP:  # Check that there is a ship at the given space
                # Get relevant information about the ship
                ship_ends = self.find_ship_ends(init_loc)
                ship_len = self.get_ship_len(init_loc, ship_ends)
                ship_dir = self.get_ship_dir(init_loc, ship_ends)
                if self.remove_ship(Ship(ship_ends[0], ship_len, ship_dir)):  # Remove original ship
                    if self.add_ship(Ship(final_loc, ship_len, ship_dir)):  # Add the new one
                        return True
                    else:
                        self.add_ship(Ship(ship_ends[0], ship_len, ship_dir))  # Re-instate original if addition failed
        return False

    def rotate_ship(self, loc: tuple, new_dir: tuple):
        """
        Function to rotate a ship, a part of which lies at loc, to the new_dir.
        The rotation will happen along the leftmost or uppermost piece of the ship.
        The rotation must pass the addition constraints to be successful.
        :param loc: The location where a part of the ship lies.
        :param new_dir: The new direction to be applied to the ship.
        :return: True if rotation was successful, False otherwise.
        """
        # Check that the location is within bounds and there is a ship at the given location
        if self.within_bounds(loc) and self.board[loc] == BattleshipBoard.SHIP:
            # Get relevant information about the ship
            ship_ends = self.find_ship_ends(loc)
            ship_len = self.get_ship_len(loc, ship_ends)
            ship_dir = self.get_ship_dir(loc, ship_ends)
            # Short-circuit the rotation if direction already matches or length is 1
            if ship_dir == new_dir or ship_len <= 1:
                return True
            orig_ship = Ship(ship_ends[0], ship_len, ship_dir)
            if self.remove_ship(orig_ship):  # Remove original ship
                if self.add_ship(Ship(ship_ends[0], ship_len, new_dir)):  # Add the rotated ship
                    return True
                else:
                    self.add_ship(orig_ship)  # Re-instate the original if rotation failed.
        return False

    def mark_as_ship(self, locs: list):
        """
        Utility function to mark the given locations as ships.
        Does no validity checks by itself.
        :param locs: List of 2D location tuples to mark as occupied by a ship.
        :return: None
        """
        for loc in locs:
            self.board[loc] = BattleshipBoard.SHIP

    def get_ship_len(self, loc: tuple, ship_ends: list=None) -> int:
        """
        Utility function to get the length of a ship a part of which lies at loc.
        :param loc: Location where a part of the ship lies.
        :param ship_ends: The ends of the ship. Computed using find_ship_ends if not provided.
        :return: Length of the ship at the given location.
        """
        if ship_ends is None:
            ship_ends = self.find_ship_ends(loc)
        return abs(ship_ends[0][0] - ship_ends[1][0]) + abs(ship_ends[0][1] - ship_ends[1][1]) + 1

    def get_ship_dir(self, loc: tuple, ship_ends: list=None) -> tuple:
        """
        Utility function to get the direction of a ship, a part of which lies at loc.
        :param loc: Location where a part of the ship lies.
        :param ship_ends: The ends of the ship. Computed using find_ship_ends if not provided.
        :return: Direction of the ship at the given location.
        """
        if ship_ends is None:
            ship_ends = self.find_ship_ends(loc)
        diff = ((ship_ends[1][0] - ship_ends[0][0]), (ship_ends[1][1] - ship_ends[0][1]))
        s = abs(diff[0] + diff[1])
        if s != 0:
            return diff[0]/s, diff[1]/s
        return 0, 1

    def already_marked(self, locs: list) -> bool:
        """
        Utility function to check if any of a list of locations are already marked as a
        Ship (1,-1), Hit and Miss (-2) or Redundant (-3).
        Function does no validity checks.
        :param locs: List of 2D location tuples. Not validated.
        :return: True if any of the locations are already marked. False otherwise.
        """
        for loc in locs:
            if self.board[loc] != BattleshipBoard.EMPTY:
                return True
        return False

    def surrounding_ship_exists(self, locs: list) -> bool:
        """
        Utility function to check if any of a list of locations are within one block
        of an existing ship.
        Function does not validate the locations passed.
        :param locs: List of 2D location tuples.
        :return: True if any of the locations are within one block of an existing ship,
                 False otherwise.
        """
        for loc in locs:
            if self.adjacent_ship_exists(loc):
                return True
        return False

    def adjacent_ship_exists(self, loc: tuple) -> bool:
        """
        Utility function to check if the given location if adjacent (within 1 block) of an existing
        ship (1 or -1).
        :param loc: 2D tuple containing location coordinates
        :return: True if within one block of an existing ship, False otherwise.
        """
        loc = np.array(loc)
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]  # Directions to check
        dirs = list(map(np.array, dirs))
        for dir_ in dirs:
            # Check if next to a ship
            if self.within_bounds(tuple(loc+dir_)) and self.board[tuple(loc+dir_)] in \
                    [BattleshipBoard.SHIP, BattleshipBoard.SHIP_HIT]:
                return True
        return False

    def already_hit(self, loc: tuple) -> bool:
        """
        Utility function to check whether a location has either already been hit or marked as redundant
        (no point in hitting since there can't be a ship here).
        :param loc: 2D tuple containing location coordinates
        :return: True if location has already been hit or marked redundant, False otherwise
        """
        if self.within_bounds(loc) and self.board[loc] < 0:
            return True
        return False

    def hit(self, loc: tuple) -> int:
        """
        Utility function to make a hit on a ship at the given location
        :param loc: 2D location tuple
        :return: 0 if hit executed but there was no ship at the location.
                 1 if hit was executed and ship part at the location was destroyed.
                 -1 if invalid location or location has already been hit or marked as redundant.
                    In this case the hit is not executed.
        """
        if not self.within_bounds(loc) or self.already_hit(loc):
            return -1

        if self.board[loc] == BattleshipBoard.EMPTY:
            self.mark_ship_miss(loc)
            return 0
        elif self.board[loc] == BattleshipBoard.SHIP:
            self.mark_ship_hit(loc)
            return 1

        return -1

    def mark_ship_hit(self, loc: tuple):
        """
        Utility function to mark a location as hit (-1).
        No validation checks performed.
        :param loc: 2D location tuple
        :return: None
        """
        if self.within_bounds(loc):
            self.board[loc] = BattleshipBoard.SHIP_HIT

    def mark_ship_miss(self, loc: tuple):
        """
        Utility function to mark a location as hit but missed (-2).
        No validation checks performed.
        :param loc: 2D location tuple
        :return: None
        """
        if self.within_bounds(loc):
            self.board[loc] = BattleshipBoard.EMPTY_HIT

    def ship_destroyed(self, loc: tuple, dirs: list=[(1, 0), (0, 1), (-1, 0), (0, -1)]) -> bool:
        """
        Utility function to check if the ship that the given location is a part
        of has been completely destroyed. It first locates the ship that the location
        to belongs to and recursively checks if all of it has been hit.
        :param loc: 2D location tuple
        :param dirs: List of 2D direction tuples of directions to check in. Defaults
                     to all four directions (North, South, East, West)
        :return: False if location is invalid, does not contain a ship, not already hit, or
                 if the whole corresponding ship has not been destroyed. True if the whole
                 ship has been destroyed.
        """
        # If invalid location or ship part at this location hasn't been destroyed,
        if not self.within_bounds(loc) or self.board[loc] != BattleshipBoard.SHIP_HIT:
            return False

        # if all surrounding are non-ships (not 1 or -1), then True
        # if any of surrounding are 1, then False
        single_ship = True  # Is this ship a singular one (just one block)
        whole_ship_destroyed = True  # Has the whole ship been destroyed.
        for dir_ in dirs:
            temp_loc = compute_end_loc(loc, 1, dir_)
            if self.within_bounds(temp_loc):
                if self.board[temp_loc] == BattleshipBoard.SHIP:
                    return False
                if self.board[temp_loc] == BattleshipBoard.SHIP_HIT:
                    # at this pt, at least one surrounding one must be -1, so keep going in those directions
                    single_ship = False
                    if not self.ship_destroyed(temp_loc, [dir_]):  # only need to recursively check this direction
                        whole_ship_destroyed = False
                        break

        return whole_ship_destroyed or single_ship

    def update_redundant_squares(self, last_updated_location: tuple, ship_destroyed: bool=False) -> int:
        """
        Utility function to update the redundant locations (-3,-2,-1) on the game board
        based on the last location that was hit. If ship part hit, then mark
        diagonal directions as redundant (if not already). If the whole ship has been destroyed
        then make the area within one block of the ship redundant (if not already).
        :param last_updated_location: 2D locatiom tuple that was hit.
        :param ship_destroyed: bool indicating whether the whole ship corresponding to this location
                               was destroyed. Expected to be the output of the ship_destroyed function
                               for this location.
        :return: -1 if invalid location or if the location was not hit. 1 otherwise.
        """
        if not self.within_bounds(last_updated_location):  # If invalid location
            return -1
        if self.board[last_updated_location] >= 0:  # If not hit
            return -1
        if self.board[last_updated_location] == BattleshipBoard.SHIP_HIT:  # If a ship part was hit
            # Mark diagonal locations redundant
            self.mark_surroundings_redundant(last_updated_location, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
            if ship_destroyed:
                ship_ends = self.find_ship_ends(last_updated_location)  # find the first and last block of the ship
                for end in ship_ends:
                    self.mark_surroundings_redundant(end)  # Mark all 8 adjacent locations redundant
        return 1

    def find_ship_ends(self, loc: tuple) -> list:
        """
        Utility function to find the start and end block locations of the ship a part of which is at the given
        location. Assumes that the given location is part of a ship.
        :param loc: 2D location tuple
        :return: 2 element list containing the start and end block locations of the corresponding ship.
        """
        ends = [loc, loc]  # Start out both as current location
        # Find the direction the ship goes in, horizontal or vertical
        direction_1 = (0, -1)  # (0,-1) or (1,0)
        if self.within_bounds(compute_end_loc(loc, 1, (1, 0))) \
                and self.board[compute_end_loc(loc, 1, (1, 0))] in [BattleshipBoard.SHIP, BattleshipBoard.SHIP_HIT]:
            direction_1 = (1, 0)

        direction_2 = (0, 1)  # (0,1) or(-1,0)
        if self.within_bounds(compute_end_loc(loc, 1, (-1, 0))) \
                and self.board[compute_end_loc(loc, 1, (-1, 0))] in [BattleshipBoard.SHIP, BattleshipBoard.SHIP_HIT]:
            direction_2 = (-1, 0)

        temp_loc_dir1 = ends[0]
        temp_loc_dir2 = ends[1]
        # Keep going until hit ship end
        while self.within_bounds(temp_loc_dir1) and self.board[temp_loc_dir1] \
                in [BattleshipBoard.SHIP, BattleshipBoard.SHIP_HIT]:
            ends[0] = temp_loc_dir1
            temp_loc_dir1 = compute_end_loc(temp_loc_dir1, 1, direction_1)
        while self.within_bounds(temp_loc_dir2) and self.board[temp_loc_dir2] \
                in [BattleshipBoard.SHIP, BattleshipBoard.SHIP_HIT]:
            ends[1] = temp_loc_dir2
            temp_loc_dir2 = compute_end_loc(temp_loc_dir2, 1, direction_2)

        return sorted(ends)

    def mark_surroundings_redundant(self, loc: tuple,
                                    dirs: list=[(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, 1), (0, -1), (1, 0)]):
        """
        Utility function to mark the surrounding of a location redundant (in the given directions).
        :param loc: 2D location tuple
        :param dirs: List of 2D direction tuples to mark redundant.
        :return: None
        """
        for dir_ in dirs:
            self.mark_redundant_helper(compute_end_loc(loc, 1, dir_))

    def mark_redundant_helper(self, loc: tuple):
        """
        Utility function to mark the given location as redundant if location is valid and not
        already redundant.
        :param loc: 2D location tuple
        :return: None
        """
        if self.within_bounds(loc) and self.board[loc] == BattleshipBoard.EMPTY:
            self.board[loc] = BattleshipBoard.REDUNDANT

    def all_ships_destroyed(self) -> bool:
        """
        Utility function to check if all the ships on the board have been destroyed (when no 1s on the board).
        :return: True if all ships destroyed, False otherwise.
        """
        return not (BattleshipBoard.SHIP in self.board)

    def within_bounds(self, loc: tuple) -> bool:
        """
        Utility function to check that a given location if within the bounds of the board.
        :param loc: 2D location tuple
        :return: True if within bounds, False otherwise.
        """
        return all(list(map(lambda idx_val_pair:
                            True if 0 <= idx_val_pair[1] < self.board.shape[idx_val_pair[0]] else False,
                        enumerate(loc))))

    def __str__(self):
        """
        Overriding the print and string representation of the Battleship Gameboard.
        :return: String representation of the GameBoard.
        """
        row_idx = [i for i in range(self.board.shape[0])]
        col_idx = [i for i in range(self.board.shape[1])]
        df = pd.DataFrame(self.board.T, index=row_idx, columns=col_idx)  # For better print output
        return df.to_string()


def get_random_coord_and_dir(x: int=10, y: int=10, dirs: list=[(0,1), (1,0), (0,-1), (-1,0)]):
    """
    Utility function that basically generates three random numbers. One which is in the range
    0-(x-1), another in the range 0-(y-1) and another in the range 0-(len(dirs)-1).
    Used by the random board function to generate a random board position and direction
    to try to put a ship at.
    :param x: The width of the board.
    :param y: The length of the board.
    :param dirs: List of possible directions.
    :return: A random position and direction.
    """
    dir_len = len(dirs)
    return randint(0, x-1), randint(0, y-1), dirs[randint(0, dir_len-1)]

