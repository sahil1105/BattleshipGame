import tkinter
from .BattleshipGrid import BattleshipGrid
from .FleetStatusPanel import FleetStatusPanel
from .PopupDialogBox import PopupDialogBox
from .Scoreboard import Scoreboard


class BattleshipGUI(tkinter.Frame):
    """
    Class to represent the GUI (View) for the BattleShip game.
    Reference:
    https://codereview.stackexchange.com/questions/23743/battleship-in-python-tkinter
    https://github.com/xstiv07/Battleship/blob/master/gui.py
    https://github.com/boompig/pyBattleShip/
    @author sahil1105
    """
    def __init__(self, master, init_dimensions: tuple = (10, 10)):
        """
        Constructor for the View part of the BattleShip game. It renders the top level frame and sets up all
        the essential components including the two grids, a fleet status panel, a status panel, and buttons
        to create ot join the game.
        :param master: Frame to attach to.
        :param init_dimensions: The starting dimensions of the grid. Defaults to (10, 10).
        """
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.dimensions = init_dimensions
        self.my_grid_frame = None
        self.my_grid = None
        self.opp_grid_frame = None
        self.opp_grid = None
        self.opp_piece_panel = None
        self.status_panel_txt_box = None
        self.join_game_button = None
        self.start_game_button = None
        self.randomize_button = None
        self.scoreboard_frame = None
        self.scoreboard = None
        self.setup_ui()
        # self.setup_init_state()
        self.config(height=500, width=1000)

    def setup_ui(self):
        """
        Utility function to add all the required UI elements to the frame.
        :return: None
        """
        self.add_my_grid()
        self.add_opp_grid()
        self.add_opp_piece_panel()
        self.add_status_msg_panel()
        self.add_buttons()
        self.add_scoreboard()

    def add_scoreboard(self):
        """
        Utility function to add the scoreboard to the GUI.
        :return: None
        """
        self.scoreboard_frame = tkinter.Frame(self)
        self.scoreboard_frame.place(x=800, y=300)
        self.scoreboard = Scoreboard(self.scoreboard_frame, (150, 100))
        self.scoreboard.pack(side=tkinter.LEFT, pady=20)

    def setup_init_state(self):
        """
        Utility function for testing purposes. Arranges the pieces in a pre-determined order.
        For testing purposes only.
        :return: None
        """
        # game_frame.my_grid.set_tile_color(3, 3, "red")

        for x, y in [(0, 0), (0, 1), (0, 4), (0, 9), (1, 6), (1, 7), (1, 9), (2, 0), (2, 4), (2, 9), (3, 4), (4, 4),
                     (4, 7), (5, 4),
                     (6, 2), (6, 8), (6, 9), (7, 2), (8, 2), (8, 8)]:
            self.my_grid.set_tile_color(x, y, "blue")

        for x, y in [(3, 4), (8, 2), (4, 7), (6, 2)]:
            self.my_grid.set_tile_color(x, y, "red")

        for x, y in [(6, 1), (1, 4), (9, 2)]:
            self.my_grid.set_tile_color(x, y, "#e5cd77")

        for x, y in [(5, 1), (5, 3), (7, 1), (7, 3), (9, 1), (9, 3), (2, 3), (2, 5), (4, 3), (4, 5), (3, 6), (3, 7),
                     (3, 8), (4, 6),
                     (4, 8), (5, 6), (5, 7), (5, 8)]:
            self.my_grid.set_tile_color(x, y, "#eae0cc")

        for x, y in [(1, 3), (2, 3), (6, 5)]:
            self.opp_grid.set_tile_color(x, y, "red")

        for x, y in [(6, 4), (2, 4), (8, 8)]:
            self.opp_grid.set_tile_color(x, y, "#e5cd77")

        for x, y in [(0, 2), (0, 4), (2, 2), (1, 2), (1, 4), (3, 2), (3, 4), (5, 4), (5, 6), (7, 4), (7, 6), (0, 3),
                     (3, 3)]:
            self.opp_grid.set_tile_color(x, y, "#eae0cc")

        self.opp_piece_panel.destroy_ship(2)

    def add_my_grid(self):
        """
        Utility function to add the player's grid of ships to the Frame.
        :return: None
        """
        self.my_grid_frame = tkinter.Frame(self)
        self.my_grid_frame.place(x=30, y=10)  # TODO: Need to modularize
        tkinter.Label(self.my_grid_frame, text="My Grid").pack()
        self.my_grid = BattleshipGrid(self.my_grid_frame, self.dimensions)
        self.my_grid.pack(side=tkinter.LEFT, pady=20)

    def add_opp_grid(self):
        """
        Utility function to add the opponent's grid to the Frame.
        :return: None
        """
        self.opp_grid_frame = tkinter.Frame(self)
        self.opp_grid_frame.place(x=400, y=10)  # TODO: Need to modularize
        tkinter.Label(self.opp_grid_frame, text="Opponent's Grid").pack()
        self.opp_grid = BattleshipGrid(self.opp_grid_frame, self.dimensions)
        self.opp_grid.pack(side=tkinter.LEFT, pady=20)

    def add_opp_piece_panel(self):
        """
        Utility function to add the fleet status panel to monitor the opponent's ships.
        :return: None
        """
        self.opp_piece_panel = FleetStatusPanel(self)
        self.opp_piece_panel.config(height=500)  # TODO
        tkinter.Label(self.opp_piece_panel, text="Opponent's Fleet Status").pack(pady=10, side=tkinter.LEFT)
        self.opp_piece_panel.place(x=800, y=30)

    def add_status_msg_panel(self):
        """
        Utility function to add a text panel that displays the game messages and current state of the game.
        :return: None
        """
        status_panel = tkinter.Frame(self)
        status_panel.place(x=425, y=400)  # TODO
        self.status_panel_txt_box = tkinter.Text(status_panel)
        self.status_panel_txt_box.pack(side=tkinter.BOTTOM, pady=10)
        self.status_panel_txt_box.insert('1.0', "Place your Ships")
        self.status_panel_txt_box.config(height=10, width=50)

    def add_buttons(self):
        """
        Utility function to add the required buttons to the Frame. Adds a button to join an existing game or
        create a new game.
        :return: None
        """
        button_panel = tkinter.Frame(self)
        button_panel.place(x=350, y=450)  # TODO
        self.randomize_button = tkinter.Button(button_panel, text="Randomize")
        self.randomize_button.pack(side=tkinter.LEFT, padx=10, pady=10)
        self.join_game_button = tkinter.Button(button_panel, text="Join")  # , command=self.get_ip_addr_to_join)
        self.join_game_button.pack(side=tkinter.LEFT, padx=10, pady=10)  # TODO
        self.start_game_button = tkinter.Button(button_panel, text="Start")  # , command=self.create_new_game)
        self.start_game_button.pack(side=tkinter.RIGHT, padx=10, pady=10)  # TODO


    def set_status_panel_msg(self, new_msg: str):
        """
        Utility function to set the message in the status panel.
        :param new_msg: String to show in the status panel.
        :return: None
        """
        self.status_panel_txt_box.delete('1.0', tkinter.END)
        self.status_panel_txt_box.insert('1.0', new_msg)

    def get_ip_addr_to_join(self):
        """
        Callback function for the join button. Creates a popup dialog box which takes in the IP
        address to join.
        :return: None
        """
        self.ip_addr_popup = PopupDialogBox(self.master, "Enter the IP Addr to join", "Join")
        self.join_game_button["state"] = "disabled"
        self.master.wait_window(self.ip_addr_popup.top)
        self.join_game_button["state"] = "normal"

    def create_new_game(self):
        """
        Callback function for the Start button. Creates a pop-up dialog that gives the IP address
        that another player must join.
        :return: None
        """
        self.create_server_popup = PopupDialogBox(self.master, "Game created at:", "OK", "192.168.1.1")
        self.start_game_button['state'] = 'disabled'
        self.master.wait_window(self.create_server_popup.top)
        self.start_game_button['state'] = 'normal'

# FOR TESTING PURPOSES ONLY


if __name__ == '__main__':
    app = tkinter.Tk()
    game_frame = BattleshipGUI(app)
    game_frame.pack(fill=tkinter.BOTH, expand=1)

    game_frame.grab_set()
    game_frame.focus_set()
    # game_frame.set_status_panel_msg("Your move")

    app.mainloop()









