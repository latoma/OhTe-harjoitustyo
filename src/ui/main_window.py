from tkinter import Tk, Button, Label, DISABLED, S, E, Toplevel, Text
from constants.labels import LABEL_NAMES, LABEL_KEYS, INSTRUCTIONS

class MainWindow(Tk):
    """ Luokka joka vastaa pelin päänäkymästä

    Attributes:
        roll_button: heitä-nappula
        throws_left_label: jäljellä olevien heittojen label
        select_buttons: lista pistevalintojen nappuloista
        save_score_button: pisteytä-nappula
        """
    def __init__(self, test_mode=False):
        super().__init__()
        self.configure(bg="white")
        self.title("Yatzy")
        self.geometry("1000x800")

        # Game title
        self.__game_title_label = Label(self, text='Yatzy!', font="lucida 40 bold italic", foreground='yellow', bg='magenta')
        self.__game_title_label.grid(row=0, column=5, columnspan=2, pady=11, padx=32)
        Label(self, text='Single Player', font="lucida 9 bold italic", foreground='yellow', bg='magenta')\
            .grid(row=0, column=5, columnspan=2, sticky=S + E, padx=25)

        # Instructions button
        self.instructions_button = Button(self, text="Ohjeet", font=("TkDefaultFont", 12), command=self.show_instructions)
        self.instructions_button.grid(row=1, column=5, columnspan=2, pady=10)

        #Roll button
        self.roll_button = Button(self, text="Heitä nopat", bg="lightgray", font=("TkDefaultFont", 12))
        self.roll_button.grid(row=2, column=2, pady=10)

        # Throws left label
        self.throws_left_label = Label(self, text="Heittoja: 3",
                                  font=("TkDefaultFont", 12))
        self.throws_left_label.grid(row=2, column=1, pady=10, padx=10)

        # Score selection buttons
        self.select_buttons = []
        self.create_score_buttons()

        if test_mode:
            self.save_score_button = Button(
                self,
                text="Pisteytä",
                font=("TkDefaultFont", 12),
            )
            self.save_score_button.grid(
                row=20, column=3,
                padx=5, pady=5,
                sticky="ew"
            )

    def show_instructions(self):
        """ Näyttää ohjeet uudessa ikkunassa """
        instructions_window = Toplevel(self)
        instructions_window.title("Ohjeet")
        instructions_window.geometry("800x500")
        instructions_text = Text(instructions_window, wrap="word")
        instructions_text.insert("1.0", "\n".join(INSTRUCTIONS))
        instructions_text.config(state=DISABLED)
        instructions_text.pack(expand=True, fill="both")

    def create_score_buttons(self):
        """ Luo pistevalintojen nappulat """
        row = 3
        for _ in LABEL_NAMES:
            # Skip bonus row
            if row == 9:
                row += 1

            select_button = Button(
                self,
                text="",
                state=DISABLED,
                relief="flat",
                bg="white"
            )
            select_button.grid(row=row, column=3, padx=5)
            self.select_buttons.append(select_button)
            row += 1

    def create_new_game_button(self, command):
        """ Luo uusi peli -nappula

        Args:
            command: funktio (joka käynnistää uuden pelin)
        """
        self.new_game_button = Button(
            self,
            text="Uusi peli",
            font=("TkDefaultFont", 12),
            bg="green",
            command=command
        )
        self.new_game_button.grid(
            row=20, column=3,
            padx=5, pady=5,
            sticky="ew"
        )

    def remove_new_game_button(self):
        if hasattr(self, 'new_game_button'):
            self.new_game_button.destroy()
            del self.new_game_button

    def set_roll_command(self, command):
        self.roll_button.configure(command=command)

    def set_select_commands(self, command_factory):
        """ Asettaa pistevalintojen komennot

        Args:
            command_factory: funktio joka palauttaa komennon
        """
        for i, key in enumerate(LABEL_KEYS):
            self.select_buttons[i].configure(
                command=command_factory(key)
            )

    def set_save_score_command(self, command):
        self.save_score_button.config(command=command)

    def update_throws_left(self, throws):
        self.throws_left_label.config(text=f"Heittoja: {throws}")

    def reset_select_button_appearence(self):
        for button in self.select_buttons:
            button.config(
                text="",
                state=DISABLED,
                relief="flat",
                bg="white"
                )
