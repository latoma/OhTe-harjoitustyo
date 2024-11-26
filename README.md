# Yatzy-peli

### Aineopintojen harjoitustyö: ohjelmistotekniikka, syksy 2024

Kyseessä on tietokoneella pelattava yksinpeli-versio tunnetusta-Yatzy noppapelistä.



### Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmäärittely.md)
- [Changelog](./dokumentaatio/changelog.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

## Käyttäminen

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

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

Raportti generoituu _htmlcov_-hakemistoon.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```
