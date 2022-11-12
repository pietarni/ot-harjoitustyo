import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_alku_saldo_oikein(self):
        self.assertEqual(str(self.maksukortti),"Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataaminen(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(str(self.maksukortti),"Kortilla on rahaa 20.00 euroa")

    def test_rahan_ottaminen(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 5.00 euroa")
        self.assertEqual(self.maksukortti.ota_rahaa(2000), False)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 5.00 euroa")

