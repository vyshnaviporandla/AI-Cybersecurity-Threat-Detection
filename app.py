
import os

import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

MODEL_PATH = os.path.join("models", "threat_detector.joblib")
model = None


def get_model():
    """Load the trained model when it is first needed."""
    global model

    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Trained model not found. Run 'python main.py' first."
            )

        model = joblib.load(MODEL_PATH)

    return model


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "project": "AI Cybersecurity Threat Detection",
        "mode": "offline dataset-based analysis",
        "model_loaded": model is not None,
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return jsonify({
                "error": "Send a JSON object containing a 'records' array."
            }), 400

        records = payload.get("records")

        if not isinstance(records, list) or not records:
            return jsonify({
                "error": "'records' must be a non-empty JSON array."
            }), 400

        if len(records) > 500:
            return jsonify({
                "error": "A maximum of 500 records is allowed per request."
            }), 400

        if not all(isinstance(record, dict) for record in records):
            return jsonify({
                "error": "Every record must be a JSON object."
            }), 400

        detector = get_model()
        X = pd.DataFrame(records)

        expected_features = (
            detector.named_steps["preprocessor"].feature_names_in_
        )
        X = X.reindex(columns=expected_features)

        predictions = detector.predict(X)
        probabilities = detector.predict_proba(X)[:, 1]

        results = []

        for index, prediction in enumerate(predictions):
            results.append({
                "traffic_class": (
                    "Potential Attack"
                    if int(prediction) == 1
                    else "Normal"
                ),
                "attack_probability": round(
                    float(probabilities[index]), 4
                ),
                "source": "Offline ML model",
            })

        return jsonify({
            "count": len(results),
            "results": results,
            "warning": (
                "Predictions are estimates from a trained dataset model, "
                "not proof of an actual attack."
            ),
        })

    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 503
    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    # Localhost only: this demo is not exposed to other devices.
    app.run(host="127.0.0.1", port=5000, debug=False)
