import streamlit as st
import assemblyai as aai
import pickle
from text_processor import PreProcessText

# --- CONFIGURATION ---
aai.settings.api_key = "Your api key from assembly ai"

# Load your ML models
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# --- UI SETUP ---
st.title(":blue[VoxKey]")
st.subheader("Your Scam Detection Shield")
# Choice: Text or Audio
option = st.radio("Select Input Type:", ("Text Message", "Audio/Video File"))

input_message = ""

if option == "Text Message":
    input_message = st.text_area("Enter the message to analyze")

else:
    uploaded_file = st.file_uploader("Upload audio/video for transcription", type=['mp3', 'wav', 'mp4', 'm4a'])
    
    if uploaded_file is not None:
        with st.spinner("Transcribing audio... please wait."):
            try:
                # AssemblyAI can take the file buffer directly
                config = aai.TranscriptionConfig(speech_models=["universal"])
                transcriber = aai.Transcriber(config=config)
                
                # We pass the uploaded file bytes to AssemblyAI
                transcript = transcriber.transcribe(uploaded_file)
                
                if transcript.status == "error":
                    st.error(f"Transcription failed: {transcript.error}")
                else:
                    input_message = transcript.text
                    st.info(f"Transcribed Text: {input_message}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- PREDICTION LOGIC ---
if st.button("Analyze"):
    if input_message.strip() == "":
        st.warning("Please provide some text or an audio file first.")
    else:
        obj = PreProcessText()
        transform_message = obj.remove_punctuation(input_message)
        
        # Vectorize
        vector_input = tfidf.transform([transform_message])
        
        # Predict 
        result = model.predict(vector_input)[0]
        
        if result == 0:
            st.error("🚨 Warning: This appears to be a SCAM.")
        else:
            st.success("✅ This seems safe.")