import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.data_loader import load_dataset


def predict_file(input_path, model_path, output_path):
    """Predict normal or potential-attack traffic from a CSV file."""

    input_path = Path(input_path)
    model_path = Path(model_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {input_path.resolve()}"
        )

    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found: {model_path.resolve()}. "
            "Train the model first using: python main.py"
        )

    model = joblib.load(model_path)

    # The shared loader removes target/identifier columns when present.
    X, _ = load_dataset(input_path, target="label")

    expected_features = model.named_steps["preprocessor"].feature_names_in_
    X = X.reindex(columns=expected_features)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    results = pd.DataFrame({
        "prediction": predictions,
        "traffic_class": [
            "Potential Attack" if value == 1 else "Normal"
            for value in predictions
        ],
        "attack_probability": probabilities.round(4),
    })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    print(f"Records analyzed: {len(results)}")
    print(f"Normal records: {(predictions == 0).sum()}")
    print(f"Potential attacks: {(predictions == 1).sum()}")
    print(f"Predictions saved to: {output_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Predict network traffic classes using a trained model."
    )
    parser.add_argument(
        "--input",
        default="data/raw/UNSW_NB15_training-set.csv",
        help="Path to the input network traffic CSV.",
    )
    parser.add_argument(
        "--model",
        default="models/threat_detector.joblib",
        help="Path to the trained model.",
    )
    parser.add_argument(
        "--output",
        default="outputs/predictions/predictions.csv",
        help="Path for the prediction CSV.",
    )

    args = parser.parse_args()

    try:
        predict_file(args.input, args.model, args.output)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
