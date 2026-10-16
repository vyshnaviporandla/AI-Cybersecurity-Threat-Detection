
from pathlib import Path
import json

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, send_from_directory, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "threat_detector.joblib"
DATA_PATH = BASE_DIR / "data" / "raw" / "UNSW_NB15_training-set.csv"
METRICS_PATH = BASE_DIR / "outputs" / "metrics" / "evaluation.json"
CHART_PATH = BASE_DIR / "images"

app = Flask(__name__)

# Default evaluation results from the previously evaluated model.
# These are dataset evaluation results, not live attack-detection rates.
metrics = {
    "accuracy": 0.9588,
    "precision": 0.9705,
    "recall": 0.9689,
    "f1": 0.9697,
    "confusion_matrix": None,
}

model = None
data = None
feature_columns = []
feature_dtypes = {}
sample_record = {}

# Load available files without preventing the dashboard from starting.
try:
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r", encoding="utf-8") as file:
            loaded_metrics = json.load(file)
        if isinstance(loaded_metrics, dict):
            metrics.update(loaded_metrics)

    if DATA_PATH.exists():
        data = pd.read_csv(DATA_PATH, nrows=100)

        excluded = {"label", "attack_cat", "id"}
        feature_columns = [
            column
            for column in data.columns
            if column not in excluded
        ]

        feature_dtypes = data[feature_columns].dtypes
        sample_record = data.iloc[0][feature_columns].to_dict()

    if MODEL_PATH.exists() and feature_columns:
        model = joblib.load(MODEL_PATH)

except Exception as error:
    app.logger.exception("Optional dashboard files could not be loaded")
    model = None


def convert_value(column, value):
    """Convert an input value to the feature's expected data type."""
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
    """Display the dashboard homepage."""
    return render_template("index.html")


@app.get("/api/metrics")
def get_metrics():
    """Return evaluation metrics and model availability."""
    return jsonify({
        "metrics": {
            "accuracy": metrics.get("accuracy", 0.9588),
            "precision": metrics.get("precision", 0.9705),
            "recall": metrics.get("recall", 0.9689),
            "f1_score": metrics.get(
                "f1_score",
                metrics.get("f1", 0.9697)
            ),
        },
        "confusion_matrix": metrics.get("confusion_matrix"),
        "feature_count": len(feature_columns),
        "prediction_available": (
            model is not None and bool(feature_columns)
        ),
    })


@app.get("/api/sample")
def get_sample():
    """Return sample features when the dataset is available."""
    if not feature_columns or not sample_record:
        return jsonify({
            "error": "Sample data is unavailable in this deployment."
        }), 503

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
    """Predict whether submitted traffic resembles an attack."""
    if model is None or not feature_columns:
        return jsonify({
            "error": (
                "Prediction is unavailable in this demo deployment. "
                "The trained model and dataset are not installed "
                "on the server."
            )
        }), 503

    payload = request.get_json(silent=True) or {}
    supplied = payload.get("features")

    if not isinstance(supplied, dict):
        return jsonify({
            "error": "Send a JSON object containing a 'features' object."
        }), 400

    missing = [
        column for column in feature_columns
        if column not in supplied
    ]

    if missing:
        return jsonify({
            "error": "Some model features are missing.",
            "missing_features": missing,
        }), 400

    try:
        row = {
            column: convert_value(column, supplied[column])
            for column in feature_columns
        }

        frame = pd.DataFrame([row], columns=feature_columns)
        prediction = int(model.predict(frame)[0])

        attack_probability = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(frame)[0]
            classes = list(model.classes_)

            if 1 in classes:
                attack_probability = float(
                    probabilities[classes.index(1)]
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
                "This is a dataset-model estimate, not proof of an "
                "actual cyberattack. Do not use this demo as a "
                "live security system."
            ),
        })

    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": (
                "Prediction failed. Check that the model, dataset, "
                "and feature preprocessing are compatible."
            )
        }), 500


@app.get("/charts/<path:filename>")
def charts(filename):
    """Serve dashboard chart images."""
    return send_from_directory(str(CHART_PATH), filename)


if __name__ == "__main__":
    print("AI Cybersecurity Threat Detection Dashboard")
    print("Open http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
