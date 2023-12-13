import os
import sys
from lib.chroma import collection
from lib.predict import predict
from PIL import Image

def prediction(image: Image):
    embedding = predict(image)
    data = collection.query(query_embeddings = [embedding], n_results = 1)
    name, timestamp = data['ids'][0][0].split("|")
    timestamp = int(timestamp)
    hours = timestamp // 3600
    minutes = timestamp % 3600 / 60
    seconds = (timestamp % 3600) % 60

    return f"{name} {hours}:{minutes}:{seconds} Score: {data['distances'][0][0]}"

def start_cli():
    try:
        filename = sys.argv[0]
    except IndexError:
        print ("No file input")

    if os.path.isfile(filename) is not True:
        print ("File no such found")
    
    image = Image.open(filename)
    result = prediction(image)
    print (result)
