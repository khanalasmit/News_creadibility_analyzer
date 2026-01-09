from fastapi import HTTPException,Path,Query,FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
import joblib
import pandas as pd
import re
import sys
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Define tokenizer + lemmatizer + stopword removal for TF-IDF
stop_words_final = set(stopwords.words('english'))
lemmatizer_final = WordNetLemmatizer()

def tokenize_lemmatize(text):
    if pd.isna(text):
        return []
    # To string and lower
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # Keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # Tokenize
    tokens = word_tokenize(text)
    # Lemmatize and remove stopwords
    tokens = [lemmatizer_final.lemmatize(t) for t in tokens
              if t not in stop_words_final and len(t) > 1]
    return tokens

# Register function in __main__ namespace for pickle to find it
sys.modules['__main__'].tokenize_lemmatize = tokenize_lemmatize

with open('C:\\Users\\Acer\\OneDrive\\Documents\\projects\\news_credibility_analyzer\\model\\final_xgb_pipeline.pkl','rb') as f:
    model=joblib.load(f)

app=FastAPI()

class UserInput(BaseModel):
    new_string:Annotated[str,Field(...,max_length=20000,description='Enter the news body here')]
 
@app.post('/predict')
def predict_premium(data:UserInput):
    # Convert to Series (not DataFrame) - model was trained on Series
    input_series = pd.Series([data.new_string])
    prediction = int(model.predict(input_series)[0])
    return JSONResponse(status_code=200,content={'message':prediction})
    
