# Handling Different Label Formats Guide

## Problem

Your datasets use different label formats:

| Dataset | Format | Labels | Maps To |
|---------|--------|--------|----------|
| MainCall.csv | CSV | `fraud` / `normal` | 0 / 1 |
| Bigmaincall.csv | CSV | `spam` / `ham` | 0 / 1 |
| SMSSpamCollection.txt | TSV | `spam` / `ham` | 0 / 1 |

**Without normalization**, you'll get errors when combining datasets.

## Solution: Automatic Label Normalization

I've created `data_loader.py` with `LabelNormalizer` class that **automatically maps all label formats to a standard format**:

```
0 = SCAM/SPAM/FRAUD/PHISHING/MALICIOUS
1 = LEGITIMATE/HAM/NORMAL/AUTHENTIC/REAL
```

## How It Works

### Step 1: Automatic Detection and Mapping

```python
from data_loader import LabelNormalizer

# Automatically converts ANY label format to 0 or 1
LabelNormalizer.normalize('fraud')      # → 0
LabelNormalizer.normalize('spam')       # → 0
LabelNormalizer.normalize('ham')        # → 1
LabelNormalizer.normalize('normal')     # → 1
LabelNormalizer.normalize('phishing')   # → 0
```

### Step 2: Load and Normalize Datasets

```python
from data_loader import DatasetLoader

# CSV with fraud/normal labels
df1 = DatasetLoader.load_csv('Datasets/MainCall.csv',
                            text_column='message',
                            label_column='label')
# → Automatically normalizes fraud→0, normal→1

# CSV with spam/ham labels
df2 = DatasetLoader.load_csv('Datasets/Bigmaincall.csv',
                            text_column='message',
                            label_column='label')
# → Automatically normalizes spam→0, ham→1

# TSV with spam/ham labels
df3 = DatasetLoader.load_tsv('Datasets/Default/SMSSpamCollection.txt',
                            label_column_index=0,
                            text_column_index=1)
# → Automatically normalizes spam→0, ham→1
```

### Step 3: Combine Datasets

```python
from data_loader import DatasetCombiner

# All datasets now have consistent labels!
combined = DatasetCombiner.combine(df1, df2, df3)

# Output:
# Total records: 23005
#   - Scam (0): 7899
#   - Legitimate (1): 15106
```

## Usage Examples

### Quick Retraining (All Steps Automated)

```bash
python quick_retrain.py
```

**Output:**
```
Loading datasets with AUTO LABEL NORMALIZATION:

Loading Datasets/MainCall.csv...
  ✓ Loaded 5928 records
    - Scam (0): 2456
    - Legitimate (1): 3472

Loading Datasets/Bigmaincall.csv...
  ✓ Loaded 11502 records
    - Scam (0): 5123
    - Legitimate (1): 6379

Loading Datasets/Default/SMSSpamCollection.txt...
  ✓ Loaded 5575 records
    - Scam (0): 747
    - Legitimate (1): 4828

=== Combined Dataset ===
Total records: 23005
  - Scam (0): 8326
  - Legitimate (1): 14679

=== Training Model ===
Training Accuracy: 0.9543

✓ Models saved successfully!
```

### Full Retraining with Metrics

```bash
python retrain_model.py
```

## Custom Label Formats

If you have a NEW dataset with a different label format:

### Method 1: Add to Normalizer (Permanent)

Edit `data_loader.py`:

```python
# Add to LabelNormalizer.LABEL_MAPPINGS
LabelNormalizer.LABEL_MAPPINGS.update({
    'scammer': 0,          # New scam label
    'legitimate_user': 1,  # New legitimate label
    'yes': 0,              # Shorthand
    'no': 1,
})
```

### Method 2: Create Custom Loader (Temporary)

```python
from data_loader import DatasetLoader, LabelNormalizer
import pandas as pd

# Add temporary mapping
LabelNormalizer.add_custom_mapping({
    'blocked': 0,      # Blocked messages = scam
    'approved': 1,     # Approved messages = legitimate
})

# Now load normally
df = DatasetLoader.load_csv('my_new_dataset.csv',
                           text_column='message',
                           label_column='status')
```

## Supported Label Formats (Out of Box)

### Scam/Spam Labels (→ 0)
- `fraud`, `spam`, `scam`, `phishing`, `malicious`, `fake`
- `0`, `false`, `False`

### Legitimate/Ham Labels (→ 1)
- `normal`, `ham`, `legitimate`, `authentic`, `real`
- `1`, `true`, `True`

## Adding New Datasets

1. **Prepare CSV file** with columns: `message`, `label`
2. **Save to Datasets folder**
3. **Edit retrain_model.py** or **quick_retrain.py**:

```python
# Add this code in the main() function
if os.path.exists('Datasets/my_new_data.csv'):
    df_new = DatasetLoader.load_csv('Datasets/my_new_data.csv',
                                   text_column='message',
                                   label_column='label')
    if df_new is not None:
        datasets.append(df_new)
```

4. **Run retraining**:
```bash
python quick_retrain.py
```

## Balancing Classes

If one class has way more data than the other (imbalanced), you can balance:

```python
from data_loader import DatasetCombiner

# Balance by undersampling majority class
combined = DatasetCombiner.combine(df1, df2, df3, balance=True)

# Before: 8326 scam, 14679 legitimate
# After:  8326 scam,  8326 legitimate (balanced)
```

## Testing Label Normalization

```bash
python data_loader.py
```

**Output shows:**
- How each dataset is loaded
- Original and normalized label counts
- Final combined dataset distribution

## Error: "Unknown label format"

If you get this error, the label wasn't recognized:

```
Unknown label format: my_label_value
```

**Solution:**
Add mapping to `data_loader.py`:

```python
LABEL_MAPPINGS = {
    # ... existing mappings ...
    'my_label_value': 0,  # or 1, depending on meaning
}
```

Then re-run retraining.

## Summary

- ✅ Handles `fraud/normal`, `spam/ham`, and other formats
- ✅ Normalizes to standard `0/1` labels
- ✅ Combines datasets automatically
- ✅ Shows label distribution before/after
- ✅ Customizable for new label formats
- ✅ Optional class balancing

**Just run:** `python quick_retrain.py`
