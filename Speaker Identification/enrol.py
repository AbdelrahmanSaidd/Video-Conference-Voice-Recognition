import pyaudio
import wave
import sounddevice
import sys
from tqdm import tqdm
from IPython.display import Audio
from pydub import AudioSegment

print("script starts here")
# speaker_name = input("Name: ")
speaker_name = "Sheriff_new"
# two recordings in Arabic and two in English. each recording is 60 seconds
recording_number = "1"
# recording_number = input("Recording id (e1, e2, a1, a2): ")
# recording_length = int(input("Length in seocnds: "))
recording_length = 15




CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = int(recording_length) + 5.1
WAVE_OUTPUT_FILENAME = speaker_name + "_" + recording_number +".wav"

file_path = "" + WAVE_OUTPUT_FILENAME

record = True
vad = False

if record:
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Started recording...")
    frames = []

    for i in tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)


    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Done recording! - T")


import torch

output_file = file_path.split('.')[0]+ '.wav'

if vad:
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=True,
                                onnx=False)

    (get_speech_timestamps,
    save_audio,
    read_audio,
    VADIterator,
    collect_chunks) = utils

    file = WAVE_OUTPUT_FILENAME
    Audio(file)

    output_file = file_path.split('.')[0]+'_only_speech'+ '.wav'
    print(file)
    wav = read_audio(file, sampling_rate=RATE)
    # get speech timestamps from full audio file
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=RATE)
    # merge all speech chunks to one audio
    if speech_timestamps:
            save_audio(output_file,
                    collect_chunks(speech_timestamps, wav), sampling_rate=RATE) 
            Audio(output_file)
    else:
            print("No activity detected")
    Audio(output_file)


# Segmentation
from scipy.io import wavfile
import os

def trim_wav(input_file, output_folder, segment_name, offset=0):
    # Read the WAV file
    sample_rate, audio_data = wavfile.read(input_file)

    # Define the duration of each segment in samples (3 seconds)
    segment_duration = 3 * sample_rate

    # Calculate the number of segments
    num_segments = len(audio_data) // segment_duration
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Trim the audio into segments
    for i in range(num_segments):
        start_sample = i * segment_duration
        end_sample = (i + 1) * segment_duration
        segment = audio_data[start_sample:end_sample]
        # Save each segment as a separate WAV file
        output_file = os.path.join(output_folder, f"{segment_name}_{i+1+offset}.wav")
        wavfile.write(output_file, sample_rate, segment)

output_folder = output_file.split('.')[0]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Directory '{output_folder}' created successfully.")
else:
    print(f"Directory '{output_folder}' already exists.")

trim_wav(output_file, output_folder, output_folder, 0)


# Normalization
import glob

# Replace 'directory_path' with the actual directory path you want to read files from
directory_path = output_folder

# Use glob to get a list of all WAV files in the directory recursively
wav_files = glob.glob(directory_path + '/**/*.wav', recursive=True)

# Print the list of WAV files
print(wav_files)
for file_name in wav_files:
    with wave.open(file_name, 'rb') as wav_file:
        # Get the audio file properties
        sample_width = wav_file.getsampwidth()
        num_channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Read the audio data
        audio_data = wav_file.readframes(num_frames)

    # Convert the audio data to AudioSegment object
    audio = AudioSegment(
        data=audio_data,
        sample_width=sample_width,
        frame_rate=sample_rate,
        channels=num_channels
    )

    # Normalize the volume
    normalized_audio = audio.normalize()

    # Change the sampling rate to 1
    normalized_audio = normalized_audio.set_frame_rate(16000)

    # Combine all channels to one channel
    normalized_audio = normalized_audio.set_channels(1)

    # Export the normalized audio as WAV file
    normalized_audio.export(file_name, format='wav')


# training
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM
from FeatureExtraction import extract_features
#from speakerfeatures import extract_features
import warnings
import os
import sys
import time
warnings.filterwarnings("ignore")

time1 = time.time()
training = True
dest = "models/"

training_size = 18

directory = output_folder

# 1 speaker
# directory = directories[0]

# List all files in the directory
file_paths = os.listdir(directory)
file_paths = sorted(file_paths)
# print(file_paths)
# Extracting features for each speaker
features = np.asarray(())
for path in file_paths:
    path = directory + "/" + path    
    path = path.strip()   
    print (path)
    
    # read the audio
    sr,audio = read(path)
    
    # extract 40 dimensional MFCC & delta MFCC features
    vector   = extract_features(audio,sr)
    
    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))

if training:            
    gmm = GMM(n_components = 5, covariance_type='diag',n_init = 3)
    gmm.fit(features)
    # dumping the trained gaussian model
    picklefile = directory + ".gmm"
    print(picklefile)
    
    if not os.path.exists("models"):
        os.makedirs("models")
        print(f"Directory 'models' created successfully.")
    else:
        print(f"Directory 'models' already exists.")

    cPickle.dump(gmm,open(dest + picklefile,'wb'))
    print ('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
    features = np.asarray(())
print("Total Time taken: ", round(time.time() - time1, 2), "seconds")
