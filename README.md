# 🛡️ AI Cybersecurity Threat Detection


A machine learning project that classifies network traffic as **Normal** or **Potential Attack** using the UNSW-NB15 dataset. The project includes data preprocessing, model evaluation, visual reports, automated alert generation, and a Flask prediction API.

> **Note:** This is an educational, offline dataset-based demonstration. It does not monitor live network traffic or confirm real-world attacks.

## 📌 Project Overview

Cybersecurity teams need ways to identify suspicious network activity. This project demonstrates how supervised machine learning can learn patterns from labeled network traffic and classify unseen test records.

### 🎯 Objectives

An educational machine-learning project that classifies network traffic records as Normal or Potential Attack using the UNSW-NB15 dataset.

## Overview

This project demonstrates how machine learning can help analyze labeled network traffic data. It includes data preprocessing, Random Forest classification, model evaluation, prediction reports, simulated security alerts, a Flask REST API, and a browser-based dashboard.

**Important:** This is an offline dataset-based demonstration. It does not capture live network traffic. A prediction is not proof of an actual cyberattack.
 (Add cybersecurity dashboard and API tests)

- Classify network traffic as normal or potentially malicious.
- Evaluate the classifier using standard machine learning metrics.
- Visualize model performance and dataset label distribution.
- Generate CSV reports of predicted potential attacks.
- Provide a local REST API for sample traffic classification.

## ✨ Features

- Network traffic classification
- Numeric and categorical feature preprocessing
- Random Forest model training
- Accuracy, precision, recall, and F1-score reporting
- Confusion matrix and label distribution charts
- CSV prediction reports and simulated alerts
- Flask REST API with input validation
- Interactive local dashboard for sample predictions
- Reproducible model training
 (Add cybersecurity dashboard and API tests)

- **Data preprocessing:** Handles numerical and categorical network features.
- **Machine learning:** Trains a classifier using Scikit-learn.
- **Model evaluation:** Calculates accuracy, precision, recall, F1-score, and a confusion matrix.
- **Visual reports:** Generates charts for model evaluation and label distribution.
- **Alert simulation:** Creates a CSV report from model predictions.
- **REST API:** Provides local health-check and prediction endpoints through Flask.
- **Reproducible workflow:** Separates data loading, preprocessing, training, visualization, and alert generation into modules.

## 🧰 Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib
- Joblib
- Flask
- HTML, CSS, and JavaScript
(Add cybersecurity dashboard and API tests)

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas and NumPy | Data processing |
| Scikit-learn | Preprocessing and machine learning |
| Matplotlib | Evaluation visualizations |
| Joblib | Saving and loading the trained model |
| Flask | Local REST API |
| Git and GitHub | Version control and project hosting |


## 📊 Model Performance

The following results were recorded on the held-out test set.

| Metric | Result |
|---|---:|
| Accuracy | 95.88% |
| Attack precision | 97.05% |
| Attack recall | 96.89% |
| Attack F1-score | 96.97% |
| Training records | 140,272 |
| Test records | 35,069 |
| Input features | 42 |

The project uses the UNSW-NB15 dataset.

Official dataset information:
https://research.unsw.edu.au/projects/unsw-nb15-dataset

Place the training CSV at:
(Add cybersecurity dashboard and API tests)

### Confusion Matrix

| Actual class | Predicted Normal | Predicted Attack |
|---|---:|---:|
| Normal | 10,498 | 702 |
| Attack | 742 | 23,127 |

The model correctly classified many normal and attack records, but it also produced false positives and false negatives. These results apply to this dataset and test split; performance on other traffic may differ.

## 📈 Visualizations

The target column is `label`:

- `0`: Normal traffic
- `1`: Attack traffic

The target label, attack category, and record identifier are excluded from the model features.

Do not commit the dataset unless you have verified that redistribution is permitted.

## Requirements

- Python compatible with the versions listed in `requirements.txt`
- Windows Command Prompt or another terminal
- The UNSW-NB15 training CSV at the path above
(Add cybersecurity dashboard and API tests)

### Confusion Matrix

![Confusion Matrix](images/confusion_matrix.png)

This chart shows correct and incorrect classifications for the two classes.

### Label Distribution

![Label Distribution](images/label_distribution.png)

This chart illustrates the distribution of normal and attack labels in the dataset.

## 🗂️ Project Structure

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
│   └── raw/
│       └── UNSW_NB15_training-set.csv
├── models/
│   └── threat_detector.joblib
├── src/
│   ├── __init__.py
│   ├── alerts.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train.py
│   └── visualize.py
├── images/
│   ├── confusion_matrix.png
│   └── label_distribution.png
└── outputs/
    ├── alerts/
    │   └── security_alerts.csv
    ├── metrics/
    │   └── evaluation.json
    └── predictions/
        └── test_predictions.csv

Open Command Prompt in the project directory and run:

```cmd
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Download the dataset separately and place it in `data/raw/UNSW_NB15_training-set.csv`.

## Run the Full Workflow

With the virtual environment active, run:

```cmd
python main.py
python simulate.py
```

The training workflow generates the trained model, evaluation metrics, test predictions, and charts. The alert simulator generates alerts from the test predictions.

Alternatively, on Windows, run:

```cmd
run_project.bat
```

This script trains the model, generates alerts, and starts the API. Keep its terminal window open while using the API.

## Run the Flask API

To start only the API:

```cmd
python app.py
```

Health endpoint:

`http://127.0.0.1:5000/health`

Prediction endpoint:

