"""
Unified data loader with automatic label normalization
Handles different label formats across datasets
"""

import pandas as pd
import os

class LabelNormalizer:
    """
    Normalizes labels to standard format: 0 (scam/spam) and 1 (legitimate/ham)
    """
    
    # Define label mapping patterns
    LABEL_MAPPINGS = {
        # Format: {original_label: normalized_label}
        # 0 = SCAM/SPAM, 1 = LEGITIMATE/HAM
        
        # Common scam/spam terms -> 0
        'fraud': 0,
        'spam': 0,
        'scam': 0,
        'phishing': 0,
        'malicious': 0,
        'fake': 0,
        '0': 0,
        0: 0,
        'false': 0,
        False: 0,
        
        # Common legitimate terms -> 1
        'normal': 1,
        'ham': 1,
        'legitimate': 1,
        'authentic': 1,
        'real': 1,
        '1': 1,
        1: 1,
        'true': 1,
        True: 1,
    }
    
    @staticmethod
    def normalize(label):
        """Convert any label format to 0 or 1"""
        if pd.isna(label):
            return None
        
        # Convert to string and lowercase for matching
        label_str = str(label).strip().lower()
        
        if label_str in LabelNormalizer.LABEL_MAPPINGS:
            return LabelNormalizer.LABEL_MAPPINGS[label_str]
        
        # Try original value
        if label in LabelNormalizer.LABEL_MAPPINGS:
            return LabelNormalizer.LABEL_MAPPINGS[label]
        
        raise ValueError(f"Unknown label format: {label}. Please add mapping in LabelNormalizer.LABEL_MAPPINGS")
    
    @staticmethod
    def add_custom_mapping(label_dict):
        """Add custom label mappings"""
        LabelNormalizer.LABEL_MAPPINGS.update(label_dict)


class DatasetLoader:
    """
    Loads datasets with automatic label normalization
    """
    
    @staticmethod
    def load_csv(file_path, text_column=None, label_column=None, has_header=True, 
                 label_col_index=0, text_col_index=1):
        """
        Load CSV and normalize labels
        
        Args:
            file_path: path to CSV file
            text_column: column name with text data (for files with headers)
            label_column: column name with labels (for files with headers)
            has_header: whether file has header row (default: True)
            label_col_index: column index for labels (for files without headers, default: 0)
            text_col_index: column index for text (for files without headers, default: 1)
        
        Returns:
            DataFrame with 'message' and 'label' columns (normalized)
        """
        print(f"\nLoading {file_path}...")
        try:
            # Load CSV with or without header
            if has_header:
                df = pd.read_csv(file_path)
                print(f"  Columns found: {df.columns.tolist()}")
                # Select relevant columns by name
                df = df[[label_column, text_column]].copy()
                df.columns = ['label', 'message']
            else:
                # Load without header, then select by index
                df = pd.read_csv(file_path, header=None)
                print(f"  No header - using column indices [{label_col_index}, {text_col_index}]")
                df = df[[label_col_index, text_col_index]].copy()
                df.columns = ['label', 'message']
            
            # Remove null values
            df = df.dropna()
            print(f"  Records before normalization: {len(df)}")
            
            # Normalize labels
            df['label'] = df['label'].apply(LabelNormalizer.normalize)
            
            # Check label distribution
            counts = df['label'].value_counts()
            print(f"  ✓ Loaded {len(df)} records")
            print(f"    - Scam (0): {counts.get(0, 0)}")
            print(f"    - Legitimate (1): {counts.get(1, 0)}")
            
            return df
        
        except Exception as e:
            print(f"  ✗ Error loading {file_path}: {e}")
            return None
    
    @staticmethod
    def load_tsv(file_path, label_column_index=0, text_column_index=1):
        """
        Load TSV file and normalize labels
        
        Args:
            file_path: path to TSV file
            label_column_index: column index containing labels
            text_column_index: column index containing text
        
        Returns:
            DataFrame with 'message' and 'label' columns (normalized)
        """
        print(f"\nLoading {file_path}...")
        try:
            df = pd.read_csv(file_path, sep='\t', header=None)
            print(f"  Columns found: {len(df.columns)}")
            
            # Select relevant columns
            df = pd.DataFrame({
                'label': df.iloc[:, label_column_index],
                'message': df.iloc[:, text_column_index]
            })
            
            # Remove null values
            df = df.dropna()
            print(f"  Records before normalization: {len(df)}")
            
            # Normalize labels
            df['label'] = df['label'].apply(LabelNormalizer.normalize)
            
            # Check label distribution
            counts = df['label'].value_counts()
            print(f"  ✓ Loaded {len(df)} records")
            print(f"    - Scam (0): {counts.get(0, 0)}")
            print(f"    - Legitimate (1): {counts.get(1, 0)}")
            
            return df
        
        except Exception as e:
            print(f"  ✗ Error loading {file_path}: {e}")
            return None


