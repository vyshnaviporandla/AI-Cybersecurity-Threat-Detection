
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay


def save_confusion_matrix(y_true, y_pred, output_path):
    """Save a confusion-matrix image for model evaluation."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 6))

    ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=["Normal", "Attack"],
        cmap="Blues",
        values_format="d",
        ax=ax,
    )

    ax.set_title("AI Cybersecurity Threat Detection")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def save_label_distribution(y, output_path):
    """Save a chart showing the distribution of normal and attack labels."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = pd.Series(y).map({
        0: "Normal",
        1: "Attack",
    })

    counts = labels.value_counts().reindex(
        ["Normal", "Attack"],
        fill_value=0,
    )

    fig, ax = plt.subplots(figsize=(7, 5))

    counts.plot(
        kind="bar",
        ax=ax,
        color=["#2E86AB", "#E76F51"],
    )

    ax.set_title("Network Traffic Label Distribution")
    ax.set_xlabel("Traffic Type")
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=0)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
