import unittest
from histogram_generator import HistogramGenerator

class TestHistogramGenerator(unittest.TestCase):
    def setUp(self):
        #Temporary hardcoded example path
        path = "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/1x1m_677498.xyz"
        self.histogramGenerator = HistogramGenerator(path)
    
    def test_histogramGenerator_works_with_existing_path(self):
        self.assertEqual(self.histogramGenerator.create_hog(),1)
    
    def test_histogramGenerator_not_work_with_nonexisting_path(self):
        path = "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/bad.xyz"
        histogramGenerator2 = HistogramGenerator(path)
        self.assertEqual(histogramGenerator2.create_hog(),0)