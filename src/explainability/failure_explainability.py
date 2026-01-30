import pandas as pd
import shap
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

DATA_PATH = "data/processed/labeled_sensor_data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df[["temperature", "vibration", "pressure", "rpm"]]
    y = df["failure_risk"]
    return X, y

def train_model(X, y):
    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )
    model.fit(X, y)
    return model

if __name__ == "__main__":
    print("Loading data...")
    X, y = load_data()

    print("Training model...")
    model = train_model(X, y)

    print("Generating SHAP explanations...")
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    # 👉 Select SHAP values for FAILURE class (class = 1)
    shap_values_failure = shap_values[..., 1]

    shap.plots.beeswarm(shap_values_failure)
    plt.show()
