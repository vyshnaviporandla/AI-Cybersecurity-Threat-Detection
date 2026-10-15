
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def create_alerts(
    records,
    predictions,
    probabilities=None,
    output_path="outputs/alerts/security_alerts.csv",
):
    """Create alerts from labeled offline model predictions."""

    records = records.reset_index(drop=True).copy()
    predictions = list(predictions)

    if len(records) != len(predictions):
        raise ValueError(
            "The number of records must match the number of predictions."
        )

    if probabilities is None:
        probabilities = [None] * len(predictions)
    else:
        probabilities = list(probabilities)

    if len(probabilities) != len(predictions):
        raise ValueError(
            "The number of probabilities must match the predictions."
        )

    timestamp = datetime.now(timezone.utc).isoformat()
    alerts = []

    for index, prediction in enumerate(predictions):
        if int(prediction) != 1:
            continue

        confidence = probabilities[index]

        alert = {
            "alert_id": f"SIM-{index + 1:05d}",
            "timestamp_utc": timestamp,
            "traffic_type": "Potential Attack",
            "model_confidence": (
                round(float(confidence), 4)
                if confidence is not None
                else None
            ),
            "source": "Offline Dataset Simulation",
        }

        # Include a few useful, non-sensitive traffic features.
        for column in ("proto", "service", "state", "dur", "sbytes", "dbytes"):
            if column in records.columns:
                alert[column] = records.iloc[index][column]

        alerts.append(alert)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "alert_id",
        "timestamp_utc",
        "traffic_type",
        "model_confidence",
        "source",
    ]

    if alerts:
        alert_df = pd.DataFrame(alerts)
    else:
        alert_df = pd.DataFrame(columns=columns)

    alert_df.to_csv(output_path, index=False)

    print(f"Generated {len(alert_df)} potential-attack alerts.")
    print(f"Saved alerts to: {output_path.resolve()}")

    return alert_df
