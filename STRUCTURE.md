# 📁 Scam Detection Project - File Organization Guide

Welcome! This project is organized for easy navigation and use. Here's the complete structure:

## 📂 Project Structure

```
Scam-Detection/
├── 📄 README.md (→ in docs/)
│
├── 🚀 QUICK START SCRIPTS (root level)
│   ├── retrain.py                 # Retrain model with new data
│   ├── run_audio_app.py          # Run audio/video scam detection
│   └── run_text_app.py           # Run text message scam detection
│
├── 📁 docs/                        # 📚 DOCUMENTATION
│   ├── README.md                   # Project overview & setup
│   ├── RETRAIN_GUIDE.md           # How to retrain the model
│   └── LABEL_NORMALIZATION_GUIDE.md # Different label formats
│
├── 📁 scripts/                     # 🐍 PYTHON SCRIPTS
│   │
│   ├── 🎯 Main Applications
│   │   ├── app.py                 # Text message scam detector
│   │   ├── audio_input.py         # Audio/video scam detector (Streamlit)
│   │   ├── integrated.py          # Integrated prediction system
│   │   └── live.py                # Live audio processing
│   │
│   ├── 🔄 Model Training & Retraining
│   │   ├── retrain_model.py       # Full retraining with metrics
│   │   └── quick_retrain.py       # Quick retraining script
│   │
│   ├── 🛠️ Utilities & Data Processing
│   │   ├── text_processor.py      # Text preprocessing (shared)
│   │   ├── data_loader.py         # Dataset loading & normalization
│   │   ├── transcribe.py          # Audio transcription
│   │   ├── transcriber.py         # Assembly AI transcriber
│   │   └── main.py                # Main entry point
│   │
│   └── 📦 Models (Auto-generated)
│       ├── vectorizer.pkl         # TF-IDF vectorizer
│       ├── model.pkl              # Naive Bayes classifier
│       ├── vectorizer_backup.pkl  # Previous vectorizer
│       └── model_backup.pkl       # Previous model
│
├── 📁 notebooks/                   # 📓 JUPYTER NOTEBOOKS
│   ├── index.ipynb               # Main training notebook
│   ├── index2.ipynb              # Secondary analysis
│   ├── index3.ipynb              # Model evaluation
│   ├── index4.ipynb              # Advanced experiments
│   ├── transcribe.ipynb          # Transcription experiments
│   └── transcribe2.ipynb         # More transcription work
│
├── 📁 Datasets/                    # 📊 TRAINING DATA
│   ├── MainCall.csv              # Fraud call transcripts
│   ├── Bigmaincall.csv           # Extended call dataset
│   └── Default/
│       ├── SMSSpamCollection.txt  # SMS spam collection
│       └── fraud_call.csv         # Fraud call records
│
├── 📁 Conversation/                # 🗣️ CONVERSATION DATA
│   └── dataset/
│       ├── raw/
│       ├── test/
│       ├── train/
│       └── valid/
│
├── ⚙️ CONFIG FILES (root level)
│   ├── requirements.txt           # Python dependencies
│   ├── pyproject.toml             # Project metadata
│   └── .venv/                     # Virtual environment
│
└── 📁 remove/                      # (Ignore - legacy files)
```

---

## 🚀 Quick Start

### 1️⃣ Detect Scam in Text Messages
```bash
streamlit run scripts/app.py
```

### 2️⃣ Detect Scam in Audio/Video
```bash
streamlit run scripts/audio_input.py
```

