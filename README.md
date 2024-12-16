# Yatzy-peli

### Aineopintojen harjoitustyö: ohjelmistotekniikka, syksy 2024

Kyseessä on tietokoneella pelattava yksinpeli versio tunnetusta Yatzy-noppapelistä.



### Dokumentaatio
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmäärittely.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)

## Asennus ja Käyttö

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Alusta/tyjennä tietokanta
   
```bash
python3 ./src/initialize_database.py
```

3. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

4. Sovelluksen voi myös käynnistää "testi-tilassa" seuraavasti:

```bash
poetry run invoke start-test-mode
```
(Testi tilassa heitoja on loputtomasti ja pelin voi pisteyttää halutessaan. Helpottaa ominaisuuksien testaamista)


### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti avautuu selaimeen automaattisesti.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```
