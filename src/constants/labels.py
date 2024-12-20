LABEL_NAMES = [
  'Ykköset (5)', 'Kakkoset (10)', 'Kolmoset (15)', 'Neloset (20)', 'Vitoset (25)',
  'Kutoset (30)', 'Yksi pari (12)', 'Kaksi paria (22)', 'Kolmiluku (18)',
  'Neliluku (24)', 'Täyskäsi (28)', 'Pieni suora (15)', 'Iso suora (20)',
  'Sattuma (30)','Yatzy (50)'
]

LABEL_KEYS = [
  'ykköset', 'kakkoset', 'kolmoset', 'neloset', 'vitoset', 'kutoset',
  'yksi_pari', 'kaksi_paria', 'kolmiluku', 'neliluku',
  'täyskäsi', 'pieni_suora', 'iso_suora', 'sattuma', 'yatzy'
]

INSTRUCTIONS = ["OHJEET:\n"
        "1. Paina 'HEITÄ' heittääksesi noppia. Sinulla on 3 heittoa per vuoro\n"
        "   - Jokaisen heiton jälkeen voit valita mitkä nopat haluat pitää (pidä-näppäimellä) "
        "ja mitkä heität uudelleen\n"
        "2. Kun haluat pisteyttää kierroksen, valitse haluamasi tulos 'valitse'-näppäimellä\n"
        "3. Kolmannen heiton jälkeen, jokin pisteytys on pakko valita, "
        "jolloin myös nolla-pisteet ovat valittavissa (punaiset valitse-näppäimet)\n"
        "4. Kun kierroksia on kulunut 15, peli päättyy. "
        "Voit tallentaa tuloksen kirjoittamalla nimesi näkyviin tulevaan laatikkoon.\n"
        "\n"
        "PISTEYTYSTEN SELITYKSET:\n"
        "(Selitykset löytyvät myös taulukosta '?'-näppäimen takaa)\n"
        "Ykköset-Kutoset: Noppien summa, joissa on kyseinen numero\n"
        "Bonus: Jos ykköset-kutoset ovat yhteensä 63p tai enemmän, saat 50 pistettä\n"
        "Pari: Kaksi noppaa, joissa on sama numero\n"
        "Kolmiluku: Kolme noppaa, joissa on sama numero\n"
        "Neliluku: Neljä noppaa, joissa on sama numero\n"
        "Täyskäsi: Kolmiluku + pari\n"
        "Pieni Suora: Nopat sisältävät numerot 1:stä 5:een\n"
        "Iso Suora: Nopat sisältävät numerot 2:sta 6:een\n"
        "Sattuma: Kaikkien noppien summa\n"
        "Yatzy: Kaikki viisi noppaa ovat samaa numero. Antaa 50 pistettä\n"
        "\n"
        "Onnea peliin, sitä tarvitset!\n"
        "\n"
        "Tekijä: Toma Lahtinen\n"
        ]

SCORE_EXPLANATION = {
  'Ykköset (5)': 'Ykköset: Noppien summa, joissa on numero 1. (Max 5 pistettä)',
  'Kakkoset (10)': 'Kakkoset: Noppien summa, joissa on numero 2. (Max 10 pistettä)',
  'Kolmoset (15)': 'Kolmoset: Noppien summa, joissa on numero 3. (Max 15 pistettä)',
  'Neloset (20)': 'Neloset: Noppien summa, joissa on numero 4. (Max 20 pistettä)',
  'Vitoset (25)': 'Vitoset: Noppien summa, joissa on numero 5. (Max 25 pistettä)',
  'Kutoset (30)': 'Kutoset: Noppien summa, joissa on numero 6. (Max 30 pistettä)',
  'Bonus': 'Bonus: Jos yläkerran summa (ykköset -> kutoset) on yhteensä 63p tai enemmän, '
  'saat 50 bonus pistettä)',
  'Yksi pari (12)': 'Yksi pari: Kaksi noppaa, joissa on sama numero. (Max 12 pistettä)',
  'Kaksi paria (22)': 'Kaksi paria: Kaksi erilukuista paria. (Max 22 pistettä)',
  'Kolmiluku (18)': 'Kolmiluku: Kolme noppaa, joissa on sama numero. (Max 18 pistettä)',
  'Neliluku (24)': 'Neliluku: Neljä noppaa, joissa on sama numero. (Max 24 pistettä)',
  'Täyskäsi (28)': 'Täyskäsi: Kolmiluku + pari. (Max 28 pistettä)',
  'Pieni suora (15)': 'Pieni suora: Nopat sisältävät numerot 1, 2, 3, 4, 5. (15 pistettä)',
  'Iso suora (20)': 'Iso suora: Nopat sisältävät numerot 2, 3, 4, 5, 6. (20 pistettä)',
  'Sattuma (30)': 'Sattuma: Kaikkien noppien summa. (Max 30 pistettä)',
  'Yatzy (50)': 'Yatzy: Kaikki viisi noppaa ovat samaa numeroa. (50 pistettä)'
}
