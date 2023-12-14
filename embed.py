from moviepy.video.io.VideoFileClip import VideoFileClip
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from lib.predict import predict
from lib.schema import Result, Embedding
from pathlib import Path
import os, glob, hashlib, pickle, zlib, sys
from lib.console import Console

class ImageSpliter:
    def __init__(self, output_folder: str, video_path: str, console: Console) -> None:
        self.output_folder = output_folder
        self.video_path = video_path
        self.console = (console if console is None else Console())

        self.clip = VideoFileClip(self.video_path)

    @property
    def duration(self):
        return self.clip.duration
    
    def timestamps(self, start_on: int = 0, interval_seconds: int = 1):
        timestamps = range(start_on, int(self.duration), interval_seconds)
        return timestamps
        
    def check_output(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def execute(self, index: int):
        frame = Image.fromarray(
            self.clip.get_frame(index)
        )
        image_path = os.path.join(self.output_folder, f"{index}.png")
        frame.save(image_path)

    def run(self, start_on: int = 0, interval_seconds: int = 1):
        self.check_output()
        self.console.info(f'Movie duration: {(round(self.duration))}')
        for index in self.timestamps(start_on, interval_seconds):
            self.execute(index=index)
        self.clip.reader.close()

class Embed:
    def __init__(self) -> None:
        self.console = Console()
        self.supported_extension = ["mkv", "mp4"]

        self.files = self.get_files()
        self.databases = self.get_databases()
        self.outputs = self.get_outputs()

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
        for image in images:
            timestamp = Path(image).as_posix().split('/')[-1].removesuffix('.png')
            image_object = Image.open(image)
            vector = predict(image_object)
            embeddings.append(
                Embedding(
                    title=title,
                    timestamp=int(timestamp),
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
            self.console.info("Continuing frame splitting")
            start_on = len(glob.glob(f"{output}/*.png"))
            image_spliter.run(start_on=start_on, interval_seconds=1)
        else:
            image_spliter.run()
        
        if os.path.isfile(os.path.join("database", checksum + '.nafis')):
            self.console.info(f"Embedding {filename} started!")
            self.embed(output_folder=output, title=title, checksum=checksum)

    def main(self):
        worker = self.console.input("Total worker: ")
        if worker.rstrip().lstrip() == "":
            worker = os.cpu_count()
        if worker.isdigit() is not True:
            self.console.danger("Input only accept digit")
            sys.exit()
        
        with self.console.status("[bold green] Starting embedding system") as status:
            with ThreadPoolExecutor(max_workers=int(worker)) as thread:
                thread.map(self.start, (self.files))

if __name__ == "__main__":
    app = Embed()
    app.main()