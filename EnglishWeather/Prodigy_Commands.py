import os
import pickle

with open('C:/Users/chris/Syncmap/Promotie/CACAPO Alignment/DutchWeather/Data/Relevantinfo.pkl', 'rb') as f:
    labels = pickle.load(f)

keystring = ','.join(list(labels.keys()))

os.system('C:/Users/chris/venv/Scripts/activate')
os.system('cd C:/Users/chris/Desktop')
#os.system('python -m prodigy ner.correct English_Weather_Dev en_core_web_md C:/Users/chris/Desktop/Dev/FullDev.jsonl --label ' + keystring + ',sunRiseTime,sunSetTime --unsegmented')

os.system('python -m prodigy db-out English_Weather_Dev > C:/Users/chris/Desktop/English_Weather_Dev.jsonl')
