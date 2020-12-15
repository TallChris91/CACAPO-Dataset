import os
import pickle

labellist = ['LOC', 'exchangeName', 'DATE', 'stockChange', 'PERCENT', 'stockPoints', 'ORG', 'MONEY', 'TICKER', 'ORDINAL']
newlabellist = sorted(labellist)
labelliststring = ','.join(newlabellist)

os.system('C:/Users/chris/venv/Scripts/activate')
os.system('cd C:/Users/chris/Desktop')
#os.system('python -m prodigy ner.correct EnglishStocksDev en_core_web_md C:/Users/chris/Desktop/Dev/FullDev.jsonl --label ' + labelliststring + ' --unsegmented')

os.system('python -m prodigy db-out EnglishStocksDev > C:/Users/chris/Desktop/EnglishStocksDev.jsonl')
