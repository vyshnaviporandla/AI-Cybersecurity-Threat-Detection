
import argparse
from pathlib import Path

import pandas as pd

from src.alerts import create_alerts


def main():
    parser = argparse.ArgumentParser(
        description="Generate offline cybersecurity simulation alerts."
    )

    parser.add_argument(
        "--input",
        default="outputs/predictions/test_predictions.csv",
        help="CSV containing test predictions.",
    )

    parser.add_argument(
        "--output",
        default="outputs/alerts/security_alerts.csv",
        help="Output path for generated alerts.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        parser.error(
            f"Predictions file not found: {input_path.resolve()}. "
            "Train the model first using: python main.py"
        )

    predictions_df = pd.read_csv(input_path)

    required_columns = {"prediction"}
    missing = required_columns - set(predictions_df.columns)

    if missing:
        parser.error(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    predictions = predictions_df["prediction"].astype(int).tolist()

    if "attack_probability" in predictions_df.columns:
        probabilities = predictions_df["attack_probability"].tolist()
    else:
        probabilities = None

    # Preserve optional traffic features for readable alert records.
    feature_columns = [
        column
        for column in ("proto", "service", "state", "dur", "sbytes", "dbytes")
        if column in predictions_df.columns
    ]

    records = predictions_df[feature_columns].copy()

    create_alerts(
        records=records,
        predictions=predictions,
        probabilities=probabilities,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
