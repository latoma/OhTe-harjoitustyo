# Architecture
Yatzy-luokka vastaa pelin kulusta, käyttöliittymän hallinnasta ja luokkien välisestä toiminnallisuudesta.
Yatzyn konstruktorissa alustetaan tietokanta, pelilogiikan moduulit ja niiden käyttöliittymät.
Yatzy sisältää metodeina pelin päätoiminnot, jotka ovat: noppien heitto (roll_dice), tuloksen valitseminen (select_score), pelin loppuminen (end_game) ja uuden pelin aloittaminen (start_new_game).
Tuloksen valitsemisen yhteydessä tarkistetaan onko 15 kierrosta tullut täyteen, jolloin peli päättyy. Tällöin kutsuttava metodi (end_game) vastaa nimimerkin kysymisestä ja tuloksen tallentamisesta tietokantaan-
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

## Käyttöliittymä

Käyttöliittymä koostuu yhdestä pääikkunasta jossa on näkyvissä nopat, tulostaulu, näiden painikkeet, sekä top 10 tulokset.

Nopilla (Dice) ja tulostaululla (Scoreboard) on omat erilliset käyttöliittymä tiedostot Dice_ui.py ja Scoreboard_ui.py, jotka löytyvät /ui kansiosta. Näiden lisäksi sieltä löytyy leaderboard_ui.py joka vastaa parhaan 10 tuloksen lista-näkymästä.

Main_window.py tiedosto vastaa pääikkunan perusrakenteen lisäksi sellaisista ui-komponenttien määrittelemisistä, jotka vaativat kommunikointia useamman moduulin kanssa. Esimerkiksi 'valitse'-näppäimet määritellään main_window:ssa, koska niiden painaminen tekee muutoksia sekä Scoreboard_ui:hin että Dice_ui:hin.

Käyttöliittymän yhdistämisesta pelilogiikan kanssa vastaa Yatzy-luokka. Myös aikaisemmin mainittujen main_window:n ui-komponenttien toiminnalisuus määritellään Yatzy:ssa


### Käyttöliittymän rakenne

```mermaid
classDiagram
    Yatzy --> DiceUI
    Yatzy --> ScoreboardUI
    Yatzy --> LeaderboardUI
    Yatzy --> MainWindow

    class Yatzy {
        -main_window: main_window
        -dice_ui: DiceUI
        -scoreboard_ui: ScoreboardUI
        -leaderboard_ui: LeaderboardUI
        -throws_left
        -round
        -test_mode
        +roll_dice()
        +select_score()
        +end_game()
        +ask_player_name()
        +start_new_game()
    }

    class MainWindow {
        +roll_button
        +select_buttons
        +show_instructions()
        +update_throws_left()
    }

    class DiceUI {
        -dice_labels
        -hold_buttons
        +animate_roll()
        +update_display()
    }

    class ScoreboardUI {
        -score_labels
        -bonus_label
        +render_score_options()
        +update_score()
    }

    class LeaderboardUI {
        -score_frame
        -score_labels
        +show_game_details()
        +update_scores()
    }
```


## Tietokannan rakenne
Pelien tiedot tallennetaan SQLite-tietokantaan käyttäen repository suunnittelumallia. Sovelluksella on käytössä kaksi taulua: games ja scoreboards:
- games: tallennetaan pelien perustiedot (nimimerkki, kokonaispisteet, ajankohta)
- scoreboards: tallennetaan yksittäisen pelin tarkemmat pisteytystiedot.
- GameRepository: pelien tallennus/haku
- ScoreboardRepository: pistetaulukoiden tallennus/haku

Päättynyt peli tallennetaan ensin games-tauluun ja
saatu ID käytetään scoreboards-taulussa viiteavaimena.


```mermaid
 classDiagram
      Game "1" --> "1" Scoreboard
      class Game{
          id
          player_name
          total_score
          timestamp
      }
      class Scoreboard{
          id
          game_id ( FK )
          scores
      }
```

## Pelin toiminta-esimerkkejä
### Noppien heitto ja tulosvaihtoehtojen lasku ja valinta
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
    Y->>Y: throws_left -= 1

    Y->>S: get_possible_scores(dice)
    S->>D: get_values()
    D-->>S: [dice values]
    S->>S: calculate_score()
    S-->>Y: possible scores

    Y ->> S: set_score(label, score)
```
