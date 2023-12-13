import os
import sys
import logging
from rich.logging import RichHandler
from rich.console import Console
from lib.chroma import collection
from lib.predict import predict, predict_image
from PIL import Image

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
        log_object.disabled = True
        
def start_cli():
    try:
        filename = sys.argv[2]
    except IndexError:
        filename = console.input("Enter your file: ")
    if os.path.isfile(filename) is not True:
        logger.error(f"The {filename} file could not be found")
        
    image = Image.open(filename)
    result = predict_image(image=image)
    if result is None:
        logger.warning("No result found!")
    else:
        logger.info(f"The film has been found")
        logger.info(f"Movie Name: {result.name}")
        logger.info(f"Estimated Duration: {result.hours}:{result.minutes}:{result.seconds}")
        logger.info(f"Score: {result.score}")