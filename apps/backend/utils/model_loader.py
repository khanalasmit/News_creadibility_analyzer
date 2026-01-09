"""
Model loading utilities
"""
import joblib
from pathlib import Path

# Define model path
MODEL_PATH = Path(__file__).parent.parent.parent.parent / "model" / "final_xgb_pipeline.pkl"


def load_model():
    """
    Load the trained XGBoost model
    
    Returns:
        Loaded model object or None if loading fails
    """
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = joblib.load(f)
        print(f"✓ Model loaded successfully from {MODEL_PATH}")
        return model
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return None
