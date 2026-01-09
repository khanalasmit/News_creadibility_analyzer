from fastapi import HTTPException,Path,Query,FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from schema.user_input import UserInput
from utils import load_model, tokenize_lemmatize

# Load model at startup
model = load_model()
    
MODEL_VERSION='1.0.0'

app=FastAPI()

 
@app.get('/')
def home():
    return {'message':'Insurance premium prediction API'} 
#machine readable
@app.get('/health')
def health_check():
    return{
        'version':MODEL_VERSION,
        'status':'Ok',
        'model_loaded':model is not None
    }
@app.post('/predict')
def predict_premium(data:UserInput):
    input_series = pd.Series([data.new_string])
    prediction = int(model.predict(input_series)[0])
    return JSONResponse(status_code=200,content={'message':prediction})
    
