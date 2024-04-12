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


asrmodel = SpeechRecognition()
text=asrmodel.transcribe('demo.wav')
# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("hatmimoha/arabic-ner")
model = AutoModelForTokenClassification.from_pretrained("hatmimoha/arabic-ner")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# Tag the text
start_time = time.time()
sentences = nltk.sent_tokenize(text)

annotations = nlp(sentences)

entities = []
tags = []
for sentence in annotations:
  for item in sentence:
    if item["word"].startswith("##"):
      entities[-1] = entities[-1] + item["word"].replace("##", "")
    else:
      entities.append(item["word"])
      tags.append(item["entity"])

for item, label in zip(entities, tags):
  print(item + "\t" + label)
