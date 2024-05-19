# Automatic Speech Recognition and Named Entity Recognition System.

This System is available in both Arabic and English. The Engluish System is compatible with Docker and the Docker Compose for the whole program. To use it with Docker clone the English_NER.  
## English Code
The Models used:

It is developed using multiple models that are built like a pipeline to extract names from an input .wav file. For Speech Recognition or Speech-to-Text we used Wav2vec2 fine-tuned model from [Hugging Face](https://huggingface.co/facebook/wav2vec2-base-960h). For the Named-Entity Recognition we used [RoBerta](https://huggingface.co/Jean-Baptiste/roberta-large-ner-english?) based model. Finally, the context of the speech was then checked with fine tuned [BERT](https://huggingface.co/consciousAI/question-answering-roberta-base-s-v2) model.


## Arabic Code
The Models used:
It is developed using multiple models that are built like a pipeline to extract names from an input .wav file. For Speech Recognition or Speech-to-Text we also used Wav2vec2 fine-tuned  model which was trained using Arabic dataset that is available on a Github repo called [Klaam](https://github.com/ARBML/klaam). For the Named-Entity Recognition we used an [Arabic NER](https://github.com/hatmimoha/arabic-ner) available on Git..

