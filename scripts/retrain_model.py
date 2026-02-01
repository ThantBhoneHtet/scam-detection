"""
Retrain the scam detection model with additional datasets
Auto-handles different label formats across datasets
"""

import pickle
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os
from data_loader import DatasetLoader, DatasetCombiner
from text_processor import PreProcessText

# Download required NLTK data
nltk.download('stopwords', quiet=True)

def load_data_from_csv(file_path, has_header=True, text_column=None, label_column=None,
                       label_col_index=0, text_col_index=1):
    """Load data from CSV file with automatic label normalization"""
    return DatasetLoader.load_csv(file_path, text_column, label_column, 
                                 has_header, label_col_index, text_col_index)


def load_data_from_tsv(file_path, label_col_index=0, text_col_index=1):
    """Load data from TSV file with automatic label normalization"""
    return DatasetLoader.load_tsv(file_path, label_col_index, text_col_index)


def combine_datasets(*dataframes, balance=False):
    """Combine multiple dataframes with optional balancing"""
    return DatasetCombiner.combine(*dataframes, balance=balance)


def retrain_model(training_data, text_column='message', label_column='label'):
    """
    Retrain the model with new data
    
    Parameters:
    - training_data: DataFrame with text and label columns
    - text_column: name of the column containing text messages
    - label_column: name of the column containing labels (0 or 1)
    """
    print("\n=== Starting Model Retraining ===\n")
    
    # Initialize preprocessor
    obj = PreProcessText()
    
    # Step 1: Create and fit CountVectorizer (Bag of Words)
    print("Step 1: Training CountVectorizer (Bag of Words)...")
    bow_transformer = CountVectorizer(analyzer=obj.token_words).fit(training_data[text_column])
    messages_bow = bow_transformer.transform(training_data[text_column])
    print(f"  - Vocabulary size: {len(bow_transformer.get_feature_names_out())}")
    
    # Step 2: Create and fit TfidfTransformer
    print("Step 2: Training TfidfTransformer...")
    tfidf_transformer = TfidfTransformer().fit(messages_bow)
    messages_tfidf = tfidf_transformer.transform(messages_bow)
    print(f"  - TF-IDF matrix shape: {messages_tfidf.shape}")
    
    # Step 3: Train Naive Bayes classifier
    print("Step 3: Training Naive Bayes classifier...")
    model = MultinomialNB().fit(messages_tfidf, training_data[label_column])
    print(f"  - Model trained successfully")
    
    # Step 4: Evaluate on training data
    print("\nStep 4: Evaluating model...")
    all_predictions = model.predict(messages_tfidf)
    accuracy = accuracy_score(training_data[label_column], all_predictions)
    print(f"  - Training Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(training_data[label_column], all_predictions, 
                               target_names=['Scam', 'Not Scam']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(training_data[label_column], all_predictions))
    
    return bow_transformer, tfidf_transformer, model


def save_models(bow_transformer, tfidf_transformer, model):
    """Save trained models to pickle files"""
    print("\n=== Saving Models ===\n")
    
    # Backup old models
    if os.path.exists('vectorizer.pkl'):
        if os.path.exists('vectorizer_backup.pkl'):
            os.remove('vectorizer_backup.pkl')
        os.rename('vectorizer.pkl', 'vectorizer_backup.pkl')
        print("Backed up old vectorizer.pkl to vectorizer_backup.pkl")
    
    if os.path.exists('model.pkl'):
        if os.path.exists('model_backup.pkl'):
            os.remove('model_backup.pkl')
        os.rename('model.pkl', 'model_backup.pkl')
        print("Backed up old model.pkl to model_backup.pkl")
    
    # Save new models
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(bow_transformer, f)
    print("Saved new vectorizer.pkl")
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Saved new model.pkl")
    
    print("\nModels saved successfully!")


def main():
    """Main retraining function"""
    
    print("\n" + "="*70)
    print("SCAM DETECTION MODEL RETRAINER - WITH AUTO LABEL NORMALIZATION")
    print("="*70)
    print("\nLoading datasets with automatic label mapping:")
    print("  - MainCall.csv (fraud/normal) → 0/1")
    print("  - Bigmaincall.csv (spam/ham) → 0/1")
    print("  - SMSSpamCollection (spam/ham) → 0/1")
    
    datasets = []
    
    # Load MainCall.csv (fraud/normal format, NO HEADERS)
    if os.path.exists('Datasets/MainCall.csv'):
        df1 = load_data_from_csv('Datasets/MainCall.csv', 
                                has_header=False,
                                label_col_index=0,
                                text_col_index=1)
        if df1 is not None:
            datasets.append(df1)
    
    # Load Bigmaincall.csv (spam/ham format, NO HEADERS)
    if os.path.exists('Datasets/Bigmaincall.csv'):
        df2 = load_data_from_csv('Datasets/Bigmaincall.csv',
                                has_header=False,
                                label_col_index=0,
                                text_col_index=1)
        if df2 is not None:
            datasets.append(df2)
    
    # Load SMSSpamCollection.txt (TSV format with spam/ham)
    if os.path.exists('Datasets/Default/SMSSpamCollection.txt'):
        df3 = load_data_from_tsv('Datasets/Default/SMSSpamCollection.txt',
                                label_col_index=0,
                                text_col_index=1)
        if df3 is not None:
            datasets.append(df3)
    
    if not datasets:
        print("\nERROR: No datasets found!")
        print("Please ensure you have CSV files in:")
        print("  - Datasets/MainCall.csv")
        print("  - Datasets/Bigmaincall.csv")
        print("  - Datasets/Default/SMSSpamCollection.txt")
        return
    
    # Combine all datasets (with optional balancing)
    print()
    combined_data = combine_datasets(*datasets, balance=False)
    
    # Retrain model
    bow_transformer, tfidf_transformer, model = retrain_model(combined_data)
    
    # Save models
    save_models(bow_transformer, tfidf_transformer, model)


if __name__ == "__main__":
    main()
