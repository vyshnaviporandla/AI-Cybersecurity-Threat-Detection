# 🛡️ AI Cybersecurity Threat Detection

A machine learning project that classifies network traffic as **Normal** or **Potential Attack** using the UNSW-NB15 dataset. The project includes data preprocessing, model evaluation, visual reports, automated alert generation, and a Flask prediction API.

> **Note:** This is an educational, offline dataset-based demonstration. It does not monitor live network traffic or confirm real-world attacks.

## 📌 Project Overview

Cybersecurity teams need ways to identify suspicious network activity. This project demonstrates how supervised machine learning can learn patterns from labeled network traffic and classify unseen test records.

### 🎯 Objectives

- Classify network traffic as normal or potentially malicious.
- Evaluate the classifier using standard machine learning metrics.
- Visualize model performance and dataset label distribution.
- Generate CSV reports of predicted potential attacks.
- Provide a local REST API for sample traffic classification.

## ✨ Features

- **Data preprocessing:** Handles numerical and categorical network features.
- **Machine learning:** Trains a classifier using Scikit-learn.
- **Model evaluation:** Calculates accuracy, precision, recall, F1-score, and a confusion matrix.
- **Visual reports:** Generates charts for model evaluation and label distribution.
- **Alert simulation:** Creates a CSV report from model predictions.
- **REST API:** Provides local health-check and prediction endpoints through Flask.
- **Reproducible workflow:** Separates data loading, preprocessing, training, visualization, and alert generation into modules.

## 🧰 Technology Stack

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

### Confusion Matrix

| Actual class | Predicted Normal | Predicted Attack |
|---|---:|---:|
| Normal | 10,498 | 702 |
| Attack | 742 | 23,127 |

The model correctly classified many normal and attack records, but it also produced false positives and false negatives. These results apply to this dataset and test split; performance on other traffic may differ.

## 📈 Visualizations

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
```

The dataset and trained model are excluded from GitHub by `.gitignore`. They are created or downloaded locally as needed.

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your computer
- Git
- Command Prompt or another terminal

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
