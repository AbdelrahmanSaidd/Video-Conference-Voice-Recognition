# English Automatic Speech Recognition and Named Entity Recognition System.

The system Recognises English Speech and uses the recognised speech to detect Named entities:  
## Running the code

## To run the Code locally without Docker
First install the required libraries

```
python3 -m venv venv

```
When installing in linux environment
```
source venv/bin/activate

```
When installing in Windows environment
```
./venv/scripts activate

```
Install required modules
```
pip install -r requirements.txt

```
Run the English-NER file for ASR
```
python English_ner.py

```

## To run the Code using Docker

Build Image using Comman below

```
docker build -t image_name

```
Run the image
```
docker run image_name

```
