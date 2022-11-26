from histogram_generator import HistogramGenerator
#Input folder:
inputpath = path =  "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/"

#Temporary hardcoded example path
xyzpath = inputpath + "1x1m_677498.xyz"
histogramGenerator = HistogramGenerator(xyzpath)
histogramGenerator.create_hog()

jsonpath = inputpath + "indeksi.json"
#histogramGenerator.read_json(jsonpath)
#histogramGenerator.get_tiles_within_boundary()

#histogramGenerator.show_hog()
