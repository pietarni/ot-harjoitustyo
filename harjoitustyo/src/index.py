from histogram_generator import HistogramGenerator
#Temporary hardcoded example path
path =  "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/1x1m_677498.xyz"
histogramGenerator = HistogramGenerator(path)
histogramGenerator.create_hog()
histogramGenerator.show_hog()