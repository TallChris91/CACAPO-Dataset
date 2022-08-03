import os
import pickle

with open(os.getcwd() + '/Data/Relevantinfo.pkl', 'rb') as f:
    labels = pickle.load(f)

keystring = ','.join(list(labels.keys()))

#Create a Virtual Environment with prodigy and spacy (and the relevant models) beforehand
os.system(os.getcwd() + '/venv/Scripts/activate')
os.system('cd ' + os.getcwd())
os.system('python -m prodigy ner.correct EnglishWeather en_core_web_md' + os.getcwd() + '/Data/FullSample.jsonl --label ' + labelliststring + ' --unsegmented')

#os.system('python -m prodigy db-out EnglishWeather > ' + os.getcwd() + '/Data/EnglishWeatherAll.jsonl')
