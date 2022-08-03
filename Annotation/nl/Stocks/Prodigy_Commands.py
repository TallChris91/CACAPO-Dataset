import os
import pickle

labellist = ['locationName', 'exchangeName', 'timePoint', 'stockChange', 'stockChangePercentage', 'stockPoints', 'companyName', 'moneyAmount']
newlabellist = sorted(labellist)
labelliststring = ','.join(newlabellist)

os.system(os.getcwd() + '/venv/Scripts/activate')
os.system('cd ' + os.getcwd())
os.system('python -m prodigy ner.correct DutchStocks nl_core_news_md ' + os.getcwd() + '/Data/FullSample.jsonl --label ' + labelliststring + ' --unsegmented')

#os.system('python -m prodigy db-out DutchStocks > ' + os.getcwd() + '/Data/DutchStocksAll.jsonl')
