import os
import pickle

labellist = ['locationName', 'exchangeName', 'timePoint', 'stockChange', 'stockChangePercentage', 'stockPoints', 'companyName', 'moneyAmount']
newlabellist = sorted(labellist)
print(newlabellist)
exit(0)
labelliststring = ','.join(newlabellist)

os.system('C:/Users/chris/venv/Scripts/activate')
os.system('cd C:/Users/chris/Desktop')
#os.system('python -m prodigy ner.correct DutchStocksDev nl_core_news_md C:/Users/chris/Desktop/Dev/FullDev.jsonl --label ' + labelliststring + ' --unsegmented')

os.system('python -m prodigy db-out DutchStocksDev > C:/Users/chris/Desktop/DutchStocksDev.jsonl')
