import tkinter


class PopupDialogBox:
    """
    Class to create a popup dialog box during the box for various functions such as entering your name,
    joining game on a network IP address, etc.
    Reference: https://stackoverflow.com/questions/10020885/creating-a-popup-message-box-with-an-entry-field
    @author sahil1105
    """
    def __init__(self, master, prompt, textbox_1_prompt="", textbox_2_prompt="", button_prompt="OK"):
        """
        Constructor for Pop up dialog box.
        :param master: The Frame to attach to.
        :param prompt: The message to show the user.
        :param button_prompt: The message on the button.
        :param textbox_1_prompt: Prompt to add to the text box
        :param textbox_2_prompt: Prompt to add to the second text box
        """
        self.top = tkinter.Toplevel(master)
        self.label = tkinter.Label(self.top, text=prompt)
        self.label.pack()
        self.entry_box_1 = tkinter.Entry(self.top, width=30, state=tkinter.NORMAL)
        self.entry_box_1.pack()
        self.entry_box_2 = tkinter.Entry(self.top, width=30, state=tkinter.NORMAL)
        self.entry_box_2.pack()
        self.entered_value_1 = None
        self.entered_value_2 = None
        self.ok_button = tkinter.Button(self.top, text=button_prompt, command=self.validate_and_exit)
        self.ok_button.pack()
        self.entry_box_1.insert(tkinter.END, textbox_1_prompt)
        self.entry_box_2.insert(tkinter.END, textbox_2_prompt)

    def validate_and_exit(self):
        """
        Default callback function for the button on the pop-up dialog box.
        :return:
        """
        self.entered_value_1 = self.entry_box_1.get()  # Store the entered value to be used by the controller.
        self.entered_value_2 = self.entry_box_2.get()
        self.top.destroy()  # Close this pop-up dialog box

