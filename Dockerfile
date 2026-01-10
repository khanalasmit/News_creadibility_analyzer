# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords wordnet punkt_tab

# Copy the entire application
COPY . .

# Expose ports
# 8000 for FastAPI backend
# 8501 for Streamlit frontend
EXPOSE 8000 8501

# Create a startup script to run both services
RUN echo '#!/bin/bash\n\
cd /app/apps/backend && uvicorn fastapi_model:app --host 0.0.0.0 --port 8000 &\n\
cd /app && streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Command to run both backend and frontend
CMD ["/bin/bash", "/app/start.sh"]