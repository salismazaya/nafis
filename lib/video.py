import os
import cv2
import datetime
from lib.exception import NotFoundError, SystemError

class Video:
    def __init__(self, filename: str, output_folder: str, start_on: int = 0, interval_seconds: int = 1) -> None:
        self.filename = filename
        self.output_folder = output_folder
        self.start_on = start_on
        self.interval_seconds = interval_seconds

        self.check_filename()
        self.check_folder()

        self.capture = self.make()

    @property
    def fps(self):
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        return fps
    
    @property
    def frames(self):
        frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        return frames
    
    @property
    def duration(self):
        seconds = round(self.frames / self.fps)
        delta = datetime.timedelta(seconds=seconds)
        return delta
    
    def get_frame(self, frame_id):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        state, frame = self.capture.read()
        return state, frame
    
    def calculate_frame(self, fps: int, second: int):
        return int(fps * second)
    
    def calculate_timestamp(self):
        duration = self.duration
        return range(self.start_on, duration.seconds, self.interval_seconds)
    
    def check_filename(self):
        if os.path.isfile(self.filename) is not True:
            raise NotFoundError(f"{self.filename} no such file")
        return True
    
    def check_folder(self):
        if os.path.isdir(self.output_folder) is not True:
            try:
                os.mkdir(self.output_folder)
            except:
                raise SystemError(f"{self.output_folder} failed make directory")
        return True
    
    def make(self):
        capture = cv2.VideoCapture(self.filename)
        return capture
    
    def close(self):
        self.capture.release()
        
    def save(self, filename: str, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, rgb)