import json

class ResultDataCreator:
    def __init__(self):

        self.features = []
    
    def add_path(self,path,travel_time,travel_distance,max_speed,median_speed,max_speedChange):
        new_feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": []
        },
        "geometry_name":"wkb_geometry",
        "properties":{
            "travel_time":travel_time,
            "travel_distance":travel_distance,
            "max_speed":max_speed,
            "median_speed":median_speed,
            "max_speed_change":max_speedChange
        }
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