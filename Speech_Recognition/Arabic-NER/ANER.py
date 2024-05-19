import sys

# Add the directory containing your module to the Python path
sys.path.append('klaam')

# Now you can import your module
import klaam
from klaam import SpeechRecognition
import nltk
nltk.download('punkt')  # Download the required tokenizer data
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer
from transformers import pipeline
#from helpers import split_sentences
import time


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
names = [('عمر ','فايد'), ('يوسف','عمرو'), ('شريف','سكران'), ('ريناد','القادي'), ('عبدالرحمن','سعيد'), ('ريم','سعيد')]

asrmodel = SpeechRecognition()
text=asrmodel.transcribe('demo.wav') #Replace demo.wav with the desired input wav file
# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("hatmimoha/arabic-ner")
model = AutoModelForTokenClassification.from_pretrained("hatmimoha/arabic-ner")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# Tag the text
start_time = time.time()
sentences = nltk.sent_tokenize(text)

annotations = nlp(sentences)
# -*- coding: utf-8 -*-
entities = []
tags = []
arabic= text.encode("utf-8")
print(arabic.decode("utf-8"))
for sentence in annotations:
  for item in sentence:
    if item["word"].startswith("##"):
      entities[-1] = entities[-1] + item["word"].replace("##", "")
    else:
      entities.append(item["word"])
      tags.append(item["entity"])

for item, label in zip(entities, tags):
  print(item + "\t" + label)
  if label == 'B-PERSON':
      n = find_closest_name(item,names)
      print (n)
