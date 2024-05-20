import base64
import io
import os
from datetime import datetime

from flask import Flask, request
from pydub import AudioSegment
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

last_audio = None
# previous_audios = []

@app.route('/', methods=['POST'])
def process_audio():
    global last_audio
    global previous_audios
    # Check if the POST request has the file part
    if 'audio' not in request.form:
        print('No audio file in request.')
        return 'No audio file in request.'
    
    if 'speakerName' in request.form:
        print(request.form)
        speakerName = request.form['speakerName']
        print(f'Speaker name: {speakerName}')

    # Decode the base64 audio data
    audio_data = base64.b64decode(request.form['audio'].split(',')[1])
    audio_file = io.BytesIO(audio_data)

    # Convert the audio file to .wav format in memory
    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
    except Exception as e:
        print(f'Error converting audio to .wav: {e}')
        return 'Error converting audio to .wav'


    # # Add the current audio to previous_audios
    # previous_audios.append(audio)

    # if last_audio is not None:
    #     audio=last_audio[-2000:]+audio[:1000]
        
    # # Check if the combined audio is less than 3 seconds
    # while len(audio) < 3000:
    #     # Check if there are no more previous audios
    #     if not previous_audios:
    #         break
    #
    #     # Take the last audio segment from previous_audios
    #     previous_audio = previous_audios.pop()
    #
    #     # Calculate the amount of audio needed
    #     audio_needed = 3000 - len(audio)
    #
    #     # Check if the previous_audio is long enough
    #     if len(previous_audio) < audio_needed:
    #         # If the previous_audio is not long enough, break the loop
    #         break
    #     else:
    #         # Take the needed audio from previous_audio
    #         needed_audio = previous_audio[-audio_needed:]
    #
    #     # Prepend the needed audio to the audio
    #     audio = needed_audio + audio

    # Remove the used audio from last_audio
    # if last_audio is not None:
    #     last_audio = last_audio[:-len(audio)]

    # Update the last audio
    last_audio = audio

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = secure_filename(f'audio_{timestamp}.wav')
    file_path = os.path.join('wavefiles/', filename)

    # Save the audio file
    try:
        audio.export(file_path, format='wav')
        print(f'Audio file saved as .wav: {file_path}')
    except Exception as e:
        print(f'Error saving audio file: {e}')
        return 'Error saving audio file.'

    # # Resample the audio to 16000 Hz
    # resampled_audio = audio.set_frame_rate(16000)

    # # Save the resampled audio file with a different name
    # resampled_filename = secure_filename(f'audio_{timestamp}_resampled.wav')
    # resampled_file_path = os.path.join('wavefilesresampled/', resampled_filename)
    # try:
    #     resampled_audio.export(resampled_file_path, format='wav')
    #     print(f'Resampled audio file saved as .wav: {resampled_file_path}')
    # except Exception as e:
    #     print(f'Error saving resampled audio file: {e}')
    #     return 'Error saving resampled audio file.'
    
    with open("audiopath.txt", 'w') as f:
        f.write(file_path)
        f.close()
    # with open("audiopathresampled.txt", 'w') as f:
    #     f.write(resampled_file_path)
    #     f.close()
    
    with open("speaker.txt", 'r') as f:
        return f.read()

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
