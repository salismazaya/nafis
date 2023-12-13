import os
import sys
from lib.console import Console
from lib.predict import predict_image
from PIL import Image
console = Console()

def start_cli(options, args):
    filename = options.filename
    if filename is None:
        console.danger("No filename selected")
        sys.exit()
    if os.path.isfile(filename) is not True:
        console.danger(f"The {filename} file could not be found")
            
    image = Image.open(filename)
    result = predict_image(image=image)
    if result is None:
        console.warning("No result found!")
    else:
        console.info(f"The film has been found")
        console.info(f"Movie Name: {result.name}")
        console.info(f"Estimated Duration: {result.hours}:{result.minutes}:{result.seconds}")
        console.info(f"Score: {result.score}")