`POST http://127.0.0.1:5000/predict`

Use the JSON request schema expected by `app.py`. A small example of the accepted input is available in the project code. Provide compatible network-traffic feature names and values for meaningful predictions.

## Run the Dashboard

Open a second Command Prompt in the project directory. Activate the virtual environment if necessary, then run:

```cmd
.venv\Scripts\python.exe dashboard.py
```

Open this address in your browser:

`http://127.0.0.1:5001`

The dashboard displays evaluation metrics and lets you test a sample traffic record. It uses the saved model and evaluation report.

## Evaluation Results

On the current held-out test split:

- Accuracy: 95.88%
- Attack precision: 97.05%
- Attack recall: 96.89%
- Attack F1-score: 96.97%

These are dataset-specific evaluation results, not guarantees of real-world performance. False positives and false negatives remain possible.

## Project Structure

```text
AI-Cybersecurity-Threat-Detection/
|-- app.py
|-- dashboard.py
|-- main.py
|-- predict.py
|-- simulate.py
|-- run_project.bat
|-- test_api.py
|-- requirements.txt
|-- README.md
|-- src/
|-- data/                 # Downloaded dataset; not committed
|-- models/               # Generated model; not committed
|-- outputs/              # Generated reports; not committed
|-- images/               # Evaluation charts
|-- templates/            # Dashboard HTML
|-- static/               # Dashboard CSS and JavaScript
 (Add cybersecurity dashboard and API tests)
```

The dataset and trained model are excluded from GitHub by `.gitignore`. They are created or downloaded locally as needed.


## ⚙️ Installation and Setup

- Use public datasets or traffic data you are authorized to analyze.
- Treat predictions as estimates, not confirmed incidents.
- Do not use this educational project as a replacement for professional security monitoring.
- Keep the demo API bound to localhost.
(Add cybersecurity dashboard and API tests)

### Prerequisites

- Python installed on your computer
- Git
- Command Prompt or another terminal

- Evaluate on an independent compatible dataset.
- Tune prediction thresholds and analyze false positives.
- Add automated tests for model and API behavior.
- Explore carefully controlled real-time integration in a separate environment.
 (Add cybersecurity dashboard and API tests)

### 1. Clone the repository


```cmd
git clone https://github.com/vyshnaviporandla/AI-Cybersecurity-Threat-Detection.git
cd AI-Cybersecurity-Threat-Detection
```

### 2. Create and activate a virtual environment

On Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the dataset

Visit the official UNSW-NB15 dataset page:

https://research.unsw.edu.au/projects/unsw-nb15-dataset

Download the training CSV named `UNSW_NB15_training-set.csv` and place it here:

```text
data/raw/UNSW_NB15_training-set.csv
```

Create the `data/raw` folders if they do not exist.

### 5. Train and evaluate the model

Run:

```cmd
python main.py
```

The training workflow creates the trained model and evaluation outputs, including the metrics, predictions, and visualization charts.

### 6. Generate alert reports

After training completes, run:

```cmd
python simulate.py
```

The script reads the test predictions and writes potential-attack alerts to:

```text
outputs/alerts/security_alerts.csv
```

The alert count depends on the generated predictions.

## 🌐 Running the Local Prediction API

Train the model first so that the saved model is available.

Start the Flask API:

```cmd
python app.py
```

The API runs locally at:

```text
http://127.0.0.1:5000
```

Keep this terminal open while testing the API.

### Health check

In another Command Prompt, run:

```cmd
python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"
```

The health endpoint reports the API status and whether the model has been loaded.

### Sample prediction request

With the API running, open a second Command Prompt, activate the virtual environment, and run:

```cmd
python -c "import json,urllib.request; data=json.dumps({'records':[{'proto':'tcp','service':'http','state':'FIN','dur':0.5,'sbytes':100,'dbytes':250}]}).encode(); req=urllib.request.Request('http://127.0.0.1:5000/predict',data=data,headers={'Content-Type':'application/json'},method='POST'); print(urllib.request.urlopen(req).read().decode())"
```

This sends one illustrative record to the local API. Its prediction is an estimate, not a confirmed security finding.

## 🔔 Alert Output

The alert simulation exports predicted potential attacks to a CSV file for inspection in spreadsheet software.

Example output location:

```text
outputs/alerts/security_alerts.csv
```

The report is generated from offline dataset predictions; it does not represent alerts collected from a live network.

## 🔐 Responsible Use and Limitations

- This project is intended for education, portfolio development, and offline experimentation.
- The model operates on supplied dataset records rather than capturing live network packets.
- A prediction labeled `Potential Attack` is not proof of malicious activity.
- False positives and false negatives are possible.
- The reported metrics should not be interpreted as a guarantee of real-world performance.
- Do not use this demonstration as the sole basis for security decisions.

## 🚀 Future Improvements

- Add automated unit and API tests.
- Build a simple dashboard for exploring predictions.
- Compare additional classification algorithms.
- Evaluate the model on a separate compatible dataset.
- Add model versioning and structured application logging.

## 👩‍💻 Author

**Vyshnavi Porandla**

B.Tech Computer Science and Engineering student interested in Python, machine learning, software development, and cybersecurity.

- **GitHub:** [@vyshnaviporandla](https://github.com/vyshnaviporandla)
- **Project repository:** [AI Cybersecurity Threat Detection](https://github.com/vyshnaviporandla/AI-Cybersecurity-Threat-Detection)

---

*Built as an educational machine learning and cybersecurity portfolio project.*
