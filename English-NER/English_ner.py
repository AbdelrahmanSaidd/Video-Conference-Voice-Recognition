import nltk
import librosa
import torch
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer,AutoTokenizer, AutoModelForTokenClassification, pipeline
nltk.download('punkt')

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def find_closest_name(input_name, name_list):
    closest_distance = float('inf')
    closest_names = None
    
    for first_name, last_name in name_list:
        distance_first = levenshtein_distance(input_name, first_name)
        distance_last = levenshtein_distance(input_name, last_name)
        if distance_first < closest_distance or distance_last < closest_distance:
            closest_distance = min(distance_first, distance_last)
            closest_names = (first_name, last_name)
    
    # Adjust the threshold factor based on your preference
    threshold_factor = 0.8
    if closest_distance > len(input_name) * threshold_factor:
        return None
    
    return closest_names

# Example usage:
names = [('Omar','Fayed'), ('Abdelrahman','Said'), ('Youssef','Amr'), ('Reem','Ahmed'), ('Renad','Elkady'), ('Sherif','Sakran')]



def load_wav2vec_960h_model():
  """
  Returns the tokenizer and the model from pretrained tokenizers models
  """
  tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
  model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
  return tokenizer, model

def correct_uppercase_sentence(input_text):
  """
  Returns the corrected sentence
  """
  sentences = nltk.sent_tokenize(input_text)
  return (' '.join([s.replace(s[0],s[0].capitalize(),1) for s in sentences]))

def asr_transcript(tokenizer, model, input_file):
  """
  Returns the transcript of the input audio recording

  Output: Transcribed text
  Input: Huggingface tokenizer, model and wav file
  """
  #read the file
  speech, samplerate = sf.read(input_file)
  #make it 1-D
  if len(speech.shape) > 1:
      speech = speech[:,0] + speech[:,1]
  #Resample to 16khz
  if samplerate != 16000:
      speech = librosa.resample(speech, samplerate, 16000)
  #tokenize
  input_values = tokenizer(speech, return_tensors="pt").input_values
  #take logits
  logits = model(input_values).logits
  #take argmax (find most probable word id)
  predicted_ids = torch.argmax(logits, dim=-1)
  #get the words from the predicted word ids
  transcription = tokenizer.decode(predicted_ids[0])
  #output is all uppercase, make only the first letter in first word capitalized
  transcription = correct_uppercase_sentence(transcription.lower())
  return transcription

wav_input = 'sample.wav'
tokenizer, model = load_wav2vec_960h_model()
text = asr_transcript(tokenizer,model,wav_input)
print(text)


nertokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
nermodel = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")


nlp = pipeline('ner', model=nermodel, tokenizer=nertokenizer, aggregation_strategy="simple")
print(nlp(text))
