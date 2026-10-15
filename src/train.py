import argparse
import json
from src.visualize import save_confusion_matrix, save_label_distribution
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.data_loader import load_dataset
from src.preprocessing import build_preprocessor


ROOT = Path(__file__).resolve().parent.parent


def train(args):
    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = ROOT / data_path

    print("Loading dataset...")
    X, y = load_dataset(
        data_path,
        target=args.target,
        max_rows=args.max_rows,
    )

    print(f"Records: {len(X):,}")
    print(f"Features: {X.shape[1]}")
    print("\nLabel counts:")
    print(y.value_counts().sort_index())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=42,
        stratify=y,
    )

    print("\nBuilding Random Forest pipeline...")
    model = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(X_train)),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=150,
                    random_state=42,
                    class_weight="balanced_subsample",
                    min_samples_leaf=2,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("Training model. Please wait...")
    model.fit(X_train, y_train)

    print("Evaluating model...")
    predictions = model.predict(X_test)

    metrics = {
        "dataset": str(data_path),
        "records": int(len(X)),
        "features": int(X.shape[1]),
        "train_records": int(len(X_train)),
        "test_records": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(
            precision_score(
                y_test, predictions, zero_division=0
            )
        ),
        "recall": float(
            recall_score(
                y_test, predictions, zero_division=0
            )
        ),
        "f1_score": float(
            f1_score(
                y_test, predictions, zero_division=0
            )
        ),
        "confusion_matrix": confusion_matrix(
            y_test, predictions
        ).tolist(),
        "classification_report": classification_report(
            y_test,
            predictions,
            target_names=["Normal", "Attack"],
            zero_division=0,
            output_dict=True,
        ),
    }

    model_path = ROOT / "models" / "threat_detector.joblib"
    metrics_path = ROOT / "outputs" / "metrics" / "evaluation.json"
    predictions_path = (
        ROOT / "outputs" / "predictions" / "test_predictions.csv"
    )

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    predictions_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)

    probabilities = model.predict_proba(X_test)[:, 1]

    results = pd.DataFrame({
        "actual_label": y_test.to_numpy(),
        "prediction": predictions,
        "predicted_label": predictions,
        "status": pd.Series(predictions).map({
            0: "Normal",
            1: "Potential Attack",
        }),
        "attack_probability": probabilities.round(4),
    })
    results.to_csv(predictions_path, index=False)


    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print("\n--- Evaluation Results ---")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 score:  {metrics['f1_score']:.4f}")
    print("\nConfusion matrix:")
    print(metrics["confusion_matrix"])
    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=["Normal", "Attack"],
        zero_division=0,
    ))

    print("\nSaved model:", model_path)
    print("Saved metrics:", metrics_path)
    print("Saved predictions:", predictions_path)
        # Save visual reports.
    confusion_matrix_path = ROOT / "images" / "confusion_matrix.png"
    label_distribution_path = ROOT / "images" / "label_distribution.png"

    save_confusion_matrix(
        y_test,
        predictions,
        confusion_matrix_path,
    )

    save_label_distribution(
        y,
        label_distribution_path,
    )

    print("Saved confusion matrix:", confusion_matrix_path)
    print("Saved label distribution:", label_distribution_path)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train an offline network threat classifier."
    )
    parser.add_argument(
        "--data",
        default="data/raw/UNSW_NB15_training-set.csv",
    )
    parser.add_argument("--target", default="label")
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--test-size", type=float, default=0.2)
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
