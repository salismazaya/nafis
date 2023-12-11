from moviepy.video.io.VideoFileClip import VideoFileClip
# from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from lib.predict import predict
from lib.schema import Result, Embedding
from pathlib import Path
import os, glob, hashlib, pickle

if not os.path.exists('outputs'):
    os.mkdir('outputs')

def split_video_to_images(video_path, output_folder, start_on = 0, interval_seconds = 1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    clip = VideoFileClip(video_path)

    duration = clip.duration

    timestamps = range(start_on, int(duration), interval_seconds)
    def execute(i):
        frame = Image.fromarray(clip.get_frame(i))
        image_path = os.path.join(output_folder, f"{i}.png")
        frame.save(image_path)
    
    for i in timestamps:
        execute(i)

    clip.reader.close()

# WORKER = int(input('Enter Total Worker: '))
files = glob.glob('videos/*.mkv') + glob.glob('videos/*.mp4')
databases = glob.glob('database/*')
outputs = glob.glob('outputs/*')
for file in files:
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
            f.write(pickle.dumps(result))