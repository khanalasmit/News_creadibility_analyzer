import streamlit as st 
import requests

API_URL='http://127.0.0.1:8000/predict'

st.markdown("News creadibility analyzer")
text_input = st.text_area(
    "Enter news body for analysis",
    height=300,
    max_chars=20000,
    placeholder="Enter up to 20,000 characters..."
)

if st.button("Predict"):
    input_data={
        'new_string':text_input
    }
    try:
        response=requests.post(API_URL,json=input_data)
        if response.status_code==200:
            result=response.json()
            prediction = result['message']
            
            if prediction == 0:
                st.error("🚫 FAKE NEWS DETECTED")
            else:
                st.success("✅ REAL NEWS - Credible Source")
        else:
            st.error(f"API Error: {response.status_code}-{response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend")
