from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from numpy import asarray
import numpy as np
from io import BytesIO
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

# do not use postman for testing images predictions, it will cause error - error parsing in body
# https://github.com/tiangolo/fastapi/issues/2401

app = FastAPI()

MODEL = tf.keras.models.load_model("./models/1/1.keras")
CLASS_NAMES = ['Early Blight','Late Blight','Healthy']

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:19006"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def img_to_np(image):
    print(1)
    image_in_array = np.array(Image.open(BytesIO(image)))
    return image_in_array

    # another method
    # img = Image.open(BytesIO(image))
    # img_to_array = asarray(img,dtype='int32')
    # return img_to_array

@app.get('/ping')
async def ping():
    return "hello"

# @app.get('/predict')
# async def predict():
#     return 


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    data = img_to_np(await file.read())
    # print(data)
    
    data_batch = np.expand_dims(data,axis=0)
    
    predictions = MODEL.predict(data_batch)
    
    print(predictions,CLASS_NAMES[np.argmax(predictions[0])])

    typeClass = CLASS_NAMES[np.argmax(predictions[0])]
    
    confidence = int(np.argmax(predictions[0]))
    confidence = str(predictions[0][confidence]*100)
    
    # pass
    # return data
    # return {"confidence": confidence,"class":CLASS_NAMES[np.argmax(predictions)]}
    
    return {"class" : typeClass, "confidence" : confidence}

if __name__=="__main__":
    app.run(host='0.0.0.0',run=app)