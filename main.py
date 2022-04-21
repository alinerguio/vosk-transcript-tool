import os
import sys
import wave
import json
import datetime
import pandas as pd
from vosk import Model, KaldiRecognizer


def log_time_specifics(start_time, end_time, dataset, quantity_files):
    process_time = end_time - start_time

    if os.path.isfile('execution_time_specifics.txt'):
        f = open('execution_time_specifics.txt', 'a')
    else:
        f = open('execution_time_specifics.txt', 'w')
        
    f.write('\n' + dataset + ';' +  str(quantity_files) + ';' + str(process_time))
    f.close()


def iterate_folder(rec, main_dir):
    all_folders = [folder for folder in os.listdir(main_dir) if '.' not in folder]
    
    for folder in all_folders:
        start_time = datetime.datetime.now()
        quantity_files = 0 
        
        curr_dir = main_dir + '/' + folder
        transc_folder = []

        all_files = [file for file in os.listdir(curr_dir) if '.wav' in file]

        if not(os.path.isdir('./transcriptions/')):
            os.mkdir('./transcriptions/')

        output_path = './transcriptions/' + folder + '.csv'

        if os.path.isfile(output_path):
            files_transcripted = pd.read_csv(output_path)
            files_transcripted_list = files_transcripted.file.tolist()
            all_files = [file for file in all_files if file not in files_transcripted_list]

        for file in all_files:

            try:
                resp = transcribe(rec, curr_dir + '/' + file)

                for r in resp:
                    result = None if 'result' not in r.keys() else r['result']
                    text = None if 'text' not in r.keys() else r['text']
                    confidence = None if 'confidence' not in r.keys() else r['confidence']

                    final_result = pd.DataFrame([{'transcription': text, 'confidence': confidence, 'result': result, 'file': file, 'database': folder}])
                    final_result.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
            
            except Exception as e:
                print('Not possible to proceed transcribing file: ' + file)
                print(e)

            except KeyboardInterrupt:
                print('\nKeyboardInterrupt: stopping manually')
                end_time = datetime.datetime.now()
                log_time_specifics(start_time, end_time, folder, quantity_files)

                sys.exit()

        end_time = datetime.datetime.now()
        log_time_specifics(start_time, end_time, folder, quantity_files)

def transcribe(rec, file):
    wf = wave.open(file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit(1)

    result = {}

    while True:
        data = wf.readframes(4000)

        if len(data) == 0:
            break
        
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())

    if result != dict():
        return result['alternatives']
    else: 
        return [{'confidence': 0, 'result': '[]', 'text': 'Sem transcricao disponivel.'}]


def log_time(start_time, end_time):
    process_time = end_time - start_time

    if os.path.isfile('execution_time.txt'):
        f = open('execution_time.txt', 'a')
        f.write('\n' + str(process_time))
        f.close()
    else:
        f = open('execution_time.txt', 'w')
        f.write(str(process_time))
        f.close()


def get_vosk_model():
    if not os.path.exists("model"):
        print ("Modelo em portugues nao encontrado.")
        exit (1)

    model = Model("model")
    rec = KaldiRecognizer(model, 16000)
    rec.SetMaxAlternatives(10)
    rec.SetWords(True)

    return rec


if __name__ == '__main__':
    main_dir = '../data/'
    rec = get_vosk_model()
    start_time = datetime.datetime.now()

    try:
        iterate_folder(rec, main_dir)
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
    except Exception as e:
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
        print(e)