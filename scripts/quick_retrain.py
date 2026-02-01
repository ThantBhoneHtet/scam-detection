"""
Quick retraining script with automatic label normalization
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

nltk.download('stopwords', quiet=True)

def retrain_with_new_data():
    """Interactive retraining with automatic label normalization"""
    
    obj = PreProcessText()
    all_data = []
    
    print("\n=== Scam Detection Model Retrainer ===\n")
    print("Loading datasets with AUTO LABEL NORMALIZATION:")
    print("  fraud/normal → 0/1")
    print("  spam/ham → 0/1\n")
    
    # Load MainCall.csv (fraud/normal, NO HEADERS)
    if os.path.exists('Datasets/MainCall.csv'):
        df = DatasetLoader.load_csv('Datasets/MainCall.csv',
                                   has_header=False,
                                   label_col_index=0,
                                   text_col_index=1)
        if df is not None:
            all_data.append(df)
    
    # Load Bigmaincall.csv (spam/ham, NO HEADERS)
    if os.path.exists('Datasets/Bigmaincall.csv'):
        df = DatasetLoader.load_csv('Datasets/Bigmaincall.csv',
                                   has_header=False,
                                   label_col_index=0,
                                   text_col_index=1)
        if df is not None:
            all_data.append(df)
    
    # Load SMSSpamCollection.txt (TSV format)
    if os.path.exists('Datasets/Default/SMSSpamCollection.txt'):
        df = DatasetLoader.load_tsv('Datasets/Default/SMSSpamCollection.txt',
                                   label_column_index=0,
                                   text_column_index=1)
        if df is not None:
            all_data.append(df)
    
    # Combine data
    if all_data:
        training_data = DatasetCombiner.combine(*all_data, balance=False)
        
        # Train
        print("\n=== Training Model ===")
        bow = CountVectorizer(analyzer=obj.token_words).fit(training_data['message'])
        bow_transformed = bow.transform(training_data['message'])
        tfidf = TfidfTransformer().fit(bow_transformed)
        tfidf_transformed = tfidf.transform(bow_transformed)
        model = MultinomialNB().fit(tfidf_transformed, training_data['label'])
        
        # Evaluate
        predictions = model.predict(tfidf_transformed)
        accuracy = accuracy_score(training_data['label'], predictions)
        print(f"Training Accuracy: {accuracy:.4f}\n")
        print(classification_report(training_data['label'], predictions,
                                   target_names=['Scam', 'Legitimate']))
        
        # Save
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(bow, f)
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        print("✓ Models saved successfully!")
    else:
        print("✗ No datasets found!")


if __name__ == "__main__":
    retrain_with_new_data()
