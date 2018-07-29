import tkinter


class BattleshipGrid(tkinter.Canvas):
    """
    Class to represent the battleship grid.
    @author sahil1105
    """

    BLOCK_MAIN_TAG = 'tile'
    # DIMENSIONS
    SQUARE_SIZE = 30

    def __init__(self, master, init_dims: tuple=(10, 10)):
        """
        Constructor for the Grid.
        :param master: Frame to attach to.
        :param init_dims: Tuple representing the dimensions of the grid. Defaults to (10, 10)
        """
        tkinter.Canvas.__init__(self, master)
        self.dims = init_dims
        self.height = (init_dims[0] + 2) * self.SQUARE_SIZE
        self.width = (init_dims[1] + 2) * self.SQUARE_SIZE
        self.config(height=self.height, width=self.width)
        self.grid_tiles = [[] for _ in range(self.dims[0])]
        self.draw_grid()

    def gen_tile_tag(self, x: int, y: int) -> str:
        """
        Utility function to generate tags for the tiles that are being added to the board.
        :param x: X position on the board.
        :param y: Y position on the board.
        :return: String to be used as the tag for the tile at (x, y).
        """
        temp = (x * self.dims[1]) + y
        return BattleshipGrid.BLOCK_MAIN_TAG + str(temp)

    def get_coord_from_tag(self, tag: str) -> tuple:
        """
        Reverse of the above gen_tile_tag function. Generates the coordinates that a tag
        belongs to.
        :param tag: The tag whose coordinates to find
        :return: The coordinates corresponding the tag.
        """
        position = int(tag[len(BattleshipGrid.BLOCK_MAIN_TAG):])  # Get the index
        y = position % self.dims[1]
        x = int((position - y)/self.dims[1])

        return x, y

    def draw_grid(self):
        """
        Utility function which actually creates the blocks of the grid.
        :return: None
        """
        for x in range(self.dims[0]):
            row_id = str(x)
            self.grid_tiles[x] = []
            self.create_text((x+1.5)*self.SQUARE_SIZE, 10, text=row_id)  # Add row id

            for y in range(self.dims[1]):
                col_id = str(y)

                if x == 0:  # Add column id
                    self.create_text(10, (y+1.5)*self.SQUARE_SIZE, text=col_id)
                # Create the rectangle (block)
                id_ = self.create_rectangle((x+1)*self.SQUARE_SIZE, (y+1)*self.SQUARE_SIZE,
                                            (x+2)*self.SQUARE_SIZE, (y+2)*self.SQUARE_SIZE,
                                            outline="gray", tags=(BattleshipGrid.BLOCK_MAIN_TAG,
                                                                  self.gen_tile_tag(x, y)))
                self.grid_tiles[x].append(id_)  # Save a reference to the created tile.

    def set_tile_color(self, x: int, y: int, color: str) -> bool:
        """
        Utility function to be probably used by the controller to set the color of the tile.
        :param x: X position of the tile
        :param y: Y position of the tile
        :param color: Color to set it to
        :return: True if tile was found and color applied successfully, else False.
        """
        if 0 <= x < len(self.grid_tiles) and 0 <= y < len(self.grid_tiles[x]):
            tile_tag = self.gen_tile_tag(x, y)
            tile_id = self.find_withtag(tile_tag)  # Find a reference to the tile
            self.itemconfigure(tile_id, fill=color)  # Change the color
            return True

        return False

    def set_tile_border(self, x: int, y: int, color: str) -> bool:
        """
        Utility function to be probably used by the controller to set the color of the border.
        :param x: X position of the tile
        :param y: Y position of the tile
        :param color: Color to set it to
        :return: True if tile was found and color applied successfully, else False.
        """
        if 0 <= x < len(self.grid_tiles) and 0 <= y < len(self.grid_tiles[x]):
            tile_tag = self.gen_tile_tag(x, y)
            tile_id = self.find_withtag(tile_tag)  # Find a reference to the tile
            self.itemconfigure(tile_id, outline=color, width=int(self.SQUARE_SIZE/10))  # Change the color
            return True

        return False
