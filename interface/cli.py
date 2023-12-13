import os
import sys
from lib.chroma import collection
from lib.predict import predict, predict_image
from PIL import Image

def start_cli():
    filename = sys.argv[2]
    if os.path.isfile(filename) is not True:
        print ("File no such found")
        
    image = Image.open(filename)
    result = predict_image(image=image)
    if result is None:
        print ("No result found")
    else:
        print (result)