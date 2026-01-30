import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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
    print("Loading labeled data...")
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("Training failure prediction model...")
    model = train_model(X_train, y_train)

    print("\nModel evaluation:")
    y_pred = model.predict(X_test)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

