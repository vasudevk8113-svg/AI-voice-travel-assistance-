# AI-voice-travel-assistance-

An intelligent voice-controlled travel assistant using local ML models and curated datasets.

## Features

-  Voice input with speech recognition
-  Voice output with text-to-speech
-  Local FLAN-T5 model (no API costs)
-  33 travel destinations with detailed information
-  Completely free and offline-capable

## Technologies Used

- Python
- Hugging Face Transformers (FLAN-T5)
- PyTorch
- Pandas
- SpeechRecognition
- pyttsx3

## Installation
```
pip install -r requirements.txt
python create_dataset.py
python travel_assistant.py
```

## How it is used 

Simply run the assistant and speak your questions:
- "Where should I travel for good food?"
- "When is the best time to visit Japan?"
- "Budget-friendly destinations in Asia"

## Dataset

This includes 33 global destinations with:
- Local cuisine recommendations
- Best visiting times
- Budget estimates
- Cultural highlights
- Activities and attractions
```
