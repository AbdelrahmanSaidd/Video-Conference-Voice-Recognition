import nltk
import librosa
import torch
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer,AutoTokenizer, AutoModelForTokenClassification, pipeline
nltk.download('punkt')


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