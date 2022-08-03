import numpy as np
import pickle
import os
import json
import jsonlines
import regex as re
from pysbd.utils import PySBDFactory
import spacy
nlnlp = spacy.load("nl_core_news_lg")
nlnlp.add_pipe(PySBDFactory(nlnlp), first=True)
ennlp = spacy.load("en_core_web_lg")
ennlp.add_pipe(PySBDFactory(ennlp), first=True)
import itertools

currentpath = os.getcwd()

def Create_Labeldict():
    labellist = ['locationName', 'exchangeName', 'timePoint', 'stockChange', 'stockChangePercentage', 'stockPoints', 'companyName', 'moneyAmount']

    labeldict = {}

    for label in labellist:
        labeldict.update({label: label})

    with open(currentpath + '/Data/Relevantinfo.pkl', 'wb') as f:
        pickle.dump(labeldict, f)

def add_dataset_info(dataset, datasettype):
    if datasettype == 'train':
        datasetidx = 0
    elif datasettype == 'dev':
        datasetidx = 1
    else:
        datasetidx = 2

    for textidx, text in enumerate(dataset):
        for paragraphidx, paragraph in enumerate(text):
            for lineidx, line in enumerate(paragraph):
                dataset[textidx][paragraphidx][lineidx].update({'datasetidx': datasetidx})

    return dataset

def Convert_Prodigy(dataset, language):
    alltexts = []

    with jsonlines.open(dataset) as f:
        for textidx, text in enumerate(f):
            markedspans = text['spans']
            fulltext = text['text']
            filename = text['meta']['filename']
            title = text['meta']['title']

            paragraphs = re.split(r'[\n\r]+', fulltext)
            paragraphs = [re.sub(r'^\s+', '', x) for x in paragraphs]
            paragraphs = [re.sub(r'\s+$', '', x) for x in paragraphs]
            paragraphslines = []
            sentenceindices = []

            existingidx = -1

            for paragraph in paragraphs:
                flat_list_sentenceindices = [item for sublist in sentenceindices for item in sublist]
                paragraphsentenceindices = []
                if language == 'en':
                    doc = ennlp(paragraph)
                elif language == 'nl':
                    doc = nlnlp(paragraph)
                lines = [sent.string.strip() for sent in doc.sents]
                for line in lines:
                    allmatches = [(m.start(0), m.end(0)) for m in re.finditer(re.escape(line), fulltext)]
                    for match in allmatches:
                        if (match not in flat_list_sentenceindices) and (match not in paragraphsentenceindices) and (match[0] >= existingidx):
                            paragraphsentenceindices.append(match)
                            matchfound = 'y'
                            existingidx = match[1]
                            break
                    if matchfound == 'n':
                        print(allmatches)
                paragraphslines.append(lines)
                sentenceindices.append(paragraphsentenceindices)
            #print(paragraphslines)
            #print(sentenceindices)
            #print(markedspans)
            textlist = []
            for idx, paragraph in enumerate(paragraphslines):
                paragraphlist = []
                for idx2, line in enumerate(paragraph):
                    #print(line)
                    textdict = {'sentence': line, 'textidx': textidx, 'paragraphidx': idx, 'sentenceidx': idx2, 'filename': filename, 'title': title}
                    paragraphlist.append(textdict)
                textlist.append(paragraphlist)

            num = 0
            while num < len(markedspans):
                spanfound = 'n'
                for idx, paragraph in enumerate(sentenceindices):
                    for idx2, boundaries in enumerate(paragraph):
                        if (markedspans[num]['start'] >= boundaries[0]) and (markedspans[num]['start'] <= boundaries[1]) and (markedspans[num]['end'] >= boundaries[0])  and (markedspans[num]['end'] <= boundaries[1]):
                            spanfound = 'y'
                            for txtparidx, textparagraph in enumerate(textlist):
                                for txtlineidx, textline in enumerate(textparagraph):
                                    if (textline['paragraphidx'] == idx) and (textline['sentenceidx'] == idx2):
                                        if markedspans[num]['label'] not in textlist[txtparidx][txtlineidx]:
                                            textlist[txtparidx][txtlineidx].update({markedspans[num]['label']: [[text['text'][markedspans[num]['start']:markedspans[num]['end']], markedspans[num]['start'], markedspans[num]['end']]]})
                                        else:
                                            textlist[txtparidx][txtlineidx][markedspans[num]['label']].append([text['text'][markedspans[num]['start']:markedspans[num]['end']], markedspans[num]['start'], markedspans[num]['end']])
                if spanfound == 'n':
                    firstsentencepar = None
                    firstsentenceline = None
                    lastsentencepar = None
                    lastsentenceline = None
                    for sentenceidx, sentencepar in enumerate(sentenceindices):
                        for boundaryidx, boundar in enumerate(sentencepar):
                            if (markedspans[num]['start'] >= boundar[0]) and (markedspans[num]['start'] <= boundar[1]):
                                firstsentencepar = sentenceidx
                                firstsentenceline = boundaryidx
                            elif (markedspans[num]['end'] >= boundar[0]) and (markedspans[num]['end'] <= boundar[1]):
                                lastsentencepar = sentenceidx
                                lastsentenceline = boundaryidx

                    #print(firstsentencepar, firstsentenceline)
                    #print(lastsentencepar, lastsentenceline)
                    if firstsentencepar == lastsentencepar:
                        sentenceindices[firstsentencepar][firstsentenceline:lastsentenceline+1] = [(sentenceindices[firstsentencepar][firstsentenceline][0], sentenceindices[firstsentencepar][lastsentenceline][1])]
                        paragraphslines[firstsentencepar][firstsentenceline:lastsentenceline + 1] = [' '.join(paragraphslines[firstsentencepar][firstsentenceline:lastsentenceline + 1])]
                    else:
                        sentenceindices[firstsentencepar:lastsentencepar+1] = [list(itertools.chain.from_iterable(sentenceindices[firstsentencepar:lastsentencepar+1]))]
                        paragraphslines[firstsentencepar:lastsentencepar + 1] = [list(itertools.chain.from_iterable(paragraphslines[firstsentencepar:lastsentencepar+1]))]


                    #print(sentenceindices)
                    #print(paragraphslines)

                else:
                    num += 1

            alltexts.append(textlist)

    return alltexts

