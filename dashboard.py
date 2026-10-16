
from pathlib import Path
import json

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "threat_detector.joblib"
DATA_PATH = BASE_DIR / "data" / "raw" / "UNSW_NB15_training-set.csv"
METRICS_PATH = BASE_DIR / "outputs" / "metrics" / "evaluation.json"
CHART_PATH = BASE_DIR / "images"

app = Flask(__name__)

# Reuse the existing trained model. Do not retrain it here.
model = joblib.load(MODEL_PATH)

# Use the original dataset to determine the model's expected features
# and their data types. No records are modified or uploaded.
data = pd.read_csv(DATA_PATH, nrows=100)
excluded = {"label", "attack_cat", "id"}
feature_columns = [c for c in data.columns if c not in excluded]
feature_dtypes = data[feature_columns].dtypes
sample_record = data.iloc[0][feature_columns].to_dict()

with open(METRICS_PATH, "r", encoding="utf-8") as file:
    metrics = json.load(file)


def convert_value(column, value):
    """Convert browser input to the type expected by the model."""
    dtype = feature_dtypes[column]

    if pd.api.types.is_integer_dtype(dtype):
        number = float(value)
        if not number.is_integer():
            raise ValueError(f"{column} must be a whole number.")
        return int(number)

    if pd.api.types.is_numeric_dtype(dtype):
        return float(value)

    return str(value)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/metrics")
def get_metrics():
    return jsonify({
        "metrics": {
            "accuracy": metrics.get("accuracy"),
            "precision": metrics.get("precision"),
            "recall": metrics.get("recall"),
            "f1_score": metrics.get("f1_score"),
        },
        "confusion_matrix": metrics.get("confusion_matrix"),
        "feature_count": len(feature_columns),
    })


@app.get("/api/sample")
def get_sample():
    """Return a sample feature record to help test the dashboard."""
    values = {}

    for column in feature_columns:
        value = sample_record[column]
        if pd.isna(value):
            value = ""
        elif hasattr(value, "item"):
            value = value.item()
        values[column] = value

    return jsonify({"features": values})


@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    supplied = payload.get("features")

    if not isinstance(supplied, dict):
        return jsonify({
            "error": "Send a JSON object containing a 'features' object."
        }), 400

    missing = [c for c in feature_columns if c not in supplied]
    if missing:
        return jsonify({
            "error": "Some model features are missing.",
            "missing_features": missing
        }), 400

    try:
        row = {
            column: convert_value(column, supplied[column])
            for column in feature_columns
        }
        frame = pd.DataFrame([row], columns=feature_columns)

        prediction = int(model.predict(frame)[0])
        probabilities = model.predict_proba(frame)[0]
        classes = list(model.classes_)
        attack_index = classes.index(1) if 1 in classes else None
        attack_probability = (
            float(probabilities[attack_index])
            if attack_index is not None else None
        )

        return jsonify({
            "prediction": prediction,
            "traffic_class": (
                "Potential Attack" if prediction == 1 else "Normal"
            ),
            "attack_probability": (
                round(attack_probability, 4)
                if attack_probability is not None else None
            ),
            "warning": (
                "This is a dataset-model estimate, not proof of an actual "
                "cyberattack. Do not use this demo as a live security system."
            )
        })

    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": (
                "Prediction failed. Check that the model, dataset, and "
                "feature preprocessing are compatible."
            )
        }), 500


@app.get("/charts/<path:filename>")
def charts(filename):
    return send_from_directory(CHART_PATH, filename)


if __name__ == "__main__":
    print("AI Cybersecurity Threat Detection Dashboard")
    print("Open http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
