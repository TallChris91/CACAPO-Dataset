import zipfile
import random
import regex as re
import json
import os
import jsonlines
import pickle

def clean_text(text):
    #performs a few cleaning steps to remove non-alphabetic characters

    #replace new line and carriage return with space
    text = text.replace("\n", " ").replace("\r", " ")
    #replace the numbers and punctuation (exclude single quote) with space
    punc_list = '!"#$%&()**+,-./:;<=>?@[\]^_{|}~' + '0123456789'
    t = str.maketrans(dict.fromkeys(punc_list, " "))
    text = text.translate(t)

    #replace single quote with empty character
    t = str.maketrans(dict.fromkeys("'`", ""))
    text = text.translate(t)

    return text

def word_tokenize(text):
    #Make a list of all the existing words
    WORD = re.compile(r'\w+')
    #Clean all punctuation, etc.
    text = clean_text(text)
    #And find all words
    words = WORD.findall(text)
    return words

filelist = []
filelistjson = []

currentpath = os.getcwd() + '/Data/'
corpuspath = os.getcwd() + '/Corpus/'

with zipfile.ZipFile(corpuspath + 'html-output-cleaned.zip') as z:
    for filename in z.namelist():
        newjson = {'meta': {}}
        with z.open(filename) as f:
            lines = f.readlines()
            fixedlines = [x.decode("utf-8") for x in lines]

        if fixedlines[-1].startswith('Game notes'):
            fixedlines = fixedlines[:-1]
            fixedlines = ''.join(fixedlines)
        else:
            fixedlines = ''.join(fixedlines)

        newjson['meta'].update({'byline': ''})
        date = re.search(r'^(.*?)\_(\d+)\_', filename).group(2)
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        newjson['meta'].update({'date': day + '-' + month + '-' + year})
        newjson['meta'].update({'edition': ''})
        newjson['meta'].update({'filename': filename})
        newjson['meta'].update({'language': 'DUTCH; NEDERLANDS'})

        textlength = len(word_tokenize(fixedlines))
        newjson['meta'].update({'length': str(textlength) + ' words'})
        newjson['meta'].update({'load-date': day + '-' + month + '-' + year})
        newjson['meta'].update({'newspaper': 'ESPN'})
        newjson['meta'].update({'publication-type': 'Web Publicatie'})
        newjson['meta'].update({'section': ''})
        newjson['meta'].update({"subject": "Sports(100%)"})
        title = re.search(r'^(.*?)\_(\d+)\_(.*?).txt$', filename).group(3)
        title = re.sub(r'\_', ' ', title)
        newjson['meta'].update({'title': title})
        newjson.update({'text': fixedlines})
        filelistjson.append(newjson)

with jsonlines.open(os.getcwd() + '/Data/SportsJson.jsonl', mode='w') as writer:
    writer.write_all(filelistjson)