# Arabic Automatic Speech Recognition and Named Entity Recognition System.

The system Recognises Arabic Speech and uses the recognised speech to detect Named entities:  
## Running the code
First install the required libraries

```
python3 -m venv venv

```

```
source venv/bin/activate

```

```
pip install -r requirements.txt

```
Run the tagger.py file for ASR
```
python tagger.py

```


## Training Corpus

The training corpus is made of 378.000 tokens (14.000 sentences) collected from the Web and annotated manually.

## Results

The results on a valid corpus made of 30.000 tokens shows an F-measure of ~87%.
