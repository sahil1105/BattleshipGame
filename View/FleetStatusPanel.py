import tkinter


class FleetStatusPanel(tkinter.Frame):
    """
    Class to represent the panel which shows the opponent's fleet status, showing how many of
    each type of ships are left, how many have been destroyed, etc.
    @author sahil1105
    """

    # DIMENSIONS TODO: parametrize these
    SHIP_SQR_SIZE = 20
    PANEL_HEIGHT = 300
    PANEL_WIDTH = 150

    def __init__(self, master, ship_sizes: dict={4: 1, 3: 2, 2: 3, 1: 4}):
        """
        Constructor for the fleet status pane;.
        :param master: Frame to attach to
        :param ship_sizes: Dictionary containing mapping from ship lengths to the number of
                           ships of that length.
                           Defaults to {4: 1, 3: 2, 2: 3, 1: 4}.
        """
        tkinter.Frame.__init__(self, master)
        self.ship_sizes = ship_sizes.copy()
        self.canvas = None
        self.ship_tiles = {}
        self.dead_ships = {}
        self.config_ui()

    def config_ui(self):
        """
        Helper to set up the UI for the fleet status panel.
        :return: None
        """
        self.canvas = tkinter.Canvas(self)
        self.canvas.grid(row=1)
        self.add_ships()
        self.canvas.pack(pady=20, side=tkinter.BOTTOM)

    def add_ships(self):
        """
        Utility function to make the fleet panel and add blocks representing the ship
        information.
        :return: None
        """
        curr_x = 0  # Column count in the current row
        curr_y = 0  # Current row label
        univ_ship_count = 0  # Number of ships already added

        for ship_size, ship_freq in self.ship_sizes.items():
            for count in range(ship_freq):
                # Shift to next row if not enough space left in the current one
                if (curr_x + ship_size)*self.SHIP_SQR_SIZE > self.PANEL_WIDTH:
                    curr_x = 0
                    curr_y += self.SHIP_SQR_SIZE + 10  # TODO
                # Add the tile
                ship_tile = self.canvas.create_rectangle(curr_x*self.SHIP_SQR_SIZE, curr_y,
                                                         (curr_x + ship_size)*self.SHIP_SQR_SIZE,
                                                         curr_y + self.SHIP_SQR_SIZE,
                                                         fill="blue", outline="black",
                                                         tags=("ship", "ship"+str(univ_ship_count)))
                curr_x += ship_size + 1  # TODO

                if ship_size not in self.ship_tiles:
                    self.ship_tiles[ship_size] = []
                self.ship_tiles[ship_size].append((ship_tile, univ_ship_count))  # Store a reference to the tile
                univ_ship_count += 1

    def set_tile_color(self, ship_tile, color="red"):
        """
        Utility function to be probably used by controller to set the color of a tile.
        :param ship_tile: The reference to the tile whose color to change.
        :param color: Color to change. Defaults to 'red'
        :return: None
        """
        self.canvas.itemconfigure(ship_tile, fill=color)

    def reset_panel(self):
        """
        Utility function to reset the status panel, marking all the ships as alive again.
        Refills the ship_tiles dictionary from the dead_ships dictionary and sets the dead_ships
        dictionary as empty again.
        :return: None
        """
        for ship_size in self.dead_ships:
            if ship_size not in self.ship_tiles:
                self.ship_tiles[ship_size] = []
            for ship in reversed(self.dead_ships[ship_size]):
                self.set_tile_color(ship[0], "blue")
                self.ship_tiles[ship_size].insert(0, ship)
        self.dead_ships = {}

    def destroy_ship(self, ship_size, color="red"):
        """
        Utility function to make a change in the panel to show that a ship has been destroyed.
        :param ship_size: Size of the ship destroyed
        :param color: Color to put on the tile to signify it's been destroyed. Defaults to 'red'.
        :return: True if ship was found and color changed, else False.
        """
        # Check if such a ship exists
        if ship_size in self.ship_tiles and len(self.ship_tiles[ship_size]) > 0:
            ship_to_kill = self.ship_tiles[ship_size].pop(0)  # Remove it from list of active ships
            self.set_tile_color(ship_to_kill[0], color)  # Change the color
            if ship_size not in self.dead_ships:
                self.dead_ships[ship_size] = []
            self.dead_ships[ship_size].append(ship_to_kill)
            return True
        return False  # Ship not found






