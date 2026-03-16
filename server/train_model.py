import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("sla_dataset.csv")

priority_map = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3
}

df["priority"] = df["priority"].map(priority_map)

X = df[["priority", "similar_count"]]
y = df["breach"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "models/sla_model.pkl")

print("Model saved")