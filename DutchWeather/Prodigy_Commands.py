import os
import pickle

labellist = ['cloudAmount', 'cloudChange', 'cloudType', 'compassDirection', 'gustAmount', 'gustChange', 'gustVelocity', 'locationArea', 'maximumTemperature', 'minimumTemperature', 'precipitationAmount', 'snowAmount', 'temperatureCelsius', 'temperatureChange', 'temperatureHotCold', 'timePoint', 'weatherArea', 'weatherChange', 'weatherFrequency', 'weatherIntensity', 'weatherOccurringChance', 'weatherType', 'windAmount', 'windChange', 'windDirection', 'windSpeedBft', 'windTurning', 'windType']
newlabellist = sorted(labellist)
#print(newlabellist)
#exit(0)
labelliststring = ','.join(newlabellist)

os.system('C:/Users/chris/venv/Scripts/activate')
os.system('cd C:/Users/chris/Desktop')
#os.system('python -m prodigy ner.correct DutchWeatherDev nl_core_news_md C:/Users/chris/Desktop/Dev/FullDev.jsonl --label ' + labelliststring + ' --unsegmented')

os.system('python -m prodigy db-out DutchWeatherDev > C:/Users/chris/Desktop/DutchWeatherDev.jsonl')
