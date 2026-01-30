import pandas as pd
import numpy as np

DATA_PATH = "data/processed/labeled_sensor_data.csv"
OUTPUT_PATH = "data/processed/rul_sensor_data.csv"

MAX_RUL = 100  # arbitrary life units (can be hours/days/cycles)

def compute_health_index(row):
    # Normalize degradation factors
    temp_score = (row["temperature"] - 60) / 20
    vib_score = (row["vibration"] - 0.4) / 0.6

    health = temp_score + vib_score
    return max(0, health)

def main():
    df = pd.read_csv(DATA_PATH)

    df["health_index"] = df.apply(compute_health_index, axis=1)

    # Convert health index to RUL
    df["RUL"] = (MAX_RUL * (1 - df["health_index"])).clip(lower=0)

    df.to_csv(OUTPUT_PATH, index=False)

    print("RUL-labeled data saved to:", OUTPUT_PATH)
    print(df[["temperature", "vibration", "health_index", "RUL"]].tail())

if __name__ == "__main__":
    main()
