"""
Shared text preprocessing utilities
Used by both training and prediction scripts
"""

import string
import nltk
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('stopwords', quiet=True)


class PreProcessText(object):
    """Text preprocessing for scam detection model"""
    
    def __init__(self):
        pass
    
    def remove_punctuation(self, text=''):
        """
        Remove punctuation from text
        Takes a String 
        Return: Return a String 
        """
        message = []
        for x in text:
            if x in string.punctuation:
                pass
            else:
                message.append(x)
        return ''.join(message)
    
    def remove_stopwords(self, text=''):
        """
        Remove stopwords from text
        Takes a String
        Return: List
        """
        words = []
        for x in text.split():
            if x.lower() not in stopwords.words('english'):
                words.append(x)
        return words
    
    def token_words(self, text=''):
        """
        Tokenize words in text
        Takes String
        Return: Token (list of words used to train the model)
        """
        message = self.remove_punctuation(text)
        words = self.remove_stopwords(message)
        return words
