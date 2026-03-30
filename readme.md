# Ransomware Detection

A small Python project for detecting ransomware-like behavior in file system activity and portable executable features. This repository contains a lightweight pipeline for feature extraction, model training, and a simple detection runner.

## Features
- Feature extraction from file metadata and binary characteristics
- Trainable ML model (scikit-learn compatible) for classification
- Quick CLI runner for scanning files or directories
- Scripts for training, evaluating, and exporting models

## Requirements
- Python 3.8+
- Typical packages: pandas, numpy, scikit-learn, joblib

Install packages (recommended inside a virtual environment):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # create this file if needed
```

If you don't have a `requirements.txt`, install minimal deps manually:

```powershell
pip install pandas numpy scikit-learn joblib
```

## Quick Start
Run the provided detector script to scan a file or directory. Replace arguments as needed.

```powershell
python ransomware.py --help
python ransomware.py --input path\to\sample.exe
python ransomware.py --scan-dir path\to\samples
```

The script prints a detection score and a simple label (`benign` / `ransomware`) depending on the trained model shipped or specified.

## Training a Model
If you have labeled feature data (CSV), train a new model with the training script (example):

```powershell
python ransomware.py --train --data data/features.csv --model-out models/rf_model.joblib
```

Training notes:
- Ensure the CSV contains a target column named `label` (0 = benign, 1 = ransomware) and matching feature columns used by the extractor.
- Use `scikit-learn` pipelines for reproducible preprocessing and training.

## Evaluation
Evaluate a saved model on a holdout dataset:

```powershell
python ransomware.py --evaluate --data data/test_features.csv --model models/rf_model.joblib
```

The evaluation will print metrics such as accuracy, precision, recall, and confusion matrix.

## Dataset
This repository does not include malware samples. Use responsibly and follow legal/ethical guidelines when collecting and handling malware or suspicious binaries. Prefer public, curated datasets from trusted sources, and analyze in an isolated, controlled environment.

## Contributing
- Open an issue for feature requests or bugs.
- For code contributions, fork the repo, create a feature branch, and open a pull request with tests where appropriate.

## License & Safety
This project is intended for research and defensive purposes. Do not use it for malicious activities. Verify the license in the repository root or ask the maintainer for clarification before using the code in production.

---

If you'd like, I can also create a `requirements.txt`, add example dataset stubs, or show exactly how `ransomware.py` expects input/CLI args — tell me which next step you prefer.