englishstocks = Convert_Prodigy(currentpath + '/Data/DutchStocksAll.jsonl', 'nl')

def GetFileNames(dataset):
    filenames = []

    with jsonlines.open(dataset) as f:
        for textidx, text in enumerate(f):
            filename = text['meta']['filename']
            filenames.append(filename)

    return filenames

englishstocksfilenames = GetFileNames(currentpath + '/Data/DutchStocksAll.jsonl')

alldatasets = [englishstocks]

filenames = [englishstocksfilenames]

datasetconcatenated = englishstocks
filenamesconcatenated = englishstocksfilenames

trainsample = np.random.choice(np.arange(len(datasetconcatenated)), int(round((len(datasetconcatenated) / 100) * 76.5, 0)), replace=False)
newrestsample = []
restsample = list(np.arange(len(datasetconcatenated)))
for i in restsample:
    if i not in trainsample:
        newrestsample.append(i)

devsample = np.random.choice(newrestsample, int(round((len(datasetconcatenated) / 100) * 8.5, 0)), replace=False)

testsample = []
for i in newrestsample:
    if i not in devsample:
        testsample.append(i)
testsample = np.array(testsample)

print(trainsample)
print(devsample)
print(testsample)
print(len(trainsample))
print(len(devsample))
print(len(testsample))

newdatalisttrain = np.array(datasetconcatenated)[trainsample]
newdatalistdev = np.array(datasetconcatenated)[devsample]
newdatalisttest = np.array(datasetconcatenated)[testsample]

newfilenamestrain = np.array(filenamesconcatenated)[trainsample]
newfilenamesdev = np.array(filenamesconcatenated)[devsample]
newfilenamestest = np.array(filenamesconcatenated)[testsample]

newdatalisttrain = add_dataset_info(newdatalisttrain.tolist(), 'train')
newdatalistdev = add_dataset_info(newdatalistdev.tolist(), 'dev')
newdatalisttest = add_dataset_info(newdatalisttest.tolist(), 'test')

newfilenamestrain = newfilenamestrain.tolist()
newfilenamesdev = newfilenamesdev.tolist()
newfilenamestest = newfilenamestest.tolist()

newdatasets = [newdatalisttrain, newdatalistdev, newdatalisttest]

newfilenames = [newfilenamestrain, newfilenamesdev, newfilenamestest]

with open(currentpath + '/Data/AlldatasetsNewSplit.pkl', 'wb') as f:
    pickle.dump(newdatasets, f)

with open(currentpath + '/Data/FilenamelistNewSplit.pkl', 'wb') as f:
    pickle.dump(newfilenames, f)

with open(currentpath + '/Data/Filenamelist.pkl', 'wb') as f:
    pickle.dump(filenames, f)

#Create_Labeldict()