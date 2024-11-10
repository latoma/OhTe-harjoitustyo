import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):
  def setUp(self):
    self.kassa = Kassapaate()
    self.kortti = Maksukortti(1000)

  def test_kassa_on_luotu(self):
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)
    self.assertEqual(self.kassa.edulliset, 0)
    self.assertEqual(self.kassa.maukkaat, 0)
  
  def test_kateisosto_toimii_edullisesti(self):
    self.assertEqual(self.kassa.syo_edullisesti_kateisella(240), 0)
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000 + 2.4)
    self.assertEqual(self.kassa.edulliset, 1)
  
  def test_kateisosto_toimii_maukkaasti(self):
    self.assertEqual(self.kassa.syo_maukkaasti_kateisella(400), 0)
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000 + 4.0)
    self.assertEqual(self.kassa.maukkaat, 1)

  def test_kateisosto_ei_toimi_edullisesti(self):
    self.assertEqual(self.kassa.syo_edullisesti_kateisella(100), 100)
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)
    self.assertEqual(self.kassa.edulliset, 0)

  def test_kateisosto_ei_toimi_maukkaasti(self):
    self.assertEqual(self.kassa.syo_maukkaasti_kateisella(200), 200)
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)
    self.assertEqual(self.kassa.maukkaat, 0)
  
  def test_korttiosto_toimii_edullisesti(self):
    self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)
    self.assertEqual(self.kortti.saldo_euroina(), 7.6)
    self.assertEqual(self.kassa.edulliset, 1)
  
  def test_korttiosto_toimii_maukkaasti(self):
    self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)
    self.assertEqual(self.kortti.saldo_euroina(), 6.0)
    self.assertEqual(self.kassa.maukkaat, 1)
  
  def test_korttiosto_ei_toimi_edullisesti(self):
    kortti = Maksukortti(100)
    self.assertEqual(self.kassa.syo_edullisesti_kortilla(kortti), False)
    self.assertEqual(kortti.saldo_euroina(), 1.0)
    self.assertEqual(self.kassa.edulliset, 0)

  def test_korttiosto_ei_toimi_maukkaasti(self):
    kortti = Maksukortti(200)
    self.assertEqual(self.kassa.syo_maukkaasti_kortilla(kortti), False)
    self.assertEqual(kortti.saldo_euroina(), 2.0)
    self.assertEqual(self.kassa.maukkaat, 0)

  def test_lataa_rahaa_kortille_toimii(self):
    self.kassa.lataa_rahaa_kortille(self.kortti, 500)
    self.assertEqual(self.kortti.saldo_euroina(), 15.0)
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000 + 5.0)

  def test_lataa_rahaa_kortille_ei_toimi(self):
    self.kassa.lataa_rahaa_kortille(self.kortti, -500)
    self.assertEqual(self.kortti.saldo_euroina(), 10.0)
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)
