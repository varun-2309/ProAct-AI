from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# =====================================================
# FastAPI App
# =====================================================
app = FastAPI(
    title="ProAct-AI API",
    description="Predictive Maintenance API (Failure Risk + RUL)",
    version="1.0"
)

# =====================================================
# Request Schema
# =====================================================
class SensorInput(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: int

# =====================================================
# Load & Train FAILURE MODEL
# =====================================================
def load_failure_model():
    df = pd.read_csv("data/processed/labeled_sensor_data.csv")

    X = df[["temperature", "vibration", "pressure", "rpm"]]
    y = df["failure_risk"]

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )
    model.fit(X, y)

    return model

failure_model = load_failure_model()

# =====================================================
# Load & Train RUL MODEL
# =====================================================
def load_rul_model():
    df = pd.read_csv("data/processed/rul_sensor_data.csv")

    X = df[["temperature", "vibration", "pressure", "rpm"]]
    y = df["RUL"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    model.fit(X, y)

    return model

rul_model = load_rul_model()

# =====================================================
# Root Endpoint
# =====================================================
@app.get("/")
def root():
    return {"message": "ProAct-AI API is running"}

# =====================================================
# Failure Prediction Endpoint
# =====================================================
@app.post("/predict/failure")
def predict_failure(data: SensorInput):
    input_df = pd.DataFrame([{
        "temperature": data.temperature,
        "vibration": data.vibration,
        "pressure": data.pressure,
        "rpm": data.rpm
    }])

    prediction = failure_model.predict(input_df)[0]
    risk = "HIGH" if prediction == 1 else "LOW"

    return {
        "failure_risk": risk
    }

# =====================================================
# RUL Prediction Endpoint
# =====================================================
@app.post("/predict/rul")
def predict_rul(data: SensorInput):
    input_df = pd.DataFrame([{
        "temperature": data.temperature,
        "vibration": data.vibration,
        "pressure": data.pressure,
        "rpm": data.rpm
    }])

    rul = rul_model.predict(input_df)[0]

    return {
        "estimated_RUL": round(float(rul), 2)
    }
