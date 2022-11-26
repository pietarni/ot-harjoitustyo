from PIL import Image

class SimulationUnit:
    def __init__(self, position, hog, roadmap, resultimg):
        self.pos = position
        self.hog = hog
        self.roadmap = roadmap
        self.resultimg = resultimg
        self.hog_lengthx = np.shape(hog_features)[0]
        self.hog_lengthy = np.shape(hog_features)[1]
    
    def ride(self):

    def current_hog_tile(self):
        return(self.hog[ int(self.pos[0]/self.hog_lengthx) ][ int(self.pos[1]/self.hog_lengthy) ][0][0])
    
    def current_tile_is_safe(self):
        return(self.roadmap[ int(self.pos[0]) ][ int(self.pos[1]) ] == (255,255,255,0))


    
