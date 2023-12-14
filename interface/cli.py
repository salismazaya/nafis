import os
import sys
from lib.console import Console
from lib.predict import Prediction
from PIL import Image
console = Console()

class CLI:
    def __init__(self, options = None) -> None:
        self.console = Console()
        self.prediction = Prediction()
        self.options = options

    def set_options(self, options):
        self.options = options
    
    def check_filename(self):
        if self.filename is None:
            self.console.danger("No filename selected")
            sys.exit()
        if os.path.isfile(self.filename) is not True:
            self.console.danger(f"The {self.filename} file could not be found")
            sys.exit()
        
    def start(self):
        self.filename = self.options.filename
        self.check_filename()

        image = Image.open(self.filename)
        result = self.prediction.predict_image(image=image)
        if result is None:
            self.console.warning("No result found!")
        else:
            self.console.info(f"The film has been found")
            self.console.info(f"Movie Name: {result.name}")
            self.console.info(f"Estimated Duration: {result.hours}:{result.minutes}:{result.seconds}")
            self.console.info(f"Score: {result.score}")