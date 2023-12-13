from lib.console import Console
import gradio as gr
from lib.predict import predict_image
from lib.schema import PredictResult
from PIL import Image
import os

console = Console()

def prediction(image_array):
    result = predict_image(Image.fromarray(image_array))
    if result is None:
        console.warning("No result found!")
        return "No result found!"
    else:
        console.info(f"The film has been found")
        console.info(f"Movie Name: {result.name}")
        console.info(f"Estimated Duration: {result.hours}:{result.minutes}:{result.seconds}")
        console.info(f"Score: {result.score}")
        return f"{result.name} {result.hours}:{result.minutes}:{result.seconds} Score: {result.score}"
    
def start_web(options):
    demo = gr.Interface(
        fn = prediction,
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