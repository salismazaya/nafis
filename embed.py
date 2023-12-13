import logging
import os
from rich.logging import RichHandler
from moviepy.video.io.VideoFileClip import VideoFileClip
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from lib.predict import predict
from lib.schema import Result, Embedding
from pathlib import Path
import os, glob, hashlib, pickle, zlib, sys

logging.basicConfig(
    level="NOSET",
    format="%(message)",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

if not os.path.exists('outputs'):
    logger.warning("Output directory not found")
    logger.info("Create new outputs directory")
    os.mkdir('outputs')

def split_video_to_images(video_path, output_folder, start_on = 0, interval_seconds = 1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    clip = VideoFileClip(video_path)

    duration = clip.duration
    logger.info(f"Movie duration: {duration}")

    timestamps = range(start_on, int(duration), interval_seconds)
    def execute(i):
        frame = Image.fromarray(clip.get_frame(i))
        image_path = os.path.join(output_folder, f"{i}.png")
        frame.save(image_path)
    
    for i in timestamps:
        execute(i)

    clip.reader.close()

try:
    WORKER = int(sys.argv[-1])
except:
    WORKER = int(input('Enter Total Worker: '))

logger.info(f"Your cpu count: {os.cpu_count()}")
if WORKER > os.cpu_count():
    logger.warning("Not recommended: if the number of workers is greater than the number of CPUs")
    
files = glob.glob('videos/*.mkv') + glob.glob('videos/*.mp4')
databases = glob.glob('database/*')
outputs = glob.glob('outputs/*')

def start(file: str):
    path = Path(file)
    title = path.as_posix().split('/')[-1]
    print(f'Split {file} to images started!')
    file_checksum = hashlib.md5(open(file, 'rb').read()).hexdigest()
    output_folder = 'outputs/' + file_checksum
    if output_folder in outputs:
        total_file = len(glob.glob(f'{output_folder}/*.png'))
        split_video_to_images(file, output_folder, start_on = total_file)
    else:
        split_video_to_images(file, output_folder)
    
    if not 'database/' + file_checksum + '.nafis' in databases:
        print(f'Embedding {file} started!')
        
        embeddings = []
        images = glob.glob(output_folder + '/*.png')
        for image in images:
            timestamp = Path(image).as_posix().split('/')[-1].removesuffix('.png')
            timestamp = int(timestamp)
            image_obj = Image.open(image)
            vector = predict(image_obj)
            
            embeddings.append(Embedding(title = title, timestamp = timestamp, vector = vector))
        
        result = Result(title = title, embeddings = embeddings)
        with open('database/' + file_checksum + '.nafis', 'wb') as f:
            f.write(
                zlib.compress(
                    pickle.dumps(result)
                )
            )

with ThreadPoolExecutor(max_workers = WORKER) as t:
    t.map(start, files)