import datetime
from lib.chroma import collection
from img2vec_pytorch import Img2Vec
from PIL import Image
from lib.schema import PredictResult

class Prediction:
    def __init__(self, cuda: bool = False, model: str = "resnet18") -> None:
        self.img2vec = Img2Vec(cuda=cuda, model=model)

    def toVector(self, image: Image):
        vector = self.img2vec.get_vec(image)
        arr = []
        for x in vector:
            arr.append(
                float(x)
            )
        return arr
    
    def predict_image(self, image: Image) -> PredictResult:
        embedding = self.toVector(image)
        data = collection.query(query_embeddings = [embedding], n_results = 1)
        if len(data['ids'][0]) > 0:
            name, timestamp = data['ids'][0][0].split("|")
            timestamp = datetime.timedelta(seconds=int(timestamp))
            # hours = timestamp.seconds // 3600
            # minutes = timestamp.seconds % 3600 // 60
            # seconds = (timestamp.seconds % 3600) % 60
            score = data["distances"][0][0]
            result = PredictResult(name=name, time=timestamp, score=score)
            return result
        else:
            return None