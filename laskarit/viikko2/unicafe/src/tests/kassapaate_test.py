import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
    
    def test_luotu_kassapaate_rahaa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_luotu_kassapaate_rahaa_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_luotu_kassapaate_edulliset(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_luotu_kassapaate_maukkaat(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullisesti_kateisella(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_edullisesti_kateisella_vaihtoraha(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)

    def test_edullisesti_kateisella_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)

    def test_maukkaasti_kateisella(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_maukkaasti_kateisella_vaihtoraha(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)

    def test_maukkaasti_kateisella_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(390), 390)

    def test_edulliset_maara_kasvaa_kateisella(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukkaat_maara_kasvaa_kateisella(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edulliset_maara_ei_kasva_kateisella(self):
        self.kassapaate.syo_edullisesti_kateisella(230)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_maukkaat_maara_ei_kasva_kateisella(self):
        self.kassapaate.syo_maukkaasti_kateisella(390)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_edullisesti_kortilla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 760)

    def test_edullisesti_kortilla2(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)

    def test_edullisesti_kortilla_ei_riita(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)


    def test_maukkaasti_kortilla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 600)

    def test_maukkaasti_kortilla2(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)

    def test_maukkaasti_kortilla_ei_riita(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)

    def test_edulliset_maara_kasvaa_kortilla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edulliset_maara_ei_kasva_kasvaa_kortilla(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukkaat_maara_kasvaa_kortilla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukkaat_maara_ei_kasva_kasvaa_kortilla(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_rahan_lataus_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.maksukortti.saldo, 1100)

    def test_rahan_lataus_kortille2(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)
    
    def test_rahan_lataus_kortille_negatiivinen(self):
        self.assertEqual(self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100), None)


    

    
    

    