### 3️⃣ Retrain Model with New Data
```bash
python scripts/retrain_model.py
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [docs/README.md](docs/README.md) | Project setup & overview |
| [docs/RETRAIN_GUIDE.md](docs/RETRAIN_GUIDE.md) | How to retrain & add datasets |
| [docs/LABEL_NORMALIZATION_GUIDE.md](docs/LABEL_NORMALIZATION_GUIDE.md) | Handle different label formats |

---

## 🐍 Python Scripts Overview

### Main Applications

| Script | Purpose |
|--------|---------|
| `scripts/app.py` | Streamlit web app for text message analysis |
| `scripts/audio_input.py` | Streamlit web app for audio/video analysis |
| `scripts/integrated.py` | Combined audio + text detection system |
| `scripts/live.py` | Real-time audio stream processing |

### Model Training

| Script | Purpose |
|--------|---------|
| `scripts/retrain_model.py` | **Full retraining** with detailed metrics |
| `scripts/quick_retrain.py` | **Quick retraining** (faster) |

### Utilities

| Script | Purpose |
|--------|---------|
| `scripts/text_processor.py` | **Shared** text preprocessing (used by all) |
| `scripts/data_loader.py` | Dataset loading with auto label normalization |
| `scripts/transcribe.py` | Audio transcription using Whisper |
| `scripts/transcriber.py` | Assembly AI transcription |
| `scripts/main.py` | Entry point |

---

## 📊 Data Files

### Datasets (Training Data)

| File | Records | Format | Labels |
|------|---------|--------|--------|
| `Datasets/MainCall.csv` | 5,925 | CSV (no header) | fraud/normal |
| `Datasets/Bigmaincall.csv` | 11,497 | CSV (no header) | spam/ham |
| `Datasets/Default/SMSSpamCollection.txt` | 5,572 | TSV | spam/ham |

**Total Training Data: 22,994 records**

### Models (Auto-generated after training)

| File | Purpose |
|------|---------|
| `scripts/vectorizer.pkl` | TF-IDF vectorizer (current) |
| `scripts/model.pkl` | Naive Bayes classifier (current) |
| `scripts/vectorizer_backup.pkl` | Previous vectorizer (backup) |
| `scripts/model_backup.pkl` | Previous model (backup) |

---

## 📓 Jupyter Notebooks

All notebooks are in `notebooks/` folder for exploratory analysis:

| Notebook | Purpose |
|----------|---------|
| `index.ipynb` | Main training & model development |
| `index2.ipynb` | Data analysis & EDA |
| `index3.ipynb` | Model evaluation |
| `index4.ipynb` | Advanced experiments |
| `transcribe.ipynb` | Audio transcription testing |
| `transcribe2.ipynb` | More transcription experiments |

---

## 🎯 Common Tasks


#### ✅ Add new training data & retrain
1. Prepare a CSV with `message` and `label` columns
2. Save to `Datasets/` folder
3. Edit `scripts/quick_retrain.py` to include your file
4. Run: `python retrain.py`

#### ✅ See detailed training metrics
```bash
python scripts/retrain_model.py
```

#### ✅ View or edit training notebooks
```bash
# Open with Jupyter Lab
jupyter lab notebooks/
```

#### ✅ Understand label mapping
See [docs/LABEL_NORMALIZATION_GUIDE.md](docs/LABEL_NORMALIZATION_GUIDE.md)

#### ✅ Get started with retraining
See [docs/RETRAIN_GUIDE.md](docs/RETRAIN_GUIDE.md)

---

## ⚙️ Configuration

### Python Environment
```
.venv/                    # Virtual environment (isolated)
requirements.txt          # Python package dependencies
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📊 Current Model Performance

- **Accuracy:** 99.50%
- **Training Data:** 22,994 messages
- **Scam Detection:** 96% recall
- **False Positives:** <1%

---

## 🔄 Model Components

1. **Text Preprocessing** (`text_processor.py`)
   - Remove punctuation
   - Remove stopwords
   - Tokenization

2. **Vectorization** (TF-IDF)
   - Converts text to numerical features
   - Vocabulary size: 12,181 words

3. **Classification** (Naive Bayes)
   - Classifies as Scam (0) or Legitimate (1)
   - Probability-based predictions

---

## 🆘 Troubleshooting

### Models won't load
→ See [docs/RETRAIN_GUIDE.md](docs/RETRAIN_GUIDE.md#error-cant-open-pickle-file)

### Label format errors
→ See [docs/LABEL_NORMALIZATION_GUIDE.md](docs/LABEL_NORMALIZATION_GUIDE.md)

### Import errors
→ Make sure you're in the right directory and virtual environment is activated

### Need to restore old model?
```bash
python -c "import shutil; shutil.copy('scripts/model_backup.pkl', 'scripts/model.pkl'); shutil.copy('scripts/vectorizer_backup.pkl', 'scripts/vectorizer.pkl'); print('✓ Restored!')"
```

---

## 📞 Need Help?

1. Check the relevant documentation file in `docs/`
2. Review the comments in the Python scripts
3. Look at example notebooks in `notebooks/`

---

## 📝 File Maintenance

Keep your workspace clean:
- ✅ Keep `scripts/` for all Python code
- ✅ Keep `docs/` for all documentation
- ✅ Keep `notebooks/` for exploration
- ✅ Keep `Datasets/` for training data only

**Never delete:**
- `scripts/text_processor.py` (used by all apps)
- `scripts/vectorizer.pkl` & `scripts/model.pkl` (the trained model)

---

Happy scam detecting! 🎯
