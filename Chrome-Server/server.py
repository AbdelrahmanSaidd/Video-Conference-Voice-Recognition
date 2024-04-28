import base64
import io
import os
from datetime import datetime

from flask import Flask, request
from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)

last_audio = None

@app.route('/', methods=['POST'])
def process_audio():
    global last_audio
    # Check if the POST request has the file part
    if 'audio' not in request.form:
        print('No audio file in request.')
        return 'No audio file in request.'

    # Decode the base64 audio data
    audio_data = base64.b64decode(request.form['audio'].split(',')[1])
    audio_file = io.BytesIO(audio_data)

    # Convert the audio file to .wav format in memory
    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
    except Exception as e:
        print(f'Error converting audio to .wav: {e}')
        return 'Error converting audio to .wav'

    # Concatenate the last 2 seconds of the previous file with the first second of the new one
    if last_audio is not None:
        audio = last_audio[-2000:] + audio[:1000]

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = secure_filename(f'audio_{timestamp}.wav')
    file_path = os.path.join('/Users/youssefabouelenin/Downloads', filename)

    # Save the audio file
    try:
        audio.export(file_path, format='wav')
        print(f'Audio file saved as .wav: {file_path}')
    except Exception as e:
        print(f'Error saving audio file: {e}')
        return 'Error saving audio file.'

    # Update the last audio
    last_audio = audio

    return 'Audio file received and saved as .wav.'


if __name__ == '__main__':
    app.run(port=8000)
