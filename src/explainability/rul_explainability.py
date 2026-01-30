import pandas as pd
import shap
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

DATA_PATH = "data/processed/rul_sensor_data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df[["temperature", "vibration", "pressure", "rpm"]]
    y = df["RUL"]
    return X, y

def train_model(X, y):
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    model.fit(X, y)
    return model

if __name__ == "__main__":
    print("Loading data...")
    X, y = load_data()

    print("Training RUL model...")
    model = train_model(X, y)

    print("Generating SHAP explanations...")
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    shap.plots.beeswarm(shap_values)
    plt.show()
