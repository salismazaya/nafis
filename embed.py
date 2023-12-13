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
    level="NOTSET",
    format="%(message)s",
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
    n_frames = clip.reader.nframes
    duration = clip.duration
    logger.info(f"Movie duration: {(round(duration / 3600) if duration > 3600 else duration)} hour")
    
    timestamps = range(start_on, int(duration), interval_seconds)
    def execute(i):
        logger.info(f"Take frame {i}/{len(timestamps)}")
        frame = Image.fromarray(clip.get_frame(i))
        image_path = os.path.join(output_folder, f"{i}.png")
        frame.save(image_path)
    
    logger.info(f"Takes image frames from a total of {n_frames} frames")
    for i in timestamps:
        execute(i)

    clip.reader.close()

try:
    WORKER = int(sys.argv[2])
except IndexError:
    WORKER = int(input('Enter Total Worker: '))

logger.info(f"Your cpu count: {os.cpu_count()}")
if WORKER > os.cpu_count():
    logger.warning("[yellow]Not recommended: [reset]if the number of workers is greater than the number of CPUs", extra={"markup": True})
    
files = glob.glob('videos/*.mkv') + glob.glob('videos/*.mp4')
databases = glob.glob('database/*')
outputs = glob.glob('outputs/*')

def start(file: str):
    path = Path(file)
    title = path.as_posix().split('/')[-1]
    logger.info("Initiate image separation from video")
    logger.info(f"{file} started!")
    file_checksum = hashlib.md5(open(file, 'rb').read()).hexdigest()
    output_folder = 'outputs/' + file_checksum
    if output_folder in outputs:
        total_file = len(glob.glob(f'{output_folder}/*.png'))
        split_video_to_images(file, output_folder, start_on = total_file)
    else:
        split_video_to_images(file, output_folder)
    
    if not 'database/' + file_checksum + '.nafis' in databases:
        logger.info(f'Embedding {file} started!')
        
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
            logger.info("Write the embedding results")
            f.write(
                zlib.compress(
                    pickle.dumps(result)
                )
            )

with ThreadPoolExecutor(max_workers = WORKER) as t:
    t.map(start, files)
    