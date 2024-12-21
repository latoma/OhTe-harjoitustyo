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
poetry run invoke coverage-report
```
![Screenshot 2024-12-20 191100](https://github.com/user-attachments/assets/c4dbfb9f-7e21-474d-a499-7c857b68dc45)
