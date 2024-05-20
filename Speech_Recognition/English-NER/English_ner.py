import nltk
import librosa
import torch
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer,AutoTokenizer, AutoModelForTokenClassification, pipeline, Wav2Vec2Processor
import mysql.connector
import time
nltk.download('punkt')


connection = mysql.connector.connect(
    user='root',password='root',host='embeddingsdb', database='db',port="3306")
print("Embeddings DB connected")

cursor = connection.cursor()
cursor.execute("SELECT first_name FROM embeddings WHERE voice IS NULL")
fnames = cursor.fetchall()
cursor.execute("SELECT last_name FROM embeddings WHERE voice IS NULL")
lnames = cursor.fetchall()
connection.close()

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

  for names in name_list:
    # Extract first and last names, handle single-element tuples consistently
    #first_name = names[0] if isinstance(names, tuple) and len(names) > 0 else ''.join(names)  # Convert single-element tuples to strings
    #last_name = names[1] if isinstance(names, tuple) and len(names) > 1 else None
    first_name,last_name = names
    new_first = str(first_name[0])
    new_last = str(last_name[0])
    # Convert names to strings before distance calculation (if not None)
    first_name = str(first_name) if first_name is not None else first_name
    last_name = str(last_name) if last_name is not None else last_name
    #print(new_first)
    #print(new_last)
    distance_first = levenshtein_distance(input_name, new_first)
    distance_last = levenshtein_distance(input_name, new_last) 

    # Check for closest distance considering both names
    min_distance = min(distance_first, distance_last)
    if min_distance < closest_distance:
      closest_distance = min_distance
      # Return only first name if last name is None
      closest_names = (new_first,new_last) 

  # Adjust the threshold factor based on your preference
  threshold_factor = 0.6
  if closest_distance > len(input_name) * threshold_factor:
    return None

  return closest_names
# Example usage:
#names = [('Omar','Fayed'), ('Abdelrahman','Said'), ('Youssef','Amr'), ('Reem','Ahmed'), ('Renad','Elkady'), ('Sherif','Sakran')]



def load_wav2vec_960h_model():
  """
  Returns the tokenizer and the model from pretrained tokenizers models
  """
  tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
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

# Record the start time
start_time = time.time()


# Record the end time

wav_input = 'test.wav'
tokenizer, model = load_wav2vec_960h_model()
text = asr_transcript(tokenizer,model,wav_input)
print(text)
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print("Elapsed time: {:.2f} seconds".format(elapsed_time))

start_time = time.time()

nertokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
nermodel = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
nlp = pipeline('ner', model=nermodel, tokenizer=nertokenizer, aggregation_strategy="simple")
n= nlp(text)
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print("Elapsed time: {:.2f} seconds".format(elapsed_time))

start_time = time.time()

qa_pipeline_roberta = pipeline("question-answering", model="consciousAI/question-answering-roberta-base-s-v2")


context = text
question = "What's my name?"
answer = qa_pipeline_roberta(question=question, context=context)

# Print answer
#print(f"Question: {question}")
#print(f"Answer: {answer['answer']}")


end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print("Elapsed time: {:.2f} seconds".format(elapsed_time))
for entity in n:
      #print (entity)
      #print ("next")
      if entity["entity_group"] == 'PER':
          name = entity["word"][1:]
          if name == answer['answer']:
            
            arrayofnames = []
            for i in range(len(fnames)):
                arrayofnames.append((fnames[i], lnames[i]))
                #print(arrayofnames)
            detected_name = find_closest_name(name,arrayofnames)
            print(detected_name)
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print("Elapsed time: {:.2f} seconds".format(elapsed_time))
        
