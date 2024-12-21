from tkinter import Label, Frame, Button, Toplevel
from constants.labels import LABEL_NAMES

# LLM used heavily here
class LeaderboardUI:
    """ Class for the leaderboard UI

    Attributes:
        root: main window
        game_repository: game repository
        scoreboard_repository: scoreboard repository
        score_frame: frame for the leaderboard
        score_labels: list of labels for the leaderboard
        score_buttons: list of buttons for the leaderboard
    """
    def __init__(self, root, game_repository, scoreboard_repository):
        """ Constructor for the LeaderboardUI class

        Args:
            root: main window
            game_repository: game repository
            scoreboard_repository: scoreboard repository
            """
        self.root = root
        self.game_repository = game_repository
        self.scoreboard_repository = scoreboard_repository
        self.score_frame = Frame(
            self.root,
            bg="white",
            highlightbackground="gray",
            highlightthickness=1
        )
        self.score_frame.grid(row=1, column=5, rowspan=15, padx=20)

        header = Label(
            self.score_frame,
            text="Top 10 tulokset:",
            font=("TkDefaultFont", 12, "bold"),
            bg="white",
            borderwidth=1,
            relief="solid",
            width=20,
            pady=5
        )
        header.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.score_labels = []
        self.score_buttons = []
        self.update_scores()

    def show_game_details(self, game):
      """ Näyttää pelin tulokset erillisessä ikkunassa

      Args:
          game_id: pelin id
          player_name: pelaajan nimi
      """
      scoreboard_data = self.scoreboard_repository.find_by_game_id(game["id"])
      if not scoreboard_data:
          print("No scoreboard data found for game", game["id"])
          return

      detail_window = Toplevel(self.root)
      detail_window.title("Pelin tulokset")
      detail_window.configure(bg="white")

      # Convert scores string back to list
      scores = scoreboard_data['scores'].split(',')

      # Header
      Label(
          detail_window,
          text=f"{game['player_name']}, {game['total_score']} pistettä",
          font=("TkDefaultFont", 12, "bold"),
          bg="white",
          pady=10
      ).pack()

      # Date played
      Label(
          detail_window,
          text=f"Pelattu: {game['timestamp']}",
          font=("TkDefaultFont", 10),
          bg="white",
          pady=5
      ).pack()

      # Create frame for scores
      scores_frame = Frame(detail_window, bg="white")
      scores_frame.pack(padx=20, pady=10)

      row = 0
      # Display upper section (0-5)
      for i in range(6):
          Label(
              scores_frame,
              text=LABEL_NAMES[i],
              font=("TkDefaultFont", 10),
              bg="white",
              anchor="w",
              width=20
          ).grid(row=row, column=0, padx=5, sticky="w")

          Label(
              scores_frame,
              text=scores[i],
              font=("TkDefaultFont", 12),
              bg="white",
              width=8,
              relief="solid",
              borderwidth=1
          ).grid(row=row, column=1, padx=5, pady=2)
          row += 1

      # Display bonus
      Label(
          scores_frame,
          text="Bonus (+50 jos 63p)",
          font=("TkDefaultFont", 10),
          bg="white",
          anchor="w",
          width=20
      ).grid(row=row, column=0, padx=5, sticky="w")

      valid_scores = [int(score) for score in scores[:6] if score.isdigit()]
      bonus = "50" if sum(valid_scores) >= 63 else "-"

      Label(
          scores_frame,
          text=bonus,
          font=("TkDefaultFont", 12),
          bg="white",
          width=8,
          relief="solid",
          borderwidth=1
      ).grid(row=row, column=1, padx=5, pady=2)
      row += 1

      # Display lower section (6-14)
      for i in range(6, 15):
          Label(
              scores_frame,
              text=LABEL_NAMES[i],
              font=("TkDefaultFont", 10),
              bg="white",
              anchor="w",
              width=20
          ).grid(row=row, column=0, padx=5, sticky="w")

          Label(
              scores_frame,
              text=scores[i],
              font=("TkDefaultFont", 12),
              bg="white",
              width=8,
              relief="solid",
              borderwidth=1
          ).grid(row=row, column=1, padx=5, pady=2)
          row += 1

      # Display total score
      Label(
          scores_frame,
          text="Kokonaistulos:",
          font=("TkDefaultFont", 12, "bold"),
          bg="white",
          anchor="w",
          width=20
      ).grid(row=row, column=0, padx=5, pady=10, sticky="w")

      Label(
          scores_frame,
          text=str(game['total_score']),
          font=("TkDefaultFont", 12, "bold"),
          bg="white",
          width=8,
          relief="solid",
          borderwidth=1
      ).grid(row=row, column=1, padx=5, pady=10)


    def update_scores(self):
        """ Päivittää tulostaulun """
        for label in self.score_labels:
            label.destroy()
        for button in self.score_buttons:
            button.destroy()
        self.score_labels.clear()
        self.score_buttons.clear()

        games = self.game_repository.find_all()[:10]
        MAX_ROWS = 10

        for i in range(1, MAX_ROWS + 1):
            bg_color = "#f0f0f0" if i % 2 == 0 else "white"

            if i <= len(games):
                rank_text = f"{i}."
                player_name = games[i-1]['player_name']
                score_text = f"{games[i-1]['total_score']} pistettä"
                timestamp = games[i-1]['timestamp']
                game_id = games[i-1]['id']
            else:
                rank_text = f"{i}."
                player_name = "---"
                score_text = "---"
                game_id = None

            # Rank label
            rank_label = Label(
                self.score_frame,
                text=rank_text,
                font=("TkDefaultFont", 11),
                bg=bg_color,
                borderwidth=1,
                relief="solid",
                anchor="center",
                width=2,
                padx=5
            )
            rank_label.grid(row=i, column=0, sticky="ew")
            self.score_labels.append(rank_label)

            # Player name label
            name_label = Label(
                self.score_frame,
                text=player_name,
                font=("TkDefaultFont", 11),
                bg=bg_color,
                borderwidth=1,
                relief="solid",
                width=10,
                anchor="center",
                padx=5
            )
            name_label.grid(row=i, column=1, sticky="ew")
            self.score_labels.append(name_label)

            # Score label
            score_label = Label(
                self.score_frame,
                text=score_text,
                font=("TkDefaultFont", 11),
                bg=bg_color,
                borderwidth=1,
                relief="solid",
                width=12,
                anchor="center",
                padx=5
            )
            score_label.grid(row=i, column=2, sticky="ew")
            self.score_labels.append(score_label)

            if game_id is not None:
                button = Button(
                    self.score_frame,
                    text="Näytä",
                    font=("TkDefaultFont", 9),
                    command=lambda game=games[i-1]:
                        self.show_game_details(game)
                )
                button.grid(row=i, column=3, padx=5)
                self.score_buttons.append(button)
