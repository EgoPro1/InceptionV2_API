import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse
from tensorflow.python.keras.preprocessing import image as imgx
from serve_model import predict, read_imagefile
from schema import Symptom
import symptom_check
import requests
from PIL import Image

app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>
<h2>Try Covid symptom checker api - it is just a learning app demo</h2>
<br>by Aniket Maurya"""

app = FastAPI(title='Comparizy', description=app_desc)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post("/predict/image")
async def predict_api(filename):
    extension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
 
    print(filename)
    print(extension)
    if not extension:
        return "Image must be jpg or png format!"

    image = Image.open(requests.get(filename, stream=True).raw)
    
         
    prediction = predict(image)

    return prediction


@app.post("/api/covid-symptom-check")
def check_risk(symptom: Symptom):
    return symptom_check.get_risk_level(symptom)


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
