from img2vec_pytorch import Img2Vec
from PIL import Image

img2vec = Img2Vec(cuda = True)

def predict(image: Image):
    vec = img2vec.get_vec(image)

    rv = []
    for x in vec:
        rv.append(float(x))
    
    return rv