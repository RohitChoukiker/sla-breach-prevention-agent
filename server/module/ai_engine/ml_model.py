import joblib
import numpy as np
import os

MODEL = None


def load_model():
    global MODEL

    if MODEL is None:
        print("[ML] Loading SLA model...")
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "sla_model.pkl"))
        MODEL = joblib.load(model_path)

    return MODEL


def predict_breach(priority, similar_count):

    model = load_model()

    priority_map = {
        "low": 0,
        "medium": 1,
        "high": 2,
        "critical": 3
    }

    features = np.array([
        priority_map.get(priority, 1),
        similar_count
    ]).reshape(1, -1)

    prob = model.predict_proba(features)[0][1]

    return float(prob)