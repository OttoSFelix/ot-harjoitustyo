import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_rahan_lataus(self):
        self.maksukortti.lataa_rahaa(200)

        self.assertEqual(self.maksukortti.saldo, 1200)

    def test_saldo_vähenee(self):
        self.maksukortti.ota_rahaa(500)

        self.assertEqual(self.maksukortti.saldo, 500)
    
    def test_saldo_ei_vähene_liiallisella_nostolla(self):
        self.maksukortti.ota_rahaa(1100)

        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_rahat_riittää(self):
        self.assertEqual(self.maksukortti.ota_rahaa(900), True)

    def test_rahat_ei_riitä(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1100), False)

    def test_saldo_euroina(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
    
    def test_str(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")


    