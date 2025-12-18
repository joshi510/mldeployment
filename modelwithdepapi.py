from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Salary Prediction API")

model = joblib.load("salary_model.joblib")

class InputData(BaseModel):
    years: float

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

@app.post("/predict")
def predict(data: InputData):
    X = np.array([[data.years]])
    prediction = model.predict(X)
    return {
        "years_experience": data.years,
        "predicted_salary": float(prediction[0])
    }
