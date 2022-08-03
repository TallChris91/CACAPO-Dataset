import pickle
import regex as re
import jsonlines
import os

def findParagraphs(filename, paragraphidx, occurrence, textidx, datasetidx, paragraph, sentence, currentpath):
    fulltext = ''

    with jsonlines.open(currentpath + '/Data/DutchWeatherAll.jsonl') as f:
        for textidx, text in enumerate(f):
            filenamejson = text['meta']['filename']
            if filenamejson == filename:
                fulltext = text['text']
                break

    paragraphs = re.split(r'[\n\r]+', fulltext)
    paragraphs = [re.sub(r'^\s+', '', x) for x in paragraphs]
    paragraphs = [re.sub(r'\s+$', '', x) for x in paragraphs]

    startidx = re.search(re.escape(paragraphs[paragraphidx]), fulltext).start()

    paragraphstartidx = occurrence[1] - startidx
    paragraphendidx = occurrence[2] - startidx

    if fulltext[occurrence[1]:occurrence[2]] != paragraphs[paragraphidx][paragraphstartidx:paragraphendidx]:
        parastartidxlist = re.finditer(re.escape(paragraphs[paragraphidx]), fulltext)
        matchfound = 'n'
        for parstartidx in parastartidxlist:
            newparstartidx = parstartidx.start()

            paragraphstartidx = occurrence[1] - newparstartidx
            paragraphendidx = occurrence[2] - newparstartidx

            if fulltext[occurrence[1]:occurrence[2]] == paragraphs[paragraphidx][paragraphstartidx:paragraphendidx]:
                startidx = newparstartidx
                matchfound = 'y'
                break

        if matchfound == 'n':
            print('Paragraph Error')
            print(fulltext[occurrence[1]:occurrence[2]])
            print(paragraphs[paragraphidx][paragraphstartidx:paragraphendidx])
            print('Datasetidx: ' + str(datasetidx))
            print('Textidx: ' + str(textidx))
            print('Paragraphidx: ' + str(paragraphidx))
            print(occurrence)
            print(paragraphs[paragraphidx])
            print(startidx)
            print(paragraph)
            print(fulltext)
            exit(0)

    sentencestartidxsentences = re.search(re.escape(sentence['sentence']), paragraphs[paragraphidx]).start()

    sentencestartidx = occurrence[1] - startidx - sentencestartidxsentences
    sentenceendidx = occurrence[2] - startidx - sentencestartidxsentences

    if fulltext[occurrence[1]:occurrence[2]] != sentence['sentence'][sentencestartidx:sentenceendidx]:
        sentstartidxlist = re.finditer(re.escape(sentence['sentence']), paragraphs[paragraphidx])
        matchfound = 'n'
        for sentstartidx in sentstartidxlist:
            newsentstartidx = sentstartidx.start()

            sentencestartidx = occurrence[1] - startidx - newsentstartidx
            sentenceendidx = occurrence[2] - startidx - newsentstartidx

            if fulltext[occurrence[1]:occurrence[2]] == sentence['sentence'][sentencestartidx:sentenceendidx]:
                matchfound = 'y'
                break

        if matchfound == 'n':
            print('Sentence Error')
            print(fulltext[occurrence[1]:occurrence[2]])
            print(sentence['sentence'][sentencestartidx:sentenceendidx])
            print('Datasetidx: ' + str(datasetidx))
            print('Textidx: ' + str(textidx))
            print('Paragraphidx: ' + str(paragraphidx))
            print(occurrence)
            print(sentence['sentence'])
            print(startidx)
            print(paragraph)
            print(fulltext)
            exit(0)
    return paragraphstartidx, paragraphendidx, sentencestartidx, sentenceendidx
    #return paragraphstartidx, paragraphendidx

currentpath = os.getcwd()
with open(currentpath + '/Data/AlldatasetsNewSplit.pkl', 'rb') as f:
    alldatasets = pickle.load(f)

for datasetidx, dataset in enumerate(alldatasets):
    for textidx, text in enumerate(dataset):
        for paragraphidx, paragraph in enumerate(text):
            for sentenceidx, sentence in enumerate(paragraph):
                if 'paragraphidx' in sentence:
                    filename = sentence['filename']
                    for combineddictkey in sentence:
                        if (combineddictkey != 'sentenceidx') and (combineddictkey != 'filename') and (combineddictkey != 'sentence') and (combineddictkey != 'title') and (combineddictkey != 'textidx') and (combineddictkey != 'paragraphidx') and (combineddictkey != 'datasetidx'):
                            for occurrenceidx, occurrence in enumerate(sentence[combineddictkey]):
                                paragraphstartidx, paragraphendidx, sentencestartidx, sentenceendidx = findParagraphs(filename, paragraphidx, occurrence, textidx, datasetidx, paragraph, sentence, currentpath)
                                #paragraphstartidx, paragraphendidx = findParagraphs(filename, paragraphidx, occurrence, textidx, datasetidx, paragraph, sentence, currentpath)
                                alldatasets[datasetidx][textidx][paragraphidx][sentenceidx][combineddictkey][occurrenceidx].extend([paragraphstartidx, paragraphendidx, sentencestartidx, sentenceendidx])
                                #alldatasets[datasetidx][textidx][paragraphidx][sentenceidx][combineddictkey][occurrenceidx].extend([paragraphstartidx, paragraphendidx])

with open(currentpath + '/Data/AlldatasetsNewSplit2.pkl', 'wb') as f:
    pickle.dump(alldatasets, f)