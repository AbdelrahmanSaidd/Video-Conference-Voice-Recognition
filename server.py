import base64
import io
from datetime import datetime

from flask import Flask, request
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_audio():
    # Check if the POST request has the file part
    if 'audio' not in request.form:
        print('No audio file in request.')
        return 'No audio file in request.'

    # Decode the base64 audio data
    audio_data = base64.b64decode(request.form['audio'].split(',')[1])
    audio_file = io.BytesIO(audio_data)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = secure_filename(f'audio_{timestamp}.wav')
    file_path = os.path.join('/Users/youssefabouelenin/Downloads', filename)

    # Convert the audio file to .wav format in memory
    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
        audio.export(file_path, format='wav')
        print(f'Audio file converted to .wav: {file_path}')
    except Exception as e:
        print(f'Error converting audio to .wav: {e}')
        return 'Error converting audio to .wav'

    print(f'Audio file saved as .wav: {file_path}')
    return 'Audio file received and saved as .wav.'


if __name__ == '__main__':
    app.run(port=8000)