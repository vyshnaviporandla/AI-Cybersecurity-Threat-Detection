# AI Cybersecurity Threat Detection

An educational machine-learning project that classifies network traffic records as **Normal** or **Potential Attack** using the public UNSW-NB15 dataset.

## Project Overview

This project demonstrates how machine learning can assist with cybersecurity threat detection by learning patterns from labeled network-traffic data.

It includes data preprocessing, model training, evaluation metrics, visualizations, prediction exports, simulated alerts, and a local Flask REST API.

**Important:** This is an offline dataset-based demonstration. It does not capture live network traffic, and a model prediction is not proof of an actual cyberattack.

## Features

- Binary network traffic classification
- Numeric and categorical data preprocessing
- Random Forest machine-learning model
- Confusion matrix and label-distribution charts
- Evaluation metrics saved as JSON
- CSV prediction reports
- Simulated potential-attack alerts
- Local Flask API for predictions
- Reproducible training with a fixed random seed

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib
- Joblib
- Flask
- SQLite is not required

## Dataset

The project uses the UNSW-NB15 training dataset.

Official dataset information:  
https://research.unsw.edu.au/projects/unsw-nb15-dataset

Place the downloaded training CSV at:

`data/raw/UNSW_NB15_training-set.csv`

The binary target is `label`:

- `0` — Normal traffic
- `1` — Attack traffic

The target label, attack category, and record identifier are excluded from the model features to reduce label leakage.

## Setup on Windows

Open Command Prompt in the project directory.

Create and activate a virtual environment:

```cmd
py -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```cmd
python -m pip install -r requirements.txt
```

Ensure the dataset exists at the path listed above.

## Train the Model

Run:

```cmd
python main.py
```

The training workflow is intended to save:

- `models/threat_detector.joblib`
- `outputs/metrics/evaluation.json`
- `outputs/predictions/test_predictions.csv`
- `images/confusion_matrix.png`
- `images/label_distribution.png`

## Generate Simulated Alerts

After training, run:

```cmd
python simulate.py
```

The simulated alerts are written to:

`outputs/alerts/security_alerts.csv`

## Run the Local API

Start the API:

```cmd
python app.py
```

Health endpoint:

`http://127.0.0.1:5000/health`

Prediction endpoint:

`POST http://127.0.0.1:5000/predict`

Example JSON request:

```json
{
  "records": [
    {
      "proto": "tcp",
      "service": "http",
      "state": "FIN",
      "dur": 0.5,
      "sbytes": 100,
      "dbytes": 250
    }
  ]
}
```

For meaningful results, provide records with feature names and value formats compatible with the dataset used for training. Missing columns are filled by the preprocessing pipeline, so incomplete records may produce less reliable predictions.

## Project Structure

```text
AI-Cybersecurity-Threat-Detection/
├── app.py
├── main.py
├── predict.py
├── simulate.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── raw/
│   └── sample/
├── models/
├── outputs/
│   ├── metrics/
│   ├── predictions/
│   └── alerts/
├── images/
├── docs/
├── notebooks/
└── src/
    ├── __init__.py
    ├── alerts.py
    ├── data_loader.py
    ├── preprocessing.py
    ├── train.py
    └── visualize.py
```

## Responsible Use

- Use public datasets or data you are authorized to analyze.
- Do not interpret predictions as confirmed incidents.
- Do not use this educational model as a replacement for professional security monitoring.
- Keep the API bound to localhost for this demo.

## Future Improvements

- Add precision, recall, F1-score, and ROC-AUC reporting.
- Add threshold tuning and false-positive analysis.
- Build a dashboard for visualizing model predictions.
- Test on a separate, compatible dataset.
- Add automated unit tests.

## License

Choose a license before distributing the source code. Check the dataset's terms separately before redistributing any dataset files.
