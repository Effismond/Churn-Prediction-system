# Use official Python 3.10 image
FROM python:3.10-slim

# Install tini for proper process handling
RUN apt-get update && apt-get install -y tini && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI and Streamlit ports
EXPOSE 8000 8501

# Use tini as init process to run both FastAPI and Streamlit
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run both FastAPI and Streamlit
CMD ["bash", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run App/streamlit_App.py --server.port 8501 --server.address 0.0.0.0"]