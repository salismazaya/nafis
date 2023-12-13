from lib.chroma import collection
from img2vec_pytorch import Img2Vec
from PIL import Image
from lib.schema import PredictResult

img2vec = Img2Vec()

def predict(image: Image):
    vec = img2vec.get_vec(image)

    rv = []
    for x in vec:
        rv.append(float(x))
    
    return rv


def predict_image(image: Image) -> PredictResult:
    embedding = predict(image)
    data = collection.query(query_embeddings = [embedding], n_results = 1)
    if len(data['ids'][0]) > 0:
        name, timestamp = data['ids'][0][0].split("|")
        timestamp = int(timestamp)
        hours = timestamp // 3600
        minutes = timestamp % 3600 / 60
        seconds = (timestamp % 3600) % 60
        score = data["distances"][0][0]
        result = PredictResult(name=name, hours=hours, minutes=minutes, seconds=seconds, score=score)
        return result
    else:
        return None