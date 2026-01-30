import pandas as pd

DATA_PATH = "data/raw/sensor_data.csv"
OUTPUT_PATH = "data/processed/labeled_sensor_data.csv"

def label_failure(row):
    if row["temperature"] > 75 or row["vibration"] > 0.9:
        return 1   # Failure risk
    return 0       # Normal

def main():
    df = pd.read_csv(DATA_PATH)

    df["failure_risk"] = df.apply(label_failure, axis=1)

    df.to_csv(OUTPUT_PATH, index=False)
    print("Labeled data saved to:", OUTPUT_PATH)
    print(df["failure_risk"].value_counts())

if __name__ == "__main__":
    main()
	