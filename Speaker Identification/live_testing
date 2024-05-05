import pyaudio
import wave
import subprocess
import sounddevice
import sys
import time
import os

from pydub import AudioSegment


import os
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from FeatureExtraction import extract_features
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
import sys

from io import BytesIO

source   = "2-wav_testing/"

same_output_file = False


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1.1
record_len = RECORD_SECONDS
wav_path = "output.wav"
record = True
vad = True
normalize = True
recognize = True
max_speaker_threshold = 0.50
condition = True
counter = 50
frames = []
frames2 = []
frames3 = []
load_models = True
dump_recordings = True
last_speaker = ""
weight = 0
while True:
    # condition = False
    counter += 1
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Started recording...", end="")

    if record:
        frames2 = frames2[len(frames2)//2:]
        frames3 = frames3[len(frames3)//3:]
        record_len = RECORD_SECONDS
        data_bytes = b''
        frames = []
        for i in range(0, int(RATE / CHUNK * record_len)):
            data = stream.read(CHUNK)
            frames.append(data)
            data_bytes += data
        frames2.extend(frames)
        frames3.extend(frames)


        stream.stop_stream()
        stream.close()
        p.terminate()
        # print(type(data_bytes))
        # sys.exit()
        if same_output_file:
            ext = ""
        else:
            ext = "./recordings_dump/" + str(counter)


        # Store the recorded frames in a variable
        recorded_frames = frames
        recorded_frames2 = frames2
        recorded_frames3 = frames3
        audio_data = b''.join(recorded_frames)
        audio_data2 = b''.join(recorded_frames2)
        audio_data3 = b''.join(recorded_frames3)

        # wf = wave.open(ext+wav_path, 'wb')
        # wf.setnchannels(CHANNELS)
        # wf.setsampwidth(p.get_sample_size(FORMAT))
        # wf.setframerate(RATE)
        # wf.writeframes(b''.join(frames))
        # wf.close()
        print("Done recording! - F")
        # print(len(frames))

    # if vad:
    #     pass

    if normalize:
        audio = AudioSegment(data=audio_data, sample_width=2, frame_rate=RATE, channels=CHANNELS)
        audio2 = AudioSegment(data=audio_data2, sample_width=2, frame_rate=RATE, channels=CHANNELS)
        audio3 = AudioSegment(data=audio_data3, sample_width=2, frame_rate=RATE, channels=CHANNELS)

        # Normalize the volume
        normalized_audio = audio.normalize()
        normalized_audio2 = audio2.normalize()
        normalized_audio3 = audio3.normalize()

        normalized_audios = [normalized_audio, normalized_audio2, normalized_audio3]

        # Change the sampling rate to 1
        # normalized_audio = normalized_audio.set_frame_rate(16000)

        # Combine all channels to one channel
        # normalized_audio = normalized_audio.set_channels(1)

        # Export the normalized audio as WAV file
        if dump_recordings:
            normalized_audio.export(ext+wav_path.split(".")[0]+"_normalized1.wav", format='wav')
            normalized_audio2.export(ext+wav_path.split(".")[0]+"_normalized2.wav", format='wav')
            normalized_audio3.export(ext+wav_path.split(".")[0]+"_normalized3.wav", format='wav')
            path = ext+wav_path.split(".")[0]+"_normalized.wav"


    if recognize:
        if load_models:
            #path where training speakers will be saved
            modelpath = "models/"

            gmm_files = [os.path.join(modelpath,fname) for fname in 
                        os.listdir(modelpath) if fname.endswith('.gmm')]

            #Load the Gaussian Models
            models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
            # print("Loaded Models: ", len(models))
            speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname
                        in gmm_files]
            load_models = False

        # path = wav_path.split(".")[0]+"_normalized.wav"
        # path = ext+wav_path
        # print("Testing Audio : ", path)
        time1 = time.time()
        selected_speakers = []
        selected_likelihoods = []
        max_speaker = -1
        max_speaker_name = ""
        index = -1
        for normalized_audio in normalized_audios:
            index += 1
            # audio_np = np.frombuffer(audio_data, dtype=np.int16)
            audio_np = np.array(normalized_audio.get_array_of_samples())
            
            # Get sample rate
            sr = RATE
            vector   = extract_features(audio_np,sr)
            log_likelihood = np.zeros(len(models))
            for i in range(len(models)):
                gmm    = models[i]  #checking with each model one by one
                scores = np.array(gmm.score(vector))
                log_likelihood[i] = scores.sum()
                # Apply softmax to the log likelihood values
            winner=np.argmax(log_likelihood)
            likelihood_values = np.exp(log_likelihood - np.max(log_likelihood)) 
            likelihood_values /= np.sum(likelihood_values)
            winner_score = log_likelihood[winner]
            predicted_speaker = speakers[winner]
            sample_time = time.time() - time1
            
            # Find the indices of the top three likelihood values
            top_indices = np.argsort(log_likelihood)[-3:][::-1]  # Indices of top three likelihoods in descending order
            top_likelihoods = np.exp(log_likelihood[top_indices] - np.max(log_likelihood))  # Compute likelihood values
            top_likelihoods /= np.sum(top_likelihoods)
            selected_speakers.append(speakers[top_indices[0]])
            selected_likelihoods.append(top_likelihoods[0])
            if top_likelihoods[0] > max_speaker:
                max_speaker = top_likelihoods[0]
                max_speaker_name = speakers[top_indices[0]]
            # if top_likelihoods[0] < max_speaker_threshold:
            #     speaker = speakers[0]
            #     likelihood = top_likelihoods[0]
            #     print(f"1. {speaker}: {likelihood}")
            #     print("skipped")
            #     continue
            # Print the top three speakers and their likelihood values
            # for rank, idx in enumerate(top_indices):
            #     speaker = speakers[idx]
            #     likelihood = top_likelihoods[rank]
            #     print(f"{rank+1}. {speaker}: {likelihood}")
            # print(f"{predicted_speaker}")
            # print("Time taken in ms: ", sample_time*1000)
        print(counter)
        if max_speaker >= 0.65:
            print("Speaker: ", max_speaker_name)
            last_speaker = max_speaker_name
            if max_speaker_name == last_speaker:
                weight += 1
        elif max_speaker >= 0.6 or (max_speaker_name == last_speaker and max_speaker >= 0.45 and weight > 3):
            print("1sec\t2sec\t3sec")
            print(selected_speakers)
            print(selected_likelihoods)
            last_speaker = max_speaker_name
            if max_speaker_name == last_speaker:
                weight += 1
            print("Max speaker: ", max_speaker_name)
        else:
            print("last speaker: ", last_speaker)
            print(max_speaker)
            weight = 0
            # last_speaker = selected_speakers[0]

    # time.sleep(1)
