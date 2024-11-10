import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)
        self.kassa = Kassapaate()

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_saldo_asetettu_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 15.0)
    
    def test_saldo_vahenee_oikein_jos_rahaa_tarpeeksi(self):
        self.kassa.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6.0)
    
    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        kortti = Maksukortti(100)
        self.kassa.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(kortti.saldo_euroina(), 1.0)

    def test_palauttaa_true_jos_rahaa_tarpeeksi(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.maksukortti), True)

    def test_palauttaa_false_jos_rahaa_ei_tarpeeksi(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(kortti), False)

    def test_ota_rahaa_palauttaa_true_jos_rahaa_tarpeeksi(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_ota_rahaa_palauttaa_false_jos_rahaa_ei_tarpeeksi(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1500), False)

    def test_string_metodi_palauttaa_oikean_merkkijonon(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
