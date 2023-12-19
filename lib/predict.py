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
    
    def find_distances(self, distances):
        val = max(distances)
        print (val)
        index = distances.index(val)
        return index
    
    def predict_image(self, image: Image) -> PredictResult:
        embedding = self.toVector(image)
        data = collection.query(query_embeddings = [embedding])
        if len(data['ids'][0]) > 0:
            index = self.find_distances(data["distances"][0])
            name, timestamp = data['ids'][0][index - 1].split("|")
            timestamp = datetime.timedelta(seconds=int(timestamp))
            # hours = timestamp.seconds // 3600
            # minutes = timestamp.seconds % 3600 // 60
            # seconds = (timestamp.seconds % 3600) % 60
            score = data["distances"][0][index - 1]
            result = PredictResult(name=name, time=timestamp, score=score)
            return result
        else:
            return None