# First stage: Build the application
FROM python:3.10.12 AS builder

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn


# Second stage: Create the final lightweight image
FROM python:3.10.12-alpine

# Copy the built application from the previous stage
COPY --from=builder /app /app

# Set the working directory in the container
WORKDIR /app

# Expose port 8000 (assuming your FastAPI app listens on port 8000)
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]