import pickle
import streamlit as st
from text_processor import PreProcessText

tfidf=pickle.load(open('vectorizer.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))

# input

input_message=st.text_input("enter message")
if st.button("Analyze"):
        # pre process
    obj=PreProcessText()
    transform_message=obj.remove_punctuation(input_message)
    # vectorise
    # bow_transformer = CountVectorizer(analyzer=obj.token_words).fit(transform_message)

    vector_input=tfidf.transform([transform_message])
    # tfidf_transformer.transform([transform_message])
    # predict 
    result=model.predict(vector_input)[0]
    if result==0:
        st.header("scam")
    else:
        st.header("no scam")