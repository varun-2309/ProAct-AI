import os
import time
import pandas as pd
from datetime import datetime
from src.data_simulation.sensor_simulator import generate_sensor_data

DATA_DIR = "data/raw"
FILE_PATH = os.path.join(DATA_DIR, "sensor_data.csv")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def ingest_data():
    ensure_data_dir()

    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=[
            "timestamp", "temperature", "vibration", "pressure", "rpm"
        ])
        df.to_csv(FILE_PATH, index=False)

    print("Starting data ingestion... Press CTRL+C to stop.\n")

    try:
        while True:
            data = generate_sensor_data()
            df = pd.DataFrame([data])
            df.to_csv(FILE_PATH, mode="a", header=False, index=False)
            print("Ingested:", data)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nData ingestion stopped.")

if __name__ == "__main__":
    ingest_data()
