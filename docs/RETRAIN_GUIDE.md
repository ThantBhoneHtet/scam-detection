# Model Retraining Guide

## Overview

Your scam detection model uses:
- **CountVectorizer** (Bag of Words): Converts text to numerical vectors
- **TfidfTransformer**: Converts word counts to TF-IDF scores
- **MultinomialNB**: Naive Bayes classifier

Both are saved as pickle files: `vectorizer.pkl` and `model.pkl`

## Why You Can't "Open" Pickle Files

Pickle files are binary Python objects, not human-readable. They can only be opened/loaded by Python code using `pickle.load()`.

## Retraining Your Model

### Option 1: Quick Retrain (Easiest)

```bash
python quick_retrain.py
```

This automatically:
- Loads your existing CSV datasets
- Combines them
- Retrains the model with all data
- Saves new `vectorizer.pkl` and `model.pkl`
- Creates backups of old models

### Option 2: Full Control Retraining

```bash
python retrain_model.py
```

This provides detailed output and metrics, showing:
- Training accuracy
- Classification report
- Confusion matrix

## Adding New Datasets

### Format Required
Your CSV files need these columns:
- `message` or `text`: The scam/non-scam message
- `label`: 0 for scam, 1 for not scam

### Step-by-Step to Add New Data

1. **Prepare your CSV file** with columns: `message`, `label`
2. **Save it** to `Datasets/` folder
3. **Edit `retrain_model.py`** and add your file in the `main()` function:

```python
# Add this line in the load_data_from_csv section
df_new = load_data_from_csv('Datasets/your_new_file.csv')
if df_new is not None:
    datasets.append(df_new)
```

4. **Run retraining**:
```bash
python retrain_model.py
```

## Python Script Template for Custom Data

```python
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# Load your new training data
df = pd.read_csv('your_data.csv')  # Must have 'message' and 'label' columns

# Create preprocessor (same as original)
from retrain_model import PreProcessText
obj = PreProcessText()

# Retrain
bow = CountVectorizer(analyzer=obj.token_words).fit(df['message'])
bow_transformed = bow.transform(df['message'])
tfidf = TfidfTransformer().fit(bow_transformed)
tfidf_transformed = tfidf.transform(bow_transformed)
model = MultinomialNB().fit(tfidf_transformed, df['label'])

# Save
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(bow, f)
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model retrained and saved!")
```

## Using the New Model

After retraining, your `app.py` and `integrated.py` will automatically use the new models:

```python
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Now use with new data
text = "Your message here"
processed = obj.remove_punctuation(text)
vector = tfidf.transform([processed])
prediction = model.predict(vector)[0]
```

## Backing Up Models

Both scripts automatically create backups:
- `vectorizer_backup.pkl` ← old vectorizer
- `model_backup.pkl` ← old model

If something goes wrong, restore from backups:
```python
import shutil
shutil.copy('vectorizer_backup.pkl', 'vectorizer.pkl')
shutil.copy('model_backup.pkl', 'model.pkl')
```

## What Data To Collect

For best results, add:
- **More scam messages**: Real scam transcripts or SMS
- **More legitimate messages**: Normal conversations, authentic communications
- **Different sources**: Different scam types, regional variations
- **Better balance**: Similar count of scam vs. legitimate messages

## Performance Tips

1. **Larger dataset = Better model** (generally)
2. **Balanced data = Better predictions** (50% scam, 50% legitimate)
3. **Clean data = Better accuracy** (remove duplicates, fix encoding)
4. **Check accuracy** after retraining to ensure it improved

## Troubleshooting

**Error: Column not found**
- Check your CSV has 'message' and 'label' columns
- Or modify the script to use your column names

**Error: Can't open pickle file**
- Make sure `vectorizer.pkl` and `model.pkl` exist
- Try retraining to generate new ones

**Low accuracy after retraining**
- Your new data might be unbalanced
- Check data quality for errors
- Retrain with more balanced dataset

## Advanced: Incremental Learning

To continuously retrain without losing knowledge:

```python
# Load existing model
old_model = pickle.load(open('model.pkl', 'rb'))

# Load your old + new data combined
all_data = pd.concat([old_data, new_data])

# Retrain on combined dataset (not just new data)
# This preserves learned patterns from old data
```

---

For questions, check the training notebook in `index.ipynb`
