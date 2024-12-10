# Architecture

```mermaid
classDiagram
    Yatzy "1" --> "1" Dice
    Yatzy "1" --> "1" Scoreboard
    Yatzy "1" --> "1" GameRepository
    Yatzy "1" --> "1" ScoreboardRepository

    Dice "1" --> "5" Die

    class Yatzy {
        -dice: Dice
        -scoreboard: Scoreboard
        -game_repository: GameRepository
        -scoreboard_repository: ScoreboardRepository
        +roll_dice()
        +select_score()
        +end_game()
        +start_new_game()
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
        +toggle_hold()
    }

    class Scoreboard {
        -scores: dict
        +calculate_score()
        +set_score()
        +get_total_score()
    }

    class GameRepository {
        -connection
        +create()
        +find_all()
    }

    class ScoreboardRepository {
        -connection
        +create()
        +find_by_game_id()
    }

```

## Nopan heitto ja tuloksen valitseminen
```mermaid
sequenceDiagram
    participant Y as Yatzy
    participant D as Dice
    participant Die as Die
    participant S as Scoreboard

    Y->>D: roll_dice()
    D->>Die: roll()
    Die-->>D: new value
    D-->>Y: dice rolled

    Y->>S: get_possible_scores(dice)
    S->>D: get_values()
    D-->>S: [dice values]
    S->>S: calculate_score()
    S-->>Y: possible scores

    Y->>S: set_score(label, score) (User selected score)
    S->>S: update scores

```
