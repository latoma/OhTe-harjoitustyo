from tkinter import Label, PhotoImage, Button
from game.dice import Dice
import random

DICE_IMAGE_FILES = ["src/assets/Die_1.png", "src/assets/Die_2.png", "src/assets/Die_3.png",
                    "src/assets/Die_4.png", "src/assets/Die_5.png", "src/assets/Die_6.png"]

# Animation constants
TEMP_FACE_DELAY = 50  # Delay between temporary faces (milliseconds)
TEMP_FACES_COUNT = 5
FINAL_FACE_DELAY = 250  # Delay before showing final face
NEXT_DIE_DELAY = 50

class DiceUI:
    """Luokka joka vastaa noppien käyttöliittymästä ja animaatiosta

    Attributes:
        root: pääikkuna
        dice: nopat
        dice_images: lista noppien kuvista
        empty_image: tyhjä kuva
        dice_labels: lista noppien kuvista
        hold_buttons: lista noppien pidä-nappuloista
    """

    def __init__(self, root, dice: Dice):
        """ Konstruktori, alustaa noppien käyttöliittymän

        Args:
            root: pääikkuna
            dice: nopat
        """
        self.root = root
        self.dice = dice
        self.dice_images = self.load_dice_images()
        self.empty_image = PhotoImage(width=64, height=64)
        self.dice_labels = self.create_dice_labels()
        self.hold_buttons = self.create_hold_buttons()

    def load_dice_images(self):
        """ Lataa noppien kuvat """
        return [PhotoImage(file=dice_image) for dice_image in DICE_IMAGE_FILES]

    def create_dice_labels(self):
        """ Luo noppien kuvat """
        dice_labels = []
        for column in range(5):
            new_die_label = Label(self.root, image=self.empty_image)
            new_die_label.grid(row=0, column=column, padx=15, pady=5)
            dice_labels.append(new_die_label)
        return dice_labels

    def create_hold_buttons(self):
        """ Luo noppien pidä-nappulat """
        hold_buttons = []
        for column in range(5):
            button = Button(
                self.root,
                text="Pidä",
                command=lambda i=column: self.toggle_hold(i),
                width=6,
                font=("TkDefaultFont", 10)
            )
            button.grid(row=1, column=column, pady=(0, 10))
            hold_buttons.append(button)
        return hold_buttons

    def toggle_hold(self, die_index):
        """ Vaihtaa nopan pidä-tilan

        Args:
            die_index: nopan indeksi
        """
        self.dice._Dice__dice[die_index].toggle_hold_status()
        self.update_hold_buttons()
        self.update_display()

    def update_hold_buttons(self):
        """ Päivittää pidä-nappuloiden tilan """
        for i, die in enumerate(self.dice._Dice__dice):
            button = self.hold_buttons[i]
            if die.in_hold():
                button.config(relief="sunken", bg="lightgray", text="Pidossa")
            else:
                button.config(relief="raised", bg="#f0f0f0", text="Pidä")

            if die.is_locked():
                button.config(state="disabled")
            else:
                button.config(state="normal")

    # LLM-used making this method
    def animate_roll(self, completion_callback=None):
        """Animates dice roll one die at a time with completion callback"""
        non_held_indices = [i for i, die in enumerate(self.dice._Dice__dice) if not die.in_hold()]
        final_values = [die.get_value() for die in self.dice._Dice__dice]

        def animate_single_die(die_index, remaining_indices):
            if not remaining_indices:
                if completion_callback:
                    completion_callback()
                return

            current_die = remaining_indices[0]

            for step in range(TEMP_FACES_COUNT):
                def show_temp(step):
                    temp_value = random.randint(1, 6)
                    self.dice_labels[current_die].configure(
                        image=self.dice_images[temp_value-1]
                    )
                self.dice_labels[current_die].after(step * TEMP_FACE_DELAY, lambda s=step: show_temp(s))

            def show_final():
                self.dice_labels[current_die].configure(
                    image=self.dice_images[final_values[current_die]-1]
                )
                if len(remaining_indices) > 1:
                    self.dice_labels[current_die].after(
                        NEXT_DIE_DELAY,
                        lambda: animate_single_die(current_die, remaining_indices[1:])
                    )
                else:
                    animate_single_die(current_die, [])

            self.dice_labels[current_die].after(FINAL_FACE_DELAY, show_final)

        if non_held_indices:
            animate_single_die(non_held_indices[0], non_held_indices)

    def update_display(self):
        """ Päivittää noppien kuvat """
        for i, die in enumerate(self.dice._Dice__dice):
            value = die.get_value()
            if value > 0:
                self.dice_labels[i].configure(
                    image=self.dice_images[value-1],
                    bg='gray' if die.in_hold() else 'white'
                )

    def reset_holds(self):
        """ Nollaa pidä-tilan """
        self.dice.reset_holds()
        self.update_hold_buttons()
        self.update_display()

    def prepare_dice_for_next_round(self):
        """ Valmistelee nopat seuraavaa kierrosta varten """
        self.reset_holds()
        self.dice.lock_dice()
        self.update_hold_buttons()
        self.update_display()
