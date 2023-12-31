import os, glob, hashlib, pickle, zlib, sys
import cv2
import datetime
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from lib.predict import Prediction
from lib.schema import Result, Embedding
from pathlib import Path
from lib.console import Console
from lib.video import Video
from optparse import OptionParser

class ImageSpliter:
    def __init__(self, output_folder: str, video_path: str, console: Console) -> None:
        self.output_folder = output_folder
        self.video_path = video_path
        self.console = (console if console is None else Console())
        self.video = Video(self.video_path, self.output_folder)

        self.fps = self.video.fps
        
    def execute(self, second: int):
        frame_id = self.video.calculate_frame(self.fps, second)
        state, frame = self.video.get_frame(frame_id)
        if state:
            image_path = os.path.join(self.output_folder, f"{second}.png")
            self.video.save(image_path, frame)

    def run(self):
        with self.console.status(f"Writing frame duration 0") as status:
            for second in self.video.calculate_timestamp():
                duration = datetime.timedelta(seconds=second)
                status.update(f"Writing frame duration {duration}")
                self.execute(second=second)
        self.video.close()

class Embed:
    def __init__(self, cuda: bool = False, model: str = "resnet18", max_worker: int = None) -> None:
        self.console = Console()
        self.prediction = Prediction(cuda=cuda, model=model)
        self.supported_extension = ["mkv", "mp4"]

        self.files = self.get_files()
        self.databases = self.get_databases()
        self.outputs = self.get_outputs()
        self.worker = (max_worker if max_worker is not None else os.cpu_count())

        self.check_output()

    def get_files(self):
        files = []
        for ext in self.supported_extension:
            files.extend(
                glob.glob(f'videos/*.{ext}')
            )
        return files
    
    def get_databases(self):
        databases = glob.glob('databases/*')
        return databases
    
    def get_outputs(self):
        outputs = glob.glob('outputs/*')
        return outputs
    
    def check_output(self):
        if not os.path.exists('outputs'):
            self.console.warning("Output directory not found")
            self.console.info("Create new outputs directory")
            os.mkdir('outputs')

    def embed(self, output_folder: str, title: str = "", checksum: str = ""):
        embeddings = []
        images = glob.glob(output_folder + "/*.png")
        with self.console.status("Embedding frame ") as status:
            for index, image in enumerate(images):
                status.update(f"Embedding frame {index}")
                timestamp = Path(image).as_posix().split('/')[-1].removesuffix('.png')
                frame_timestamp = datetime.timedelta(seconds=int(timestamp))
                image_array = cv2.imread(image)
                image_object = Image.fromarray(image_array)
                vector = self.prediction.toVector(image_object)
                embeddings.append(
                    Embedding(
                        title=title,
                        timestamp=frame_timestamp,
                        vector=vector
                    )
                )
        
        result = Result(
            title=title,
            embeddings=embeddings
        )
        with open(os.path.join('database', checksum + ".nafis"), 'wb') as File:
            File.write(
                zlib.compress(pickle.dumps(result))
            )

    def start(self, filename: str):
        self.console.info("Initialite image seperation from video")
        self.console.info(f"{filename} started!")
        
        path = Path(filename)
        title = path.as_posix().split("/")[-1]
        checksum = hashlib.md5(open(filename, "rb").read()).hexdigest()
        output = os.path.join("outputs", checksum)
        image_spliter = ImageSpliter(output_folder=output, video_path=filename, console=self.console)
        if os.path.isdir(output):
            self.console.info("Remove old output folder")
            try:
                os.remove(output)
            except OSError:
                self.console.warning("Failed remove old output folder")
        else:
            self.console.info("Make new checksum folder")
            os.mkdir(output)
        image_spliter.run()
        
        if os.path.isfile(os.path.join("database", checksum + '.nafis')):
            self.console.info(f"Overwrite database")
        self.console.info(f"Embedding {filename} started!")
        self.embed(output_folder=output, title=title, checksum=checksum)

    def main(self):
        self.check_output()
        
        for filename in self.files:
            self.console.info(f"Start embedding file {filename}")
            self.start(filename=filename)

if __name__ == "__main__":
    option = OptionParser()
    option.add_option("--cuda", dest="cuda", help="Use your GPU", action="store_true")
    option.add_option("-w", "--worker", dest="worker", help="Total worker")
    option.add_option("-m", "--model", dest="model", help="Model, default: resnet18")
    opt, args = option.parse_args()
    
    app = Embed(
        cuda=(True if opt.cuda == True else False),
        model=(opt.model if opt.model is not None else "resnet18"),
        max_worker=(opt.worker if opt.worker is not None else os.cpu_count())
    )
    app.main()