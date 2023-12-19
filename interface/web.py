import warnings
warnings.filterwarnings("ignore")
import os
import datetime
import gradio as gr
from lib.console import Console
from lib.predict import Prediction
from PIL import Image

class Web:
    def __init__(self) -> None:
        self.console = Console()
        self.prediction = Prediction()

    def convert_to_duration(self, timestamp):
        if isinstance(timestamp, datetime.timedelta) is not True:
            return datetime.timedelta(seconds=timestamp)
        
    def predict(self, image_array):
        result = self.prediction.predict_image(Image.fromarray(image_array))
        if result is None:
            self.console.warning("No result found!")
            return "No result found!"
        else:
            timestamp = result.time
            self.console.info(f"The film has been found")
            self.console.info(f"Movie Name: {result.name}")
            self.console.info(f"Estimated Duration: {result.time}")
            self.console.info(f"Score: {result.score}")
            return f"{result.name} {result.time} Score: {result.score}"

    def start(self):    
        demo = gr.Interface(
            fn = self.predict,
            inputs = "image",
            outputs = "text",
            allow_flagging = False,
            title = 'NAFIS',
            description = 'Made with love by salismazaya and my friends. this is open source https://github.com/salismazaya/nafis',
        )
        demo.launch(
            server_name = os.environ.get('HOST'),
            server_port = int(os.environ.get('PORT', 8000))
        )