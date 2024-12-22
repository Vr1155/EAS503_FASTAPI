# Use an official Python runtime as a parent image
FROM python:3.12.7

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model files into the container
COPY main.py .
COPY logistic.joblib .
COPY new_model.joblib .
COPY preprocessor_pipeline.joblib .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

