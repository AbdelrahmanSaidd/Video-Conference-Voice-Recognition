import base64
import io
from datetime import datetime

from flask import Flask, request
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os

import socket

def check_port(ip_address, port):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout in seconds (optional)
    sock.settimeout(1)
    try:
        # Try to connect to the IP address and port
        sock.connect((ip_address, port))
        # If connection succeeds, port is open
        print(f"Port {port} is open on {ip_address}")
        return True
    except Exception as e:
        # If connection fails, port is closed
        print(f"Port {port} is closed on {ip_address}: {e}")
        return False
    finally:
        # Always close the socket
        sock.close()

# Example usage:
check_port("127.0.0.1", 5000)

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
    file_path = os.path.join('/app/', filename)

    # Convert the audio file to .wav format in memory
    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
        audio.export(file_path, format='wav')
        print(f'Audio file converted to .wav: {file_path}')
    except Exception as e:
        print(f'Error converting audio to .wav: {e}')
        return 'Error converting audio to .wav'

    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
        audio.export(file_path, format='wav')
        print(f'Audio file converted to .wav: {file_path}')
    except Exception as e:
        print(f'Error converting audio to .wav: {e}')
        return 'Error converting audio to .wav'
    
    
    print(f'Audio file saved as .wav: {file_path}')
  
    while TRUE:
        try:
            with open(file_path, 'w') as file: 
                print("file opened")
                break
        except Error: 
            print("file not opened")

    
    
    return 'Audio file received and saved as .wav.'
 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
