import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti
class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.rikas_maksukortti = Maksukortti(1000)
        self.koyha_maksukortti = Maksukortti(200)

    def test_kassapaate_init_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_maukas_onnistunut_kateisosto(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500),100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_edullinen_onnistunut_kateisosto(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(340),100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_maukas_epaonnistunut_kateisosto(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(100),100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullinen_epaonnistunut_kateisosto(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100),100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        
    def test_maukas_onnistunut_korttiosto(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.rikas_maksukortti),True)
        self.assertEqual(str(self.rikas_maksukortti),"Kortilla on rahaa 6.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullinen_onnistunut_korttiosto(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.rikas_maksukortti),True)
        self.assertEqual(str(self.rikas_maksukortti),"Kortilla on rahaa 7.60 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_epaonnistunut_korttiosto(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.koyha_maksukortti),False)
        self.assertEqual(str(self.koyha_maksukortti),"Kortilla on rahaa 2.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullinen_epaonnistunut_korttiosto(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.koyha_maksukortti),False)
        self.assertEqual(str(self.koyha_maksukortti),"Kortilla on rahaa 2.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kortille_rahan_lataaminen(self):
        self.kassapaate.lataa_rahaa_kortille(self.koyha_maksukortti,200)
        self.assertEqual(str(self.koyha_maksukortti),"Kortilla on rahaa 4.00 euroa")

    def test_kortille_rahan_lataaminen_nollasumma(self):
        self.kassapaate.lataa_rahaa_kortille(self.koyha_maksukortti,-200)
        self.assertEqual(str(self.koyha_maksukortti),"Kortilla on rahaa 2.00 euroa")
        