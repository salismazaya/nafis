import gradio as gr
from lib.chroma import collection
from lib.predict import predict
from PIL import Image
import os

def prediction(image_array):
    embedding = predict(Image.fromarray(image_array))
    data = collection.query(query_embeddings = [embedding], n_results = 1)
    name, timestamp =  data['ids'][0][0].split('|')
    timestamp = int(timestamp)
    hours = timestamp // 3600
    minutes = timestamp % 3600 // 60
    seconds = (timestamp % 3600) % 60

    return f"{name} {hours}:{minutes}:{seconds} Score: {data['distances'][0][0]}"

demo = gr.Interface(fn = prediction, inputs = "image", outputs = "text")

if __name__ == "__main__":
    demo.launch(
        server_name = os.environ.get('HOST'),
        server_port = int(os.environ.get('PORT', 8000))
    )   