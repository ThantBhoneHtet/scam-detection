import streamlit as st
import websockets
import asyncio
import json
import pyaudio
import os
from pathlib import Path

if 'text' not in st.session_state:
	st.session_state['text'] = 'Listening...'
	st.session_state['run'] = False

# Audio parameters 
st.sidebar.header('Audio Parameters')

FRAMES_PER_BUFFER = int(st.sidebar.text_input('Frames per buffer', 3200))
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = int(st.sidebar.text_input('Rate', 16000))
p = pyaudio.PyAudio()
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# Start/stop audio transmission
def start_listening():
	st.session_state['run'] = True

def download_transcription():
	read_txt = open('transcription.txt', 'r')
	st.download_button(
		label="Download transcription",
		data=read_txt,
		file_name='transcription_output.txt',
		mime='text/plain')

def stop_listening():
	st.session_state['run'] = False

# Web user interface
st.title('🎙️ Real-Time Transcription App')
col1, col2 = st.columns(2)

col1.button('Start', on_click=start_listening)
col2.button('Stop', on_click=stop_listening)

# Display transcription output area
st.markdown("---")
st.subheader("📝 Transcription Output")
transcription_placeholder = st.empty()
status_placeholder = st.empty()

# Send audio (Input) / Receive transcription (Output)
async def send_receive():
	URL = f"wss://streaming.assemblyai.com/v3/ws?sample_rate={RATE}&model=default"

	print(f'Connecting websocket to url ${URL}')

	headers = {"Authorization": st.secrets['api_key']}
	
	async with websockets.connect(
		URL,
		subprotocols=["chat"],
		additional_headers=headers,
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		r = await asyncio.sleep(0.1)
		print("Receiving messages ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")
		status_placeholder.success("✅ Connected to transcription service")


		async def send():
			while st.session_state['run']:
				try:
					data = stream.read(FRAMES_PER_BUFFER)
					# Send raw binary audio data, not JSON
					r = await _ws.send(data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(f"Connection closed: {e}")
					status_placeholder.warning("⚠️ Connection closed")
					break

				except Exception as e:
					print(f"Error in send: {e}")
					status_placeholder.error(f"❌ Error: {e}")
					break

				r = await asyncio.sleep(0.01)


		async def receive():
			while st.session_state['run']:
				try:
					result_str = await _ws.recv()
					result_json = json.loads(result_str)
					
					# Skip non-transcript messages
					if result_json.get('type') == 'Begin':
						print(f"Session started: {result_json.get('id')}")
						continue
					
					if 'text' in result_json and result_json['text']:
						result = result_json['text']
						message_type = result_json.get('message_type', 'Unknown')

						if message_type == 'FinalTranscript':
							print(f"Final: {result}")
							st.session_state['text'] = result
							transcription_placeholder.success(f"**Final:** {result}")

							# Save to file
							transcription_txt = open('transcription.txt', 'a')
							transcription_txt.write(result)
							transcription_txt.write(' ')
							transcription_txt.close()
						
						elif message_type == 'PartialTranscript':
							print(f"Partial: {result}")
							transcription_placeholder.info(f"*Partial:* {result}")


				except websockets.exceptions.ConnectionClosedError as e:
					print(f"Connection closed: {e}")
					status_placeholder.warning("⚠️ Connection closed")
					break

				except json.JSONDecodeError as e:
					print(f"JSON decode error: {e}")
					break

				except KeyError as e:
					print(f"Key error: {e}")
					break

				except Exception as e:
					print(f"Error in receive: {e}")
					status_placeholder.error(f"❌ Error: {e}")
					break
			
		send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())

if Path('transcription.txt').is_file():
	st.markdown('### Download')
	download_transcription()
	os.remove('transcription.txt')