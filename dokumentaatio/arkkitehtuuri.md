# Architecture

```mermaid
classDiagram
    class Yatzy {
        -dice: Dice
        -scoreboard: Scoreboard
        +start()
        +roll_dice()
    }
    class Dice {
        -dice: Die[]
        +roll_dice()
        +get_values()
    }
    class Die {
        -value: int
        -in_hold: bool
        +roll()
        +toggle_hold_status()
    }
    class Scoreboard {
        -scores: dict
        +get_possible_scores()
        +calculate_score()
    }

    Yatzy --> Dice : has
    Yatzy --> Scoreboard : has
    Dice --> Die : has 5
