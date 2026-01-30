import pandas as pd
from sklearn.ensemble import IsolationForest

DATA_PATH = "data/raw/sensor_data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df[["temperature", "vibration", "pressure", "rpm"]]

def train_model(data):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(data)
    return model

def detect_anomalies(model, data):
    data["anomaly"] = model.predict(data)
    data["anomaly"] = data["anomaly"].map({1: "Normal", -1: "Anomaly"})
    return data

if __name__ == "__main__":
    print("Loading data...")
    data = load_data()

    print("Training anomaly detection model...")
    model = train_model(data)

    print("Detecting anomalies...")
    results = detect_anomalies(model, data)

    print(results.tail(10))
