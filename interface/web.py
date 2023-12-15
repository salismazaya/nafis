import os
import gradio as gr
from nafis.console import Console
from nafis.predict import Prediction
from PIL import Image

class Web:
    def __init__(self) -> None:
        self.console = Console()
        self.prediction = Prediction()

    def predict(self, image_array):
        result = self.prediction.predict_image(Image.fromarray(image_array))
        if result is None:
            self.console.warning("No result found!")
            return "No result found!"
        else:
            self.console.info(f"The film has been found")
            self.console.info(f"Movie Name: {result.name}")
            self.console.info(f"Estimated Duration: {result.hours}:{result.minutes}:{result.seconds}")
            self.console.info(f"Score: {result.score}")
            return f"{result.name} {result.hours}:{result.minutes}:{result.seconds} Score: {result.score}"

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