import tkinter


class Scoreboard(tkinter.Canvas):
    """
    Class to represent a scoreboard for a series of matches between two players.
    Reference:
    https://stackoverflow.com/questions/23360003/display-update-score-on-python-using-tkinter
    http://effbot.org/tkinterbook/canvas.htm
    https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Get-input-using-Entry-class-Tkinter-textbox
    @author sahil1105
    """
    def __init__(self, master, dims: tuple=(150, 100)):
        """
        Constructor for the scoreboard canvas.
        :param master: The master frame to pack to.
        :param dims: The dimensions of the scoreboard. Defaults to (150, 100)
        """
        tkinter.Canvas.__init__(self, master)
        self.master = master
        self.width = dims[0]
        self.height = dims[1]
        self.config(height=self.height, width=self.width)
        self.player1_name = None
        self.player2_name = None
        self.score_box_1 = None
        self.score_box_2 = None
        self.score_1 = 0
        self.score_2 = 0
        self.create_ui()

    def create_ui(self):
        """
        Utility function to add the relevant elements to the scoreboard UI.
        :return: None
        """
        self.player1_name = self.create_player_name_box(int(self.width/4), int(self.height/4), "You")
        self.player2_name = self.create_player_name_box(int(3*self.width/4), int(self.height/4), "Opponent")
        self.score_box_1 = self.create_score_box(int(self.width/4), int(3*self.height/4), color="blue")
        self.score_box_2 = self.create_score_box(int(3*self.width/4), int(3*self.height/4), color="red")

    def create_player_name_box(self, x: int, y: int, text="You", color="green"):
        """
        Utility function to add a box on the canvas with a player's name.
        :param x: The x coordinate to place the name at.
        :param y: The y coordinate to place the name at.
        :param text: The text to place.
        :param color: The color to use for the text.
        :return: A reference to the text box created.
        """
        return self.create_text(x, y, text=text, fill=color, width=int(self.width/2))

    def create_score_box(self, x, y, color="blue"):
        """
        Utility function to add a box to show the score of a player.
        Score starts out at 0.
        :param x: The x coordinate to place the score at.
        :param y: The y coordinate to place the score at.
        :param color: The color to use for the score.
        :return: Reference to the text box for the score.
        """
        return self.create_text(x, y, text="0", fill=color, width=int(self.width/4))

    def set_player_1_name(self, name):
        """
        Utility function to set the name of the first player.
        :param name: Name to set.
        :return: None
        """
        self.set_text(self.player1_name, name)

    def set_player_2_name(self, name):
        """
        Utility function to set the name of the second player.
        :param name: Name to set.
        :return: None
        """
        self.set_text(self.player2_name, name)

    def set_score_1(self, new_score):
        """
        Utility function to set the score of the first player.
        :param new_score: Score to set
        :return: None
        """
        self.score_1 = new_score
        self.set_text(self.score_box_1, self.score_1)

    def set_score_2(self, new_score):
        """
        Utility function to set the score of the second player.
        :param new_score: Score to set
        :return: None
        """
        self.score_2 = new_score
        self.set_text(self.score_box_2, self.score_2)

    def increment_score_1(self, inc=1):
        """
        Utility function to increment the current score of the first player.
        :param inc: Points to increment by. Default=1
        :return: None
        """
        self.set_score_1(self.score_1 + inc)

    def increment_score_2(self, inc=1):
        """
        Utility function to increment the current score of the second player.
        :param inc: Points to increment by. Default=1
        :return: None
        """
        self.set_score_2(self.score_2 + inc)

    def reset_scores(self):
        """
        Utility function to reset the scores of both players to 0.
        :return: None
        """
        self.set_score_1(0)
        self.set_score_2(0)

    def set_text(self, component, text):
        """
        Utility function used by above functions to set the text of a component on the canvas.
        :param component: Component whose text to change.
        :param text: Text to set in the component.
        :return: None
        """
        self.itemconfig(component, text=str(text))