class DatasetCombiner:
    """
    Combines multiple datasets with label normalization
    """
    
    @staticmethod
    def combine(*dataframes, balance=False):
        """
        Combine multiple dataframes
        
        Args:
            *dataframes: DataFrames to combine
            balance: if True, balance classes by undersampling majority class
        
        Returns:
            Combined DataFrame
        """
        combined = pd.concat(dataframes, ignore_index=True)
        
        print(f"\n=== Combined Dataset ===")
        print(f"Total records: {len(combined)}")
        
        counts = combined['label'].value_counts()
        print(f"  - Scam (0): {counts.get(0, 0)}")
        print(f"  - Legitimate (1): {counts.get(1, 0)}")
        
        if balance:
            print(f"\nBalancing dataset...")
            class_0 = combined[combined['label'] == 0]
            class_1 = combined[combined['label'] == 1]
            
            min_size = min(len(class_0), len(class_1))
            
            class_0_balanced = class_0.sample(n=min_size, random_state=42)
            class_1_balanced = class_1.sample(n=min_size, random_state=42)
            
            combined = pd.concat([class_0_balanced, class_1_balanced], ignore_index=True)
            print(f"After balancing: {len(combined)} records")
            print(f"  - Scam (0): {min_size}")
            print(f"  - Legitimate (1): {min_size}")
        
        return combined


def demo_load_all_datasets(balance=False):
    """
    Demo: Load all available datasets with automatic normalization
    """
    print("\n" + "="*60)
    print("UNIFIED DATASET LOADER - AUTO LABEL NORMALIZATION")
    print("="*60)
    
    datasets = []
    
    # Load MainCall.csv (fraud/normal, NO HEADERS)
    if os.path.exists('Datasets/MainCall.csv'):
        df = DatasetLoader.load_csv('Datasets/MainCall.csv',
                                   has_header=False,
                                   label_col_index=0,
                                   text_col_index=1)
        if df is not None:
            datasets.append(df)
    
    # Load Bigmaincall.csv (spam/ham, NO HEADERS)
    if os.path.exists('Datasets/Bigmaincall.csv'):
        df = DatasetLoader.load_csv('Datasets/Bigmaincall.csv',
                                   has_header=False,
                                   label_col_index=0,
                                   text_col_index=1)
        if df is not None:
            datasets.append(df)
    
    # Load SMSSpamCollection.txt (spam/ham in TSV format)
    if os.path.exists('Datasets/Default/SMSSpamCollection.txt'):
        df = DatasetLoader.load_tsv('Datasets/Default/SMSSpamCollection.txt',
                                   label_column_index=0,
                                   text_column_index=1)
        if df is not None:
            datasets.append(df)
    
    if not datasets:
        print("\n✗ No datasets found!")
        return None
    
    # Combine all datasets
    combined = DatasetCombiner.combine(*datasets, balance=balance)
    
    return combined


if __name__ == "__main__":
    # Test the loader
    combined_data = demo_load_all_datasets(balance=False)
    
    if combined_data is not None:
        print("\n" + "="*60)
        print("Sample combined data:")
        print("="*60)
        print(combined_data.head(10))
        print("\nLabel distribution:")
        print(combined_data['label'].value_counts())
