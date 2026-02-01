# Install the assemblyai package by executing the command "pip install assemblyai"

import assemblyai as aai

aai.settings.api_key = "Your api key from assembly ai"

# audio_file = "./local_file.mp3"
audio_file = "./final.mp4"

config = aai.TranscriptionConfig(speech_models=["universal"])

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

# print(transcript.sentiment_analysis)
print(transcript.text)