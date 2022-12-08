import json

class ResultDataCreator:
    def __init__(self):

        self.features = []
    def add_path(self,path):
        new_feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": []
        },
        "geometry_name":"wkb_geometry",
        "properties":{}
        }
        new_feature["geometry"]["coordinates"] = path
        self.features.append(new_feature)
    def write_result_json(self, jsonpath):
        # Reads json data, this is specifically for reading the roadmap data.
        with open(jsonpath, 'r') as f:
            data = json.load(f)
        
        data["features"] = self.features
        # Serializing json
        json_object = json.dumps(data, indent=4)
        
        # Writing to sample.json
        with open("results/result.json", "w") as outfile:
            outfile.write(json_object)
        print("done")
        #for element in data["features"]:
        #    