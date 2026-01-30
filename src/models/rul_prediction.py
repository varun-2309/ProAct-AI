import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

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
    print("Loading RUL-labeled data...")
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    print("Training RUL prediction model...")
    model = train_model(X_train, y_train)

    print("\nModel evaluation:")
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
