import os
import pickle

labellist = ['LOC', 'exchangeName', 'DATE', 'stockChange', 'PERCENT', 'stockPoints', 'ORG', 'MONEY', 'TICKER', 'ORDINAL']
newlabellist = sorted(labellist)
labelliststring = ','.join(newlabellist)

#Create a Virtual Environment with prodigy and spacy (and the relevant models) beforehand
os.system(os.getcwd() + '/venv/Scripts/activate')
os.system('cd ' + os.getcwd())
os.system('python -m prodigy ner.correct EnglishStocks en_core_web_md ' + os.getcwd() + '/Data/FullSample.jsonl --label ' + labelliststring + ' --unsegmented')

#os.system('python -m prodigy db-out EnglishStocks > ' + os.getcwd() + '/Data/EnglishStocksAll.jsonl')
