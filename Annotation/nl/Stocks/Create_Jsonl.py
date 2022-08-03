import zipfile
import random
import regex as re
import json
import os
import jsonlines

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
filelistsample = []
filelistsamplejson = []

currentpath = os.getcwd()

with zipfile.ZipFile(currentpath + '/Data/DutchStocksReports.zip') as z:
    for filename in z.namelist():
        if filename.endswith('.json'):
            filelist.append(filename)
            with z.open(filename) as f:
                lines = f.read()
                lines = json.loads(lines.decode("utf-8"))
                fixedlines = lines['text']
                textlength = len(word_tokenize(fixedlines))
                if textlength <= 325:
                    filelistsample.append(filename)
                    filelistsamplejson.append(lines)

for idx, jsonfile in enumerate(filelistsamplejson):
    newjson = {'meta': {}}
    for key in jsonfile:
        if key == 'text':
            newjson.update({'text': jsonfile[key]})
        else:
            newjson['meta'].update({key: jsonfile[key]})
    filelistsamplejson[idx] = newjson


#Take 200 random files
samplealllist = random.sample(filelistsamplejson, 200)

with jsonlines.open(currentpath + '/Data/FullSample.jsonl', mode='w') as writer:
    writer.write_all(filelistsamplejson)