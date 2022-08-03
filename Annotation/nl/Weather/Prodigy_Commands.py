import os
import pickle

labellist = ['cloudAmount', 'cloudChange', 'cloudType', 'compassDirection', 'gustAmount', 'gustChange', 'gustVelocity', 'locationArea', 'maximumTemperature', 'minimumTemperature', 'precipitationAmount', 'snowAmount', 'temperatureCelsius', 'temperatureChange', 'temperatureHotCold', 'timePoint', 'weatherArea', 'weatherChange', 'weatherFrequency', 'weatherIntensity', 'weatherOccurringChance', 'weatherType', 'windAmount', 'windChange', 'windDirection', 'windSpeedBft', 'windTurning', 'windType']
newlabellist = sorted(labellist)
labelliststring = ','.join(newlabellist)

#Create a Virtual Environment with prodigy and spacy (and the relevant models) beforehand
os.system(os.getcwd() + '/venv/Scripts/activate')
os.system('cd ' + os.getcwd())
os.system('python -m prodigy ner.correct DutchWeather nl_core_news_md ' + os.getcwd() + '/Data/WeatherJson.jsonl --label ' + labelliststring + ' --unsegmented')

#os.system('python -m prodigy db-out DutchWeather > ' + os.getcwd() + '/Data/DutchWeatherAll.jsonl')
