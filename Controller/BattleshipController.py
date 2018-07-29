import tkinter
import Model.BattleshipBoard as battleship_board
import Model.Ship as Ship
from View.PopupDialogBox import PopupDialogBox
import View.BattleshipGUI as BattleshipGUI
from Networking.BattleshipNetworkingBackend import BattleshipNetwork


class Battleship_Controller():
    """
    The controller class for a Battleship game.
    Adds the appropriate callbacks to the components of the GUI and uses the model to relay
    the changes to the GUI.
    References:
    https://stackoverflow.com/questions/6740855/board-drawing-code-to-move-an-oval
    http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    @author sahil1105
    """

    # Color constants
    COLOR_SHIP = "blue"
    COLOR_EMPTY = "white"
    COLOR_SHIP_HIT = "red"
    COLOR_EMPTY_HIT = "#e5cd77"
    COLOR_REDUNDANT = "#eae0cc"
    # Game state constants
    GAME_STATE_NOT_STARTED = 0
    GAME_STATE_MY_TURN = 1
    GAME_STATE_OPP_TURN = -1
    GAME_STATE_OVER = 2

    def __init__(self, init_dims=(10, 10)):
        """
        Constructor for the controller.
        Sets up the GUI, the model and adds the appropriate callbacks between the two.
        Implements the game loop using game states.
        :param init_dims: The dimension of the game.
        """
        self.init_dims = init_dims
        self.app = tkinter.Tk()
        # Set up the view
        self.view = BattleshipGUI.BattleshipGUI(self.app, init_dims)
        self.view.pack(fill=tkinter.BOTH, expand=1)
        self.view.grab_set()
        self.view.focus_set()
        # Set up the model
        self.model = battleship_board.BattleshipBoard()
        self.model_opp = battleship_board.BattleshipBoard()
        # Set the initial state
        self.curr_game_state = Battleship_Controller.GAME_STATE_NOT_STARTED
        self.ships = self.init_ships()
        self.place_ships()
        # Set up callback functionality for moves
        self.right_click_menu = RightClickRotate(self.view.master, self)
        self._drag_data = {"x": -1, "y": -1, "block_tag": None}
        self._hit_click_data = {"x": -1, "y": -1, "block_tag": None}
        self.setup_callbacks()
        # Start the game
        self.network = BattleshipNetwork(self)  # Initialize the networking backend
        self.app.mainloop()

    def init_ships(self) -> list:
        """
        Provides the default placement of ships.
        :return: List of initial ships to be placed.
        """
        init_ships = [Ship.Ship((0, 0), 2, (0, 1)), Ship.Ship((2, 0), 1, (0, 1)), Ship.Ship((6, 2), 3, (1, 0)),
                      Ship.Ship((0, 4), 1, (1, 0)), Ship.Ship((2, 4), 4, (1, 0)), Ship.Ship((1, 6), 2, (0, 1)),
                      Ship.Ship((4, 7), 1, (1, 0)), Ship.Ship((6, 8), 2, (0, 1)), Ship.Ship((8, 8), 1, (0, 1)),
                      Ship.Ship((0, 9), 3, (1, 0))]
        return init_ships

    def place_ships(self):
        """
        Add the ships to the model and updates the GUI to reflect the additions.
        :return: None
        """
        for ship in self.ships:
            self.model.add_ship(ship)
        self.update_grids()

    def update_grids(self):
        """
        Updates the GUI blocks on the two grids with the states as in the model.
        :return: None
        """
        # Color mapping for block state to color
        color_map = {battleship_board.BattleshipBoard.SHIP: Battleship_Controller.COLOR_SHIP,
                     battleship_board.BattleshipBoard.EMPTY: Battleship_Controller.COLOR_EMPTY,
                     battleship_board.BattleshipBoard.SHIP_HIT: Battleship_Controller.COLOR_SHIP_HIT,
                     battleship_board.BattleshipBoard.EMPTY_HIT: Battleship_Controller.COLOR_EMPTY_HIT,
                     battleship_board.BattleshipBoard.REDUNDANT: Battleship_Controller.COLOR_REDUNDANT}
        # Set the tile colors according to the color map
        for x in range(self.model.board.shape[0]):
            for y in range(self.model.board.shape[1]):
                self.view.my_grid.set_tile_color(x, y, color_map[self.model.board[x, y]])
                self.view.opp_grid.set_tile_color(x, y, color_map[self.model_opp.board[x, y]])

    def reset(self):
        """
        Reset functionality for the game. Resets the model and the view. The scoreboard is not changed.
        :return: None
        """
        # Reset the model
        self.model = battleship_board.BattleshipBoard()
        self.model_opp = battleship_board.BattleshipBoard()
        self.curr_game_state = Battleship_Controller.GAME_STATE_NOT_STARTED
        # Reset the view
        self.ships = self.init_ships()
        self.place_ships()
        self.setup_start_button_callback()
        self.view.opp_piece_panel.reset_panel()
        self.network = BattleshipNetwork(self)

    def reset_score(self):
        """
        Utility function to reset the score of the game to 0-0.
        :return: None
        """
        self.view.scoreboard.reset_scores()

    def setup_callbacks(self):
        """
        Utility function that sets up all the callbacks required for the game.
        :return: None
        """
        self.setup_block_drag_callbacks()
        self.setup_opp_board_callbacks()
        self.setup_right_click_callbacks()
        self.setup_start_button_callback()
        self.setup_join_button_callback()
        self.setup_randomize_button_callback()

    def setup_randomize_button_callback(self):

        self.view.randomize_button.bind("<Button-1>", self.randomize_callback)

    def randomize_callback(self, event):

        if self.curr_game_state == Battleship_Controller.GAME_STATE_NOT_STARTED:
            self.model.generate_random_board()
            self.update_grids()

    def setup_start_button_callback(self):
        """
        Utility function to set up the callback for the start button.
        :return: None
        """
        self.view.start_game_button["text"] = "Start"  # Set text to Start
        self.view.start_game_button.bind("<Button-1>", self.start_button_callback)  # Attach a callback

    def start_button_callback(self, event):
        """
        Callback function for the start button.
        :param event: The button click event details.
        :return: None
        """
        # self.create_server_popup = PopupDialogBox(self.view.master, "Game created at:", "192.168.2.1", "54321")
        # self.view.master.wait_window(self.create_server_popup.top)
        self.network.start_game()
        self.curr_game_state = Battleship_Controller.GAME_STATE_MY_TURN  # Change game state
        self.view.set_status_panel_msg("Your turn")
        # Make the button a forfeit button
        self.view.start_game_button["text"] = "Forfeit"
        self.view.start_game_button.bind("<Button-1>", self.forfeit)

    def forfeit(self, event):
        """
        Callback function for the forfeit button.
        :param event: The button click event details.
        :return: None
        """
        self.network.send_response(3)
        self.view.scoreboard.increment_score_2()  # Increment score of opponent.
        self.view.set_status_panel_msg("You lose")
        self.reset()  # Reset the game

    def setup_join_button_callback(self):
        """
        Utility function to setup the callback on the Join button.
        :return: None
        """
        self.view.join_game_button.bind("<Button-1>", self.join_button_callback)

    def join_button_callback(self, event):
        """
        Callback function for the Join button. Used to join a pre-existing game instance.
        :param event: The button click event details.
        :return: None
        """
        if self.curr_game_state == Battleship_Controller.GAME_STATE_NOT_STARTED:
            self.network.join_game(input("IP?"), int(input("Port?")))
            # self.join_game_popup = PopupDialogBox(self.view.master, "Enter IP and Port to Join", "", "", "Join")
            # self.view.join_game_button["state"] = tkinter.DISABLED
            # self.view.master.wait_window(self.join_game_popup.top)
            # self.view.join_game_button["state"] = tkinter.NORMAL
            # self.network.join_game(self.join_game_popup.entered_value_1, int(self.join_game_popup.entered_value_2))
            self.curr_game_state = Battleship_Controller.GAME_STATE_OPP_TURN  # Change game state
            self.view.set_status_panel_msg("Opponent's turn")
            self.view.start_game_button["text"] = "Forfeit"
            self.view.start_game_button.bind("<Button-1>", self.forfeit)
            tkinter.Tk.update(self.app)
            self.respond_to_opp_move()

    def setup_right_click_callbacks(self):
        """
        Utility function to setup callback for right click on grid blocks.
        :return: None
        """
        self.view.my_grid.tag_bind(self.view.my_grid.BLOCK_MAIN_TAG, "<Button-2>", self.right_click_menu.popup)

    def setup_opp_board_callbacks(self):
        """
        Utility function to set up callback functions for the blocks on opponent's board.
        Used to process hits.
        :return: None
        """
        self.view.opp_grid.tag_bind(self.view.opp_grid.BLOCK_MAIN_TAG, "<ButtonPress-1>", self.press_hit)
        self.view.opp_grid.tag_bind(self.view.opp_grid.BLOCK_MAIN_TAG, "<ButtonRelease-1>", self.release_hit)

    def press_hit(self, event):
        """
        Callback function for when the players tries to hit a block on the
        opponent's grid.
        :param event: The button click event details.
        :return: None
        """
        # If correct game state, then store the information
        if self.curr_game_state == Battleship_Controller.GAME_STATE_MY_TURN:
            self._hit_click_data["block_tag"] = \
                self.view.opp_grid.gettags(self.view.opp_grid.find_closest(event.x, event.y)[0])[1]
            self._hit_click_data["x"], self._hit_click_data["y"] = \
                self.view.my_grid.get_coord_from_tag(self._hit_click_data["block_tag"])

    def release_hit(self, event):
        """
        Callback function when the player hits the block on the opponent's grid.
        :param event: The button click event details.
        :return: None
        """
        # If correct game state, then process the hit on the clicked block.
        if self.curr_game_state == Battleship_Controller.GAME_STATE_MY_TURN:
            item_specifier = self.view.opp_grid.gettags(self.view.opp_grid.find_closest(event.x, event.y)[0])[1]
            x, y = self.view.opp_grid.get_coord_from_tag(item_specifier)
            if x == self._hit_click_data["x"] and y == self._hit_click_data["y"]:
                self.perform_hit(x, y)
            self._hit_click_data["x"] = -1
            self._hit_click_data["y"] = -1
            self._hit_click_data["block_tag"] = None

    def perform_hit(self, x, y):
        """
        Function to perform a hit at (x,y) on the opponent's grid.
        :param x: X-coordinate of where to hit.
        :param y: Y-coordinate of where to hit.
        :return: None
        """
        if self.curr_game_state == Battleship_Controller.GAME_STATE_MY_TURN:  # Ensure correct game state
            if self.model_opp.already_marked([(x, y)]):  # Make sure the block is not already marked
                self.view.set_status_panel_msg("Invalid Move, the box is already marked.")
            else:
                response = self.get_response((x, y))  # Ask for the response fot the move
                if response in [1, 2, 3]:  # If hit
                    self.model_opp.mark_ship_hit((x, y))
                    self.model_opp.update_redundant_squares((x, y), False if response == 1 else True)
                if response in [2, 3]:  # If ship destroyed
                    ship_len = self.model_opp.get_ship_len((x,y))
                    self.view.opp_piece_panel.destroy_ship(ship_len)
                if response == 3:  # If game won
                    self.curr_game_state = Battleship_Controller.GAME_STATE_OVER
                    self.view.set_status_panel_msg("You win!")
                    self.view.scoreboard.increment_score_1()
                    self.network.end_game()
                    self.reset()
                elif response == 0:  # If miss
                    self.model_opp.mark_ship_miss((x, y))
                    self.curr_game_state = Battleship_Controller.GAME_STATE_OPP_TURN
                    self.view.set_status_panel_msg("Opponent's Turn")
                elif response not in [0, 1, 2, 3]:  # If invalid response
                    self.view.set_status_panel_msg("Invalid Response Received!")
            self.update_grids()  # Update GUI based on updated model
            tkinter.Tk.update(self.app)  # Force update the GUI
        if self.curr_game_state == Battleship_Controller.GAME_STATE_OPP_TURN:
            self.respond_to_opp_move()

    def respond_to_opp_move(self):
        """
        Function to handle the move of an opponent, process the move and send the appropriate
        response.
        :return: Response to send to a move
        """
        # Ensure correct game state
        while self.curr_game_state == Battleship_Controller.GAME_STATE_OPP_TURN:
            loc = self.network.get_move()
            if loc == (3,):
                self.curr_game_state = Battleship_Controller.GAME_STATE_OVER
                self.view.set_status_panel_msg("You win!")
                self.view.scoreboard.increment_score_1()
                self.network.end_game()
                self.reset()
                break
            hit_response = self.model.hit(loc)  # Get response of hit
            if hit_response == 1:  # if hit on a ship
                if self.model.ship_destroyed(loc):  # ship destroyed
                    hit_response = 2
                    self.model.update_redundant_squares(loc, True)
                    if self.model.all_ships_destroyed():  # Lost game
                        hit_response = 3
                        self.curr_game_state = Battleship_Controller.GAME_STATE_OVER
                        self.view.set_status_panel_msg("You lost!")
                        self.view.scoreboard.increment_score_2()
                else:
                    self.model.update_redundant_squares(loc)
            else:  # miss, so change of turn
                self.curr_game_state = Battleship_Controller.GAME_STATE_MY_TURN
                self.view.set_status_panel_msg("Your turn")
            self.update_grids()  # Update GUI based on updated model
            tkinter.Tk.update(self.app)  # Force update the GUI
            self.network.send_response(hit_response)  # transmit the response.
            if hit_response == 3:
                self.reset()  # Reset the game if you lose.

    def get_response(self, loc):
        """
        Utility function to get opponent's response to a move to a strike on loc.
        :param loc: Location to hit
        :return: The response to the strike at loc
        """
        return self.network.transmit_move_and_get_response(loc)

    def setup_block_drag_callbacks(self):
        """
        Utility function to set up callbacks for the drag and drop functionality of the board
        to be able to rearrange the blocks before starting the game.
        :return: None
        """
        self.view.my_grid.tag_bind(self.view.my_grid.BLOCK_MAIN_TAG, "<ButtonPress-1>", self.on_tile_press)
        self.view.my_grid.tag_bind(self.view.my_grid.BLOCK_MAIN_TAG, "<ButtonRelease-1>", self.on_tile_release)

    def on_tile_press(self, event):
        """
        Callback function for when a drag is initiated.
        :param event: The mouse press details.
        :return: None
        """
        # Ensure correct game state
        if self.curr_game_state == Battleship_Controller.GAME_STATE_NOT_STARTED:
            # Save starting position
            self._drag_data["block_tag"] = \
                self.view.my_grid.gettags(self.view.my_grid.find_closest(event.x, event.y)[0])[1]
            self._drag_data["x"], self._drag_data["y"] = \
                self.view.my_grid.get_coord_from_tag(self._drag_data["block_tag"])

    def on_tile_release(self, event):
        """
        Callback function for when a drag is finished.
        :param event: The mouse release details.
        :return: None
        """
        # Ensure correct game state.
        if self.curr_game_state == Battleship_Controller.GAME_STATE_NOT_STARTED:
            # Find the loc to move to
            item_specifier = self.view.my_grid.gettags(self.view.my_grid.find_closest(event.x, event.y)[0])[1]
            final_x, final_y = self.view.my_grid.get_coord_from_tag(item_specifier)
            # If actually moved
            if self._drag_data["x"] != final_x or self._drag_data["y"] != final_y:
                # Attempt to move the ship
                self.model.move_ship((self._drag_data["x"], self._drag_data["y"]), (final_x, final_y))
                self.update_grids()  # Update GUI
            # Reset the drag and release details.
            self._drag_data["x"] = 0
            self._drag_data["y"] = 0
            self._drag_data["block_tag"] = None


