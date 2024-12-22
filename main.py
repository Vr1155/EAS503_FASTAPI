from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Load pre-trained model and preprocessing pipeline
# model = joblib.load("logistic.joblib")  # Replace with your model filename
preprocessor = joblib.load("preprocessor_pipeline.joblib")  # Load preprocessing pipeline
model = joblib.load("new_model.joblib")

# Initialize FastAPI app
app = FastAPI()

# Define input schema for raw features
class LoanApplication(BaseModel):
    person_age: int
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: int
    credit_score: int
    previous_loan_defaults_on_file: str


@app.get("/")
def read_root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Welcome to the Loan Approval Prediction API!"}


@app.post("/predict")
def predict(application: LoanApplication):
    """
    Predict loan approval based on user inputs.
    """
    # Convert input data to DataFrame for preprocessing
    input_data = pd.DataFrame([application.dict()])

    # Apply preprocessing pipeline to transform data (matches training)
    processed_data = preprocessor.transform(input_data)

    # Make prediction using the loaded model
    prediction = model.predict(processed_data)[0]

    # Map prediction to human-readable output
    result = "Approved" if prediction == 1 else "Denied"

    return {"loan_status": result}
