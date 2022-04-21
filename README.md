# Vosk API usage for Portuguese

## Goal

The goal is to download and process audios to be able to transcript them using the vosk transcript tool. To use this script, you must have a folder named "model" with a [model](https://alphacephei.com/vosk/models) of your choosing. In this case, I used the [Portuguese/Brazilian Portuguese](https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip) available on the VOSK website.

## Requirements

To use this code, you'll need this requirements.   

[![Python Version](https://img.shields.io/badge/python-3.8.2-green)](https://www.python.org/downloads/release/python-382/)

When the repository is first cloned, use this commands:
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Execution
Then, every time you want to access, don't forget to activate you enviroment:
```
$ source env/bin/activate
```

## Pipeline

### Downloading and Processing Data

Check [this repository](https://github.com/alinerguio/processing-data) for more info on this matter.  

Also, after processing the data specified in the directory and adapted it, there was the need to process the data in order to change the extension of the file to wav. This simple process is in the **to_wav.py** file. 

### Transcription

The script implementation was very simple and direct, the use of the API only required to reference the model in the [code](https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py), then create a Kaldi recognizer using that model of language (setting specifications such as the maximum of alternatives of transcriptions for that specific audio), and, finally, read the frames of the audio. 

About the configurations of the kaldi recognizer, in this case, was used the maximum of ten alternatives of transcriptions and the words were mapped on the frames in each case of the transcriptions. For example, in an audio of the VoxForge database, there were two options of response, and, in each one the words were mapped in the seconds they started and finished - which can be seen in the table below. 

| Confidence | Word Mapping                                                                                                                                                                                       | Transcription              |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| 234.278381 | [{'end': 1.35, 'start': 0.93, 'word': 'aquela'},  {'end': 1.77, 'start': 1.35, 'word': 'mulher'},  {'end': 2.85, 'start': 2.1, 'word': 'portuguesa'}]                                              | aquela mulher portuguesa   |
| 232.921143	 | [{'end': 1.35, 'start': 0.93, 'word': 'aquela'},  {'end': 1.77, 'start': 1.35, 'word': 'mulher'},  {'end': 2.07, 'start': 1.98, 'word': 'é'},  {'end': 2.85, 'start': 2.07, 'word': 'portuguesa'}] | aquela mulher é portuguesa |


## Executing scripts

To execute the scripts, there is the need to set the environment - as stated in the "Requirements" session. After that, is also essential that the data is processed as described previously (Downloading and Processing Data). To execute the code, is only necessary to execute the python command and the script name, as ilustrated below:

```
$ python3 main.py
```
