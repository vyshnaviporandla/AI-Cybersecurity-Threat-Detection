
from pathlib import Path

import numpy as np
import pandas as pd


def load_dataset(csv_path, target="label", max_rows=None):
    """Load and validate a labeled network-traffic CSV."""

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path.resolve()}"
        )

    df = pd.read_csv(csv_path, nrows=max_rows)
    df.columns = df.columns.str.strip().str.lower()

    if target not in df.columns:
        raise ValueError(
            f"Target column '{target}' is missing. "
            f"Available columns: {df.columns.tolist()}"
        )

    # Remove records without a usable target.
    df = df.dropna(subset=[target]).copy()

    # Convert the binary target to integers.
    y = pd.to_numeric(df[target], errors="raise").astype(int)

    if not y.isin([0, 1]).all():
        raise ValueError("Expected binary labels: 0 and 1.")

    # Remove labels and identifiers that should not be model inputs.
    drop_columns = [target, "attack_cat", "id"]
    X = df.drop(
        columns=[c for c in drop_columns if c in df.columns]
    ).copy()

    # Replace infinite numeric values with missing values.
    X = X.replace([np.inf, -np.inf], np.nan)

    # Keep numeric columns numeric and categorical columns categorical.
    for column in X.columns:
        if X[column].dtype == "object":
            X[column] = X[column].astype("string").str.strip()

    return X, y
