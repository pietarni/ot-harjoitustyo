from histogram_generator import HistogramGenerator
#Input folder:
inputpath = path =  "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/"

#Temporary hardcoded example path
xyzpath = inputpath + "1x1m_677498.xyz"
histogramGenerator = HistogramGenerator(xyzpath)
jsonpath = inputpath + "roads.json"
histogramGenerator.read_json(jsonpath)
#histogramGenerator.polygon("dsad.png")
#histogramGenerator.create_hog()
#histogramGenerator.show_hog()