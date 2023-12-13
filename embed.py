from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from lib.predict import predict
from lib.schema import Result, Embedding
from pathlib import Path
import os, glob, hashlib, pickle, zlib, sys, cv2, numpy as np

if not os.path.exists('outputs'):
    os.mkdir('outputs')

def split_video_to_images(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    vidcap = cv2.VideoCapture(video_path)
    count = 0
    success = True
    while success:
      print(count, output_folder)
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))      
      success, image = vidcap.read()

      image_last = cv2.imread("{}.png".format(count-1))
      if np.array_equal(image,image_last):
          break

      cv2.imwrite(output_folder + "/%d.png" % count, image)
      count += 1

try:
    WORKER = int(sys.argv[-1])
except:
    WORKER = int(input('Enter Total Worker: '))

files = glob.glob('videos/*.mkv') + glob.glob('videos/*.mp4')
databases = glob.glob('database/*')
outputs = glob.glob('outputs/*')

def start(file: str):
    path = Path(file)
    title = path.as_posix().split('/')[-1]
    print(f'Split {file} to images started!')
    file_checksum = hashlib.md5(open(file, 'rb').read()).hexdigest()
    output_folder = 'outputs/' + file_checksum
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