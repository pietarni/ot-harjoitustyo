import unittest
from data_handler import DataHandler
import pathlib


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        # Input folder:
        self.directory = str(pathlib.Path(__file__).parent.parent.resolve())
        self.inputpath = self.directory+"/input/"
        self.zippath = self.inputpath + "Greater-helsinki-3.zip"
        #hardcorded example url
        elevationdataurl = "https://kartta.hel.fi/helshares/karkeamalli/1x1m/1x1m_677498.xyz"
        jsonpath = self.inputpath + "indeksi.json"
        self.data_handler = DataHandler(
        elevationdataurl,self.inputpath ,[7,7], self.zippath)

    def test_elevation_map_generation_works_with_existing_path(self):
        self.assertRaises(ValueError,self.data_handler.setup_data())
        try:
            self.data_handler.setup_data()
        except Exception:
            self.fail("setup_data() raised "+Exception+" unexpectedly!")

    def test_elevation_map_generation_not_work_with_nonexisting_path(self):
        bad_url = "https://kartta.hel.fi/helshares/karkeamalli/1x1m/1x1m_6774989999.xyz"
        dataHandler2 = DataHandler(bad_url,self.inputpath,[7,7],self.zippath)
        try:
            dataHandler2.setup_data()
        except Exception:
            self.fail("setup_data() raised "+Exception+" unexpectedly!")
