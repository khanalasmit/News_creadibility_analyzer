"""
Text preprocessing utilities
"""
import re
import sys
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Initialize NLTK components
stop_words_final = set(stopwords.words('english'))
lemmatizer_final = WordNetLemmatizer()


def tokenize_lemmatize(text):
    """
    Tokenize, lemmatize, and clean text for model input
    
    Args:
        text: Input text to process
        
    Returns:
        list: List of processed tokens
    """
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
