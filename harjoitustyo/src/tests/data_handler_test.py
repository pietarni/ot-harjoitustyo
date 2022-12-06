import unittest
from data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        # Temporary hardcoded example path
        path = "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/1x1m_677498.xyz"
        self.histogramGenerator = HistogramGenerator(path)

    def test_histogramGenerator_works_with_existing_path(self):
        self.assertEqual(self.histogramGenerator.read_elevation_data(), 1)

    def test_histogramGenerator_not_work_with_nonexisting_path(self):
        path = "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/bad.xyz"
        histogramGenerator2 = HistogramGenerator(path)
        self.assertEqual(histogramGenerator2.read_elevation_data(), 0)
