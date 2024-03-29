# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files into the container
COPY main.py .
COPY requirements.txt .
COPY models ./models

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (assuming your FastAPI app listens on port 8000)
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
