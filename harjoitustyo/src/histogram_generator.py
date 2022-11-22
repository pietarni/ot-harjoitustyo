from PIL import Image
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage import data,exposure
import matplotlib.pyplot as plt
class HistogramGenerator:
    def __init__(self, path):
        #Temporary test and example source data
        self.path = path
        
        #Temporary hard-coded values, got from source data.
        self.min_data_X = 25498000
        self.min_data_Y = 6677000

        self.max_data_X = 25499000
        self.max_data_Y = 6678000

        self.len_data_X = self.max_data_X - self.min_data_X
        self.len_data_Y = self.max_data_Y - self.min_data_Y

    #Creates histogram of oriented gradients from heightmap
    def create_hog(self):

        img = Image.new('RGB', (self.len_data_X + 1,self.len_data_Y + 1), "black") # Create a new black image
        pixels = img.load()
        try:
            with open(self.path) as infile:
                for line in infile:
                    splitline = line.split(" ")
                    #Get X,Y,Z values from data, put into image
                    xval = int(float(splitline[0]))-self.min_data_X
                    yval = self.len_data_Y-(int(float(splitline[1]))-self.min_data_Y)
                    zval = int(float(splitline[2])*10)

                    pixels[xval,yval] = (zval,zval,zval)
        except:
            print("ERROR: bad path")
            return 0
        img.save("heightmap.png")
        #Create Histogram of oriented gradients from image, we will use these to analyze slopes in the terrain.
        #From documentation of scikit-image: https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html
        hogimg = imread("heightmap.png")
        fd, hog_image = hog(hogimg, orientations=9, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualize=True, channel_axis=-1)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
        ax1.axis('off')
        ax1.imshow(hogimg, cmap=plt.cm.gray)
        ax1.set_title('Input image')
        #Adjust HOG gamma to make it more visible
        hog_image_bright = exposure.adjust_gamma(hog_image, gamma=0.4,gain=1)
        ax2.axis('off')
        ax2.imshow(hog_image_bright, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')
        #Returns 1 if success
        return 1
    
    #Shows the created plot with the heightmap and HOG
    #Will not be tested, since plt.show() pauses code execution until the window is closed.
    def show_hog(self):
        plt.show()