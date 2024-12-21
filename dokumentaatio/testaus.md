# Testaaminen

Ohjelmaa on testattu sekä  yksikkö- ja integraatiotestein unittestillä.

## Yksikkötestaus
Dice, Die ja Scoreboard luokkien testaus on tehty yksikkötesteillä. Luokat ovat melko suoraviivaisia nykyiseltä toiminnallisuudeltaan, joten samoin on  testitkin.

**Erikoishuomiona** scoreboard_test:istä löytyvä test_get_scores_as_list, joka toimii määrittelmänä sille missä muodossa tuloskortin data tulee palauttaa.

Game- ja Scoreboard-repositoriot on testattu yksikkötestein käyttäen mock-olioita ja testidataa. Testit varmistavat, että molempien repositorioiden haku- ja tallennusmenetelmät toimivat perustasolla.

## Integraatiotestaus
Yatzy.py on vastuussa pelin kulusta ja moduulien välisestä yhteistoiminnasta, jonka takia integraatiotestaus sopii siihen paremmin. Testeissä testataan noppien heittämisen sekä tuloksen valitsemisen perustoiminnallisuutta. Testit käyttävät testitietokantaa

## Testikattavuus
```bash
# (databases are initialized with python3 ./src/initialize_database.py)
poetry run invoke coverage-report
```

![Screenshot 2024-12-21 154817](https://github.com/user-attachments/assets/26ae45ea-6829-4a0f-a0dc-4651f4449c41)
