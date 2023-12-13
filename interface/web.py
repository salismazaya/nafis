import logging
from rich.logging import RichHandler
from rich.console import Console
import gradio as gr
from lib.chroma import collection
from lib.predict import predict, predict_image
from lib.schema import PredictResult
from PIL import Image
import os

console = Console()
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")
logger.setLevel(logging.INFO)

for log_name, log_object in logging.Logger.manager.loggerDict.items():
    if log_name != "rich":
        logging.getLogger(log_name).setLevel(logging.WARNING)

def prediction(image_array):
    result = predict_image(Image.fromarray(image_array))
    if result is None:
        logger.warning("No result found!")
        return "No result found!"
    else:
        logger.info(f"The film has been found")
        logger.info(f"Movie Name: {result.name}")
        logger.info(f"Estimated Duration: {result.hours}:{result.minutes}:{result.seconds}")
        logger.info(f"Score: {result.score}")
        return f"{result.name} {result.hours}:{result.minutes}:{result.seconds} Score: {result.score}"
    
def start_web():
    demo = gr.Interface(fn = prediction, inputs = "image", outputs = "text")
    demo.launch(
        server_name = os.environ.get('HOST'),
        server_port = int(os.environ.get('PORT', 8000))
    )