import gradio as gr
from lib.predict import predict_image
from lib.schema import PredictResult
from PIL import Image
import os

def prediction(image_array):
    result = predict_image(Image.fromarray(image_array))
    if isinstance(result, PredictResult):
        return f"{result.name} {result.hours}:{result.minutes}:{result.seconds} Score: {result.score}"
    else:
        return "No result found"
    
def start_web():
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