class RightClickRotate:
    """
    Class to represent right click functionality on the blocks of the player's grid
    in the Battleship game.
    Reference:
    https://stackoverflow.com/questions/12014210/tkinter-app-adding-a-right-click-context-menu/12014379
    @author sahil1105
    """
    def __init__(self, master, controller_ref: Battleship_Controller):
        """
        Constructor for the right click instance. Sets up the associated menu to show and
        the callbacks for options on this menu.
        :param master: Master frame
        :param controller_ref: Reference to the battleship controller.
        """
        self.aMenu = tkinter.Menu(master, tearoff=0)  # Create the menu
        self.controller_ref = controller_ref
        # Add items to menu
        self.aMenu.add_command(label="Orient Horizontally", command=self.orient_horizontally)
        self.aMenu.add_command(label="Orient Vertically", command=self.orient_vertically)
        self.selected_item = None

    def orient_helper(self, direction: tuple):
        """
        Helper function to orient the block at the clicked location.
        :param direction: The direction to orient in.
        :return: None
        """
        if self.selected_item is not None:
            self.controller_ref.model.rotate_ship(self.selected_item, direction)  # Try rotating
            self.controller_ref.update_grids()  # Update the GUI
            self.selected_item = None  # Reset the right click state

    def orient_horizontally(self):
        """
        Callback function for Orient Horizontally option on the menu.
        :return: None
        """
        self.orient_helper((1, 0))

    def orient_vertically(self):
        """
        Callback function for Orient Vertically option on the menu.
        :return: None
        """
        self.orient_helper((0, 1))

    def popup(self, event):
        """
        Callback function to when a right click is pressed on the grid.
        :param event: The click details.
        :return: None
        """
        # Ensure correct game state
        if self.controller_ref.curr_game_state == Battleship_Controller.GAME_STATE_NOT_STARTED:
            # Find the block coordinates where right click was attempted.
            item_specifier = self.controller_ref.view.my_grid.gettags(self.controller_ref.
                                                                      view.my_grid.find_closest(event.x, event.y)[0])[1]
            self.selected_item = self.controller_ref.view.my_grid.get_coord_from_tag(item_specifier)
            self.aMenu.post(event.x_root, event.y_root)  # Show the menu at the location of right click


if __name__ == '__main__':
    bc = Battleship_Controller()
