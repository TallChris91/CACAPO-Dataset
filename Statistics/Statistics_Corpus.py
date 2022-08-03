import pickle
import jsonlines
#from pysbd.utils import PySBDFactory
import spacy
nlp = spacy.load("nl_core_news_lg")
import regex as re
import itertools
import pysbd

@nlp.component("sbd")
def pysbd_sentence_boundaries(doc):
    seg = pysbd.Segmenter(language="nl", clean=False, char_span=True)
    sents_char_spans = seg.segment(doc.text)
    char_spans = [doc.char_span(sent_span.start, sent_span.end, alignment_mode="contract") for sent_span in sents_char_spans]
    start_token_ids = [span[0].idx for span in char_spans if span is not None]
    for token in doc:
        token.is_sent_start = True if token.idx in start_token_ids else False
    return doc

nlp.add_pipe("sbd", first=True)


def MyToolAmount(datasetpath, multipledomains='y'):
    with open(datasetpath, 'rb') as f:
        domaindata = pickle.load(f)

    instancenumber = 0

    if multipledomains == 'y':
        for dataset in domaindata:
            for text in dataset:
                for paragraph in text:
                    instancenumber += len(paragraph)
    else:
        for text in domaindata:
            for paragraph in text:
                instancenumber += len(paragraph)

    return instancenumber

def MyToolUniqueMRs(datasetpath, multipledomains='y', removenumbers='n', return_len='y'):
    with open(datasetpath, 'rb') as f:
        domaindata = pickle.load(f)

    mrlist = []
    filterlist = ['sentenceidx', 'filename', 'sentence', 'title']
    if multipledomains == 'y':
        for dataset in domaindata:
            for text in dataset:
                for paragraph in text:
                    for sentencedict in paragraph:
                        newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}

                        if removenumbers == 'n':
                            mrlist.append(newsentencedict)
                        else:
                            newsentencedictcopy = {}
                            for oldkey in newsentencedict.keys():
                                newkey = re.sub(r'\d+', '', oldkey)
                                if newkey not in newsentencedictcopy:
                                    newsentencedictcopy.update({newkey: newsentencedict[oldkey]})
                                else:
                                    newsentencedictcopy[newkey] = newsentencedictcopy[newkey] + ';; ' + newsentencedict[oldkey]
                            mrlist.append(newsentencedictcopy)
    else:
        for text in domaindata:
            for paragraph in text:
                for sentencedict in paragraph:
                    newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}
                    mrlist.append(newsentencedict)

    newmrlist = [i for n, i in enumerate(mrlist) if i not in mrlist[n + 1:]]
    if return_len == 'y':
        return len(newmrlist)
    else:
        return newmrlist

def MyToolRefsPerMR(datasetpath, multipledomains='y', removenumbers='n'):
    with open(datasetpath, 'rb') as f:
        domaindata = pickle.load(f)

    mrlist = []
    filterlist = ['sentenceidx', 'filename', 'sentence', 'title']
    if multipledomains == 'y':
        for dataset in domaindata:
            for text in dataset:
                for paragraph in text:
                    for sentencedict in paragraph:
                        newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}

                        if removenumbers == 'n':
                            reffound = 'n'
                            for idx, mrdict in enumerate(mrlist):
                                if mrdict['dict'] == newsentencedict:
                                    mrlist[idx]['reflist'].append(sentencedict['sentence'])
                                    reffound = 'y'
                            if reffound == 'n':
                                mrlist.append({'dict': newsentencedict, 'reflist': [sentencedict['sentence']]})

                        if removenumbers == 'y':
                            newsentencedictcopy = {}
                            for oldkey in newsentencedict.keys():
                                newkey = re.sub(r'\d+', '', oldkey)
                                if newkey not in newsentencedictcopy:
                                    newsentencedictcopy.update({newkey: newsentencedict[oldkey]})
                                else:
                                    newsentencedictcopy[newkey] = newsentencedictcopy[newkey] + ';; ' + newsentencedict[oldkey]

                            reffound = 'n'
                            for idx, mrdict in enumerate(mrlist):
                                if mrdict['dict'] == newsentencedictcopy:
                                    mrlist[idx]['reflist'].append(sentencedict['sentence'])
                                    reffound = 'y'
                            if reffound == 'n':
                                mrlist.append({'dict': newsentencedictcopy, 'reflist': [sentencedict['sentence']]})
    else:
        for text in domaindata:
            for paragraph in text:
                for sentencedict in paragraph:
                    newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}

                    if removenumbers == 'n':
                        reffound = 'n'
                        for idx, mrdict in enumerate(mrlist):
                            if mrdict['dict'] == newsentencedict:
                                mrlist[idx]['reflist'].append(sentencedict['sentence'])
                                reffound = 'y'
                        if reffound == 'n':
                            mrlist.append({'dict': newsentencedict, 'reflist': [sentencedict['sentence']]})

                    if removenumbers == 'y':
                        newsentencedictcopy = {}
                        for oldkey in newsentencedict.keys():
                            newkey = re.sub(r'\d+', '', oldkey)
                            if newkey not in newsentencedictcopy:
                                newsentencedictcopy.update({newkey: newsentencedict[oldkey]})
                            else:
                                newsentencedictcopy[newkey] = newsentencedictcopy[newkey] + ';; ' + newsentencedict[oldkey]

                        reffound = 'n'
                        for idx, mrdict in enumerate(mrlist):
                            if mrdict['dict'] == newsentencedictcopy:
                                mrlist[idx]['reflist'].append(sentencedict['sentence'])
                                reffound = 'y'
                        if reffound == 'n':
                            mrlist.append({'dict': newsentencedictcopy, 'reflist': [sentencedict['sentence']]})

    totalrefs = 0
    maxrefs = 0
    minrefs = None
    for ref in mrlist:
        totalrefs += len(ref['reflist'])
        if len(ref['reflist']) > maxrefs:
            maxrefs = len(ref['reflist'])
        if minrefs == None:
            minrefs = len(ref['reflist'])
        elif len(ref['reflist']) < minrefs:
            minrefs = len(ref['reflist'])

    #refspermr = totalrefs / len(mrlist)
    return totalrefs, len(mrlist), minrefs, maxrefs

def MyToolSlotsPerMR(datasetpath, multipledomains='y', removenumbers='n'):
    with open(datasetpath, 'rb') as f:
        domaindata = pickle.load(f)

    mrlist = []
    filterlist = ['sentenceidx', 'filename', 'sentence', 'title']
    if multipledomains == 'y':
        for dataset in domaindata:
            for text in dataset:
                for paragraph in text:
                    for sentencedict in paragraph:
                        newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}

                        if removenumbers == 'n':
                            mrlist.append(newsentencedict)

                        if removenumbers == 'y':
                            newsentencedictcopy = {}
                            for oldkey in newsentencedict.keys():
                                newkey = re.sub(r'\d+', '', oldkey)
                                if newkey not in newsentencedictcopy:
                                    newsentencedictcopy.update({newkey: newsentencedict[oldkey]})
                                else:
                                    newsentencedictcopy[newkey] = newsentencedictcopy[newkey] + ';; ' + newsentencedict[oldkey]

                            mrlist.append(newsentencedictcopy)
    else:
        for text in domaindata:
            for paragraph in text:
                for sentencedict in paragraph:
                    newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}

                    if removenumbers == 'n':
                        mrlist.append(newsentencedict)

                    if removenumbers == 'y':
                        newsentencedictcopy = {}
                        for oldkey in newsentencedict.keys():
                            newkey = re.sub(r'\d+', '', oldkey)
                            if newkey not in newsentencedictcopy:
                                newsentencedictcopy.update({newkey: newsentencedict[oldkey]})
                            else:
                                newsentencedictcopy[newkey] = newsentencedictcopy[newkey] + ';; ' + newsentencedict[oldkey]

                        mrlist.append(newsentencedictcopy)

    totalslots = 0
    for mr in mrlist:
        totalslots += len(mr)

    return totalslots, len(mrlist)

def wordtokenizer(message, nlp):
    nldoc = nlp(message)
    # Return the lowercase token if the token is not actually punctuation
    tokenlist = [token.text.lower() for token in nldoc if re.search(r"^\p{P}+$", token.text) == None]
    return tokenlist

def MyToolWordsPerRef(datasetpath, multipledomains='y'):
    with open(datasetpath, 'rb') as f:
        domaindata = pickle.load(f)

    mrlist = []
    if multipledomains == 'y':
        for dataset in domaindata:
            for text in dataset:
                for paragraph in text:
                    for sentencedict in paragraph:
                        mrlist.append(sentencedict['sentence'])

    else:
        for text in domaindata:
            for paragraph in text:
                for sentencedict in paragraph:
                    mrlist.append(sentencedict['sentence'])

    for idx, val in enumerate(mrlist):
        mrlist[idx] = wordtokenizer(val, nlp)

    sentencelengthlist = [len(x) for x in mrlist]
    return sentencelengthlist

def ProdigyAmount(domaindata):
    instancenumber = 0

    for text in domaindata:
        for paragraph in text:
            instancenumber += len(paragraph)
    return instancenumber

def ProdigyUniqueMRs(domaindata):
    mrlist = []
    filterlist = ['text', 'textidx', 'paragraphidx', 'lineidx']
    for text in domaindata:
        for paragraph in text:
            for sentencedict in paragraph:
                newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}
                mrlist.append(newsentencedict)

    newmrlist = [i for n, i in enumerate(mrlist) if i not in mrlist[n + 1:]]
    return newmrlist

def ProdigyRefsPerMR(domaindata):
    mrlist = []
    filterlist = ['text', 'textidx', 'paragraphidx', 'lineidx']
    for text in domaindata:
        for paragraph in text:
            for sentencedict in paragraph:
                newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}
                reffound = 'n'
                for idx, mrdict in enumerate(mrlist):
                    if mrdict['dict'] == newsentencedict:
                        mrlist[idx]['reflist'].append(sentencedict['text'])
                        reffound = 'y'
                if reffound == 'n':
                    mrlist.append({'dict': newsentencedict, 'reflist': [sentencedict['text']]})

    totalrefs = 0
    maxrefs = 0
    minrefs = None
    for ref in mrlist:
        totalrefs += len(ref['reflist'])
        if len(ref['reflist']) > maxrefs:
            maxrefs = len(ref['reflist'])
        if minrefs == None:
            minrefs = len(ref['reflist'])
        elif len(ref['reflist']) < minrefs:
            minrefs = len(ref['reflist'])

    #refspermr = totalrefs / len(mrlist)
    return totalrefs, len(mrlist), minrefs, maxrefs

def ProdigySlotsPerMR(domaindata):
    mrlist = []
    filterlist = ['text', 'textidx', 'paragraphidx', 'lineidx']

    for text in domaindata:
        for paragraph in text:
            for sentencedict in paragraph:
                newsentencedict = {k: v for k, v in sentencedict.items() if k not in filterlist}
                mrlist.append(newsentencedict)

    totalslots = 0
    for mr in mrlist:
        totalslots += len(mr)

    return totalslots, len(mrlist)

def ProdigyWordsPerRef(domaindata):
    mrlist = []
    for text in domaindata:
        for paragraph in text:
            for sentencedict in paragraph:
                mrlist.append(sentencedict['text'])

    for idx, val in enumerate(mrlist):
        mrlist[idx] = wordtokenizer(val, nlp)

    sentencelengthlist = [len(x) for x in mrlist]
    return sentencelengthlist

def Convert_Prodigy(dataset):
    alltexts = []

    with jsonlines.open(dataset) as f:
        for textidx, text in enumerate(f):
            markedspans = text['spans']
            fulltext = text['text']

            paragraphs = re.split(r'[\n\r]+', fulltext)
            paragraphs = [re.sub(r'^\s+', '', x) for x in paragraphs]
            paragraphs = [re.sub(r'\s+$', '', x) for x in paragraphs]
            paragraphslines = []
            sentenceindices = []

            existingidx = -1

            for paragraph in paragraphs:
                flat_list_sentenceindices = [item for sublist in sentenceindices for item in sublist]
                paragraphsentenceindices = []
                doc = nlp(paragraph)
                lines = [sent.text.strip() for sent in doc.sents]
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
                    textdict = {'text': line, 'textidx': textidx, 'paragraphidx': idx, 'lineidx': idx2}
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
                                    if (textline['paragraphidx'] == idx) and (textline['lineidx'] == idx2):
                                        textlist[txtparidx][txtlineidx].update({markedspans[num]['label']: text['text'][markedspans[num]['start']:markedspans[num]['end']]})
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

currentpath = os.getcwd()

dutchaccidentsamount = MyToolAmount(currentpath + '/DutchAccidents/Data/Alldatasets.pkl')
dutchsportsamount = MyToolAmount(currentpath + '/DutchSports/Data/Alldatasets.pkl')
dutchweatheramount = MyToolAmount(currentpath + '/DutchWeather/Data/Alldatasets.pkl')
dutchweatherdev = Convert_Prodigy(currentpath + '/DutchWeather/Data/DutchWeatherDev.jsonl')
dutchweathertest = Convert_Prodigy(currentpath + '/DutchWeather/Data/DutchWeatherTest.jsonl')
dutchweatheramountdev = ProdigyAmount(dutchweatherdev)
dutchweatheramounttest = ProdigyAmount(dutchweathertest)
dutchstockstrain = Convert_Prodigy(currentpath + '/DutchStocks/Data/DutchStocksTrain.jsonl')
dutchstocksdev = Convert_Prodigy(currentpath + '/DutchStocks/Data/DutchStocksDev.jsonl')
dutchstockstest = Convert_Prodigy(currentpath + '/DutchStocks/Data/DutchStocksTest.jsonl')
dutchstocksamounttrain = ProdigyAmount(dutchstockstrain)
dutchstocksamountdev = ProdigyAmount(dutchstocksdev)
dutchstocksamounttest = ProdigyAmount(dutchstockstest)
print('Dutch number of instances: ' + str(dutchaccidentsamount + dutchsportsamount + dutchweatheramount + dutchweatheramountdev + dutchweatheramounttest + dutchstocksamounttrain + dutchstocksamountdev + dutchstocksamounttest))

englishaccidentsamount = MyToolAmount(currentpath + '/EnglishAccidents/Data/Alldatasets.pkl')
englishsportsamount = MyToolAmount(currentpath + '/EnglishSports/Data/Tempdataset.pkl', 'n')
englishsportstrain = Convert_Prodigy(currentpath + '/EnglishSports/Data/EnglishSportsTrain.jsonl')
englishsportsdev = Convert_Prodigy(currentpath + '/EnglishSports/Data/EnglishSportsDev.jsonl')
englishsportstest = Convert_Prodigy(currentpath + '/EnglishSports/Data/EnglishSportsTest.jsonl')
englishsportsamounttrain = ProdigyAmount(englishsportstrain)
englishsportsamountdev = ProdigyAmount(englishsportsdev)
englishsportsamounttest = ProdigyAmount(englishsportstest)
englishstockstrain = Convert_Prodigy(currentpath + '/EnglishStocks/Data/EnglishStocksTrain.jsonl')
englishstocksdev = Convert_Prodigy(currentpath + '/EnglishStocks/Data/EnglishStocksDev.jsonl')
englishstockstest = Convert_Prodigy(currentpath + '/EnglishStocks/Data/EnglishStocksTest.jsonl')
englishstocksamounttrain = ProdigyAmount(englishstockstrain)
englishstocksamountdev = ProdigyAmount(englishstocksdev)
englishstocksamounttest = ProdigyAmount(englishstockstest)
englishweathertrain = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather.jsonl')
englishweatherdev = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Dev.jsonl')
englishweathertest = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Test.jsonl')
englishweatheramountttrain = ProdigyAmount(englishweathertrain)
englishweatheramountdev = ProdigyAmount(englishweatherdev)
englishweatheramounttest = ProdigyAmount(englishweathertest)
print('English number of instances: ' + str(englishaccidentsamount + englishsportsamount + englishsportsamounttrain + englishsportsamountdev + englishsportsamounttest + englishstocksamounttrain + englishstocksamountdev + englishstocksamounttest + englishweatheramountttrain + englishweatheramountdev + englishweatheramounttest))

dutchaccidentsmr = MyToolUniqueMRs(currentpath + '/DutchAccidents/Data/Alldatasets.pkl', 'y', 'y')
dutchsportsmr = MyToolUniqueMRs(currentpath + '/DutchSports/Data/Alldatasets.pkl')
dutchweathermrtrain = MyToolUniqueMRs(currentpath + '/DutchWeather/Data/Alldatasets.pkl', 'y', 'n', 'n')
dutchweathermrdev = ProdigyUniqueMRs(dutchweatherdev)
dutchweathermrtest = ProdigyUniqueMRs(dutchweathertest)
dutchweathermrlist = dutchweathermrtrain + dutchweathermrdev + dutchweathermrtest
newdutchweathermrlist = [i for n, i in enumerate(dutchweathermrlist) if i not in dutchweathermrlist[n + 1:]]
#dutchstockstrain = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksTrain.jsonl')
dutchstocksmrtrain = ProdigyUniqueMRs(dutchstockstrain)
dutchstocksmrdev = ProdigyUniqueMRs(dutchstocksdev)
dutchstocksmrtest = ProdigyUniqueMRs(dutchstockstest)
dutchstocksmrlist = dutchstocksmrtrain + dutchstocksmrdev + dutchstocksmrtest
newdutchstocksmrlist = [i for n, i in enumerate(dutchstocksmrlist) if i not in dutchstocksmrlist[n + 1:]]
print('Dutch number of unique MRs: ' + str(dutchaccidentsmr + dutchsportsmr + len(newdutchweathermrlist) + len(newdutchstocksmrlist)))

englishaccidentsmr = MyToolUniqueMRs(currentpath + '/EnglishAccidents/Data/Alldatasets.pkl')
englishsportsmr = MyToolUniqueMRs(currentpath + '/EnglishSports/Data/Tempdataset.pkl', 'n', 'n', 'n')
englishsportsmrtrain = ProdigyUniqueMRs(englishstockstrain)
englishsportsmrdev = ProdigyUniqueMRs(englishstocksdev)
englishsportsmrtest = ProdigyUniqueMRs(englishstockstest)
englishsportsmrlist = englishsportsmr + englishsportsmrtrain + englishsportsmrdev + englishsportsmrtest
newenglishsportsmrlist = [i for n, i in enumerate(englishsportsmrlist) if i not in englishsportsmrlist[n + 1:]]
#englishstockstrain = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksTrain.jsonl')
englishstocksmrtrain = ProdigyUniqueMRs(englishstockstrain)
englishstocksmrdev = ProdigyUniqueMRs(englishstocksdev)
englishstocksmrtest = ProdigyUniqueMRs(englishstockstest)
englishstocksmrlist = englishstocksmrtrain + englishstocksmrdev + englishstocksmrtest
newenglishstocksmrlist = [i for n, i in enumerate(englishstocksmrlist) if i not in englishstocksmrlist[n + 1:]]
#englishweathertrain = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather.jsonl')
#englishweatherdev = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Dev.jsonl')
#englishweathertest = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Test.jsonl')
englishweathermrtrain = ProdigyUniqueMRs(englishweathertrain)
englishweathermrdev = ProdigyUniqueMRs(englishweatherdev)
englishweathermrtest = ProdigyUniqueMRs(englishweathertest)
englishweathermrlist = englishweathermrtrain + englishweathermrdev + englishweathermrtest
newenglishweathermrlist = [i for n, i in enumerate(englishweathermrlist) if i not in englishweathermrlist[n + 1:]]
print('English number of unique MRs: ' + str(englishaccidentsmr + len(newenglishsportsmrlist) + len(newenglishstocksmrlist) + len(newenglishweathermrlist)))

dutchaccidentstotalrefs, dutchaccidentsuniquerefs, dutchaccidentsminrefs, dutchaccidentsmaxrefs = MyToolRefsPerMR(currentpath + '/DutchAccidents/Data/Alldatasets.pkl', 'y', 'y')
dutchsporttotalrefs, dutchsportuniquerefs, dutchsportminrefs, dutchsportmaxrefs = MyToolRefsPerMR(currentpath + '/DutchSports/Data/Alldatasets.pkl')
dutchweathertotalrefs, dutchweatheruniquerefs, dutchweatherminrefs, dutchweathermaxrefs = MyToolRefsPerMR(currentpath + '/DutchWeather/Data/Alldatasets.pkl')
dutchweathertotalrefsdev, dutchweatheruniquerefsdev, dutchweatherminrefsdev, dutchweathermaxrefsdev = ProdigyRefsPerMR(dutchweatherdev)
dutchweathertotalrefstest, dutchweatheruniquerefstest, dutchweatherminrefstest, dutchweathermaxrefstest = ProdigyRefsPerMR(dutchweathertest)
#dutchstockstrain = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksTrain.jsonl')
dutchstockstotalrefstrain, dutchstocksuniquerefstrain, dutchstocksminrefstrain, dutchstocksmaxrefstrain = ProdigyRefsPerMR(dutchstockstrain)
dutchstockstotalrefsdev, dutchstocksuniquerefsdev, dutchstocksminrefsdev, dutchstocksmaxrefsdev = ProdigyRefsPerMR(dutchstocksdev)
dutchstockstotalrefstest, dutchstocksuniquerefstest, dutchstocksminrefstest, dutchstocksmaxrefstest = ProdigyRefsPerMR(dutchstockstest)
dutchsumtotalrefs = dutchaccidentstotalrefs + dutchsporttotalrefs + dutchweathertotalrefs + dutchweathertotalrefsdev + dutchweathertotalrefstest + dutchstockstotalrefstrain + dutchstockstotalrefsdev + dutchstockstotalrefstest
#dutchsumtotaluniquerefs = dutchaccidentsuniquerefs + dutchsportuniquerefs + dutchweatheruniquerefs + dutchweatheruniquerefsdev + dutchweatheruniquerefstest + dutchstocksuniquerefstrain + dutchstocksuniquerefsdev + dutchstocksuniquerefstest
dutchsumtotaluniquerefs = dutchaccidentsmr + dutchsportsmr + len(newdutchweathermrlist) + len(newdutchstocksmrlist)
print('Dutch refs per MR: ' + str(dutchsumtotalrefs / dutchsumtotaluniquerefs))
dutchminrefs = min([dutchaccidentsminrefs, dutchsportminrefs, dutchweatherminrefs, dutchweatherminrefsdev, dutchweatherminrefstest, dutchstocksminrefstrain, dutchstocksminrefsdev, dutchstocksminrefstest])
dutchmaxrefs = max([dutchaccidentsmaxrefs, dutchsportmaxrefs, dutchweathermaxrefs, dutchweathermaxrefsdev, dutchweathermaxrefstest, dutchstocksmaxrefstrain, dutchstocksmaxrefsdev, dutchstocksmaxrefstest])
print('Dutch minimum refs: ' + str(dutchminrefs))
print('Dutch maximum refs: ' + str(dutchmaxrefs))

englishaccidentstotalrefs, englishaccidentsuniquerefs, englishaccidentsminrefs, englishaccidentsmaxrefs = MyToolRefsPerMR(currentpath + '/EnglishAccidents/Data/Alldatasets.pkl')
englishsporttotalrefs, englishsportuniquerefs, englishsportminrefs, englishsportmaxrefs = MyToolRefsPerMR(currentpath + '/EnglishSports/Data/Tempdataset.pkl', 'n')
englishsportstotalrefstrain, englishsportsuniquerefstrain, englishsportsminrefstrain, englishsportsmaxrefstrain = ProdigyRefsPerMR(englishsportstrain)
englishsportstotalrefsdev, englishsportsuniquerefsdev, englishsportsminrefsdev, englishsportsmaxrefsdev = ProdigyRefsPerMR(englishsportsdev)
englishsportstotalrefstest, englishsportsuniquerefstest, englishsportsminrefstest, englishsportsmaxrefstest = ProdigyRefsPerMR(englishsportstest)
#englishstockstrain = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksTrain.jsonl')
englishstockstotalrefstrain, englishstocksuniquerefstrain, englishstocksminrefstrain, englishstocksmaxrefstrain = ProdigyRefsPerMR(englishstockstrain)
englishstockstotalrefsdev, englishstocksuniquerefsdev, englishstocksminrefsdev, englishstocksmaxrefsdev = ProdigyRefsPerMR(englishstocksdev)
englishstockstotalrefstest, englishstocksuniquerefstest, englishstocksminrefstest, englishstocksmaxrefstest = ProdigyRefsPerMR(englishstockstest)
#englishweathertrain = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather.jsonl')
#englishweatherdev = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Dev.jsonl')
#englishweathertest = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Test.jsonl')
englishweathertotalrefstrain, englishweatheruniquerefstrain, englishweatherminrefstrain, englishweathermaxrefstrain = ProdigyRefsPerMR(englishweathertrain)
englishweathertotalrefsdev, englishweatheruniquerefsdev, englishweatherminrefsdev, englishweathermaxrefsdev = ProdigyRefsPerMR(englishweatherdev)
englishweathertotalrefstest, englishweatheruniquerefstest, englishweatherminrefstest, englishweathermaxrefstest = ProdigyRefsPerMR(englishweathertest)
englishsumtotalrefs = englishaccidentstotalrefs + englishsporttotalrefs + englishsportstotalrefstrain + englishsportstotalrefsdev + englishsportstotalrefstest + englishstockstotalrefstrain + englishstockstotalrefsdev + englishstockstotalrefstest + englishweathertotalrefstrain + englishweathertotalrefsdev + englishweathertotalrefstest
#englishsumtotaluniquerefs = englishaccidentsuniquerefs + englishsportuniquerefs + englishsportsuniquerefstrain + englishsportsuniquerefsdev + englishsportsuniquerefstest + englishstocksuniquerefstrain + englishstocksuniquerefsdev + englishstocksuniquerefstest + englishweatheruniquerefstrain + englishweatheruniquerefsdev + englishweatheruniquerefstest
englishsumtotaluniquerefs = englishaccidentsmr + len(newenglishsportsmrlist) + len(newenglishstocksmrlist) + len(newenglishweathermrlist)
print('English refs per MR: ' + str(englishsumtotalrefs / englishsumtotaluniquerefs))
englishminrefs = min([englishaccidentsminrefs, englishsportminrefs, englishsportsminrefstrain, englishsportsminrefsdev, englishsportsminrefstest, englishstocksminrefstrain, englishstocksminrefsdev, englishstocksminrefstest, englishweatherminrefstrain, englishweatherminrefsdev, englishweatherminrefstest])
englishmaxrefs = max([englishaccidentsmaxrefs, englishsportmaxrefs, englishsportsmaxrefstrain, englishsportsmaxrefsdev, englishsportsmaxrefstest, englishstocksmaxrefstrain, englishstocksmaxrefsdev, englishstocksmaxrefstest, englishweathermaxrefstrain, englishweathermaxrefsdev, englishweathermaxrefstest])
print('English minimum refs: ' + str(englishminrefs))
print('English maximum refs: ' + str(englishmaxrefs))

dutchaccidentstotalslots, dutchaccidentstotalmrs = MyToolSlotsPerMR(currentpath + '/DutchAccidents/Data/Alldatasets.pkl', 'y', 'y')
dutchsporttotalslots, dutchsportstotalmrs = MyToolSlotsPerMR(currentpath + '/DutchSports/Data/Alldatasets.pkl')
dutchweathertotalslots, dutchweathertotalmrs = MyToolSlotsPerMR(currentpath + '/DutchWeather/Data/Alldatasets.pkl')
dutchweathertotalslotsdev, dutchweathertotalmrsdev = ProdigySlotsPerMR(dutchweatherdev)
dutchweathertotalslotstest, dutchweathertotalmrstest = ProdigySlotsPerMR(dutchweathertest)
#dutchstockstrain = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksTrain.jsonl')
dutchstockstotalslotstrain, dutchstockstotalmrstrain = ProdigySlotsPerMR(dutchstockstrain)
dutchstockstotalslotsdev, dutchstockstotalmrsdev = ProdigySlotsPerMR(dutchstocksdev)
dutchstockstotalslotstest, dutchstockstotalmrstest = ProdigySlotsPerMR(dutchstockstest)
dutchtotalslots = dutchaccidentstotalslots + dutchsporttotalslots + dutchweathertotalslots + dutchweathertotalslotsdev + dutchweathertotalslotstest + dutchstockstotalslotstrain + dutchstockstotalslotsdev + dutchstockstotalslotstest
dutchtotalmrs = dutchaccidentstotalmrs + dutchsportstotalmrs + dutchweathertotalmrs + dutchweathertotalmrsdev + dutchweathertotalmrstest + dutchstockstotalmrstrain + dutchstockstotalmrsdev + dutchstockstotalmrstest
print('Dutch slots per MR: ' + str(dutchtotalslots / dutchtotalmrs))

englishaccidentstotalslots, englishaccidentstotalmrs = MyToolSlotsPerMR(currentpath + '/EnglishAccidents/Data/Alldatasets.pkl', 'y', 'y')
englishsporttotalslots, englishsporttotalmrs = MyToolSlotsPerMR(currentpath + '/EnglishSports/Data/Tempdataset.pkl', 'n')
englishsportstotalslotstrain, englishsportstotalmrstrain = ProdigySlotsPerMR(englishsportstrain)
englishsportstotalslotsdev, englishsportstotalmrsdev = ProdigySlotsPerMR(englishsportsdev)
englishsportstotalslotstest, englishsportstotalmrstest = ProdigySlotsPerMR(englishsportstest)
#englishweathertrain = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather.jsonl')
#englishweatherdev = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Dev.jsonl')
#englishweathertest = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Test.jsonl')
englishweathertotalslotstrain, englishweathertotalmrstrain = ProdigySlotsPerMR(englishweathertrain)
englishweathertotalslotsdev, englishweathertotalmrsdev = ProdigySlotsPerMR(englishweatherdev)
englishweathertotalslotstest, englishweathertotalmrstest = ProdigySlotsPerMR(englishweathertest)
#englishstockstrain = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksTrain.jsonl')
englishstockstotalslotstrain, englishstockstotalmrstrain = ProdigySlotsPerMR(englishstockstrain)
englishstockstotalslotsdev, englishstockstotalmrsdev = ProdigySlotsPerMR(englishstocksdev)
englishstockstotalslotstest, englishstockstotalmrstest = ProdigySlotsPerMR(englishstockstest)
englishtotalslots = englishaccidentstotalslots + englishsporttotalslots + englishsportstotalslotstrain + englishsportstotalslotsdev + englishsportstotalslotstest + englishweathertotalslotstrain + englishweathertotalslotsdev + englishweathertotalslotstest + englishstockstotalslotstrain + englishstockstotalslotsdev + englishstockstotalslotstest
englishtotalmrs = englishaccidentstotalmrs + englishsporttotalmrs + englishsportstotalmrstrain + englishsportstotalmrsdev + englishsportstotalmrstest + englishweathertotalmrstrain + englishweathertotalmrsdev + englishweathertotalmrstest + englishstockstotalmrstrain + englishstockstotalmrsdev + englishstockstotalmrstest
print('English slots per MR: ' + str(englishtotalslots / englishtotalmrs))

dutchaccidentssentencelength = MyToolWordsPerRef(currentpath + '/DutchAccidents/Data/Alldatasets.pkl')
dutchsportssentencelength = MyToolWordsPerRef(currentpath + '/DutchSports/Data/Alldatasets.pkl')
dutchweathersentencelength = MyToolWordsPerRef(currentpath + '/DutchWeather/Data/Alldatasets.pkl')
dutchweathersentencelengthdev = ProdigyWordsPerRef(dutchweatherdev)
dutchweathersentencelengthtest = ProdigyWordsPerRef(dutchweathertest)
#dutchstockstrain = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksTrain.jsonl')
dutchstockssentencelengthtrain = ProdigyWordsPerRef(dutchstockstrain)
dutchstockssentencelengthdev = ProdigyWordsPerRef(dutchstocksdev)
dutchstockssentencelengthtest = ProdigyWordsPerRef(dutchstockstest)
dutchallsentencelengthlist = dutchsportssentencelength + dutchsportssentencelength + dutchweathersentencelength + dutchweathersentencelengthdev + dutchweathersentencelengthtest + dutchstockssentencelengthtrain + dutchstockssentencelengthdev + dutchstockssentencelengthtest
dutchtotalsentencelength = sum(dutchallsentencelengthlist)
dutchaveragesentencelength = dutchtotalsentencelength / len(dutchallsentencelengthlist)
print('Dutch words per ref: ' + str(dutchaveragesentencelength))

englishaccidentssentencelength = MyToolWordsPerRef(currentpath + '/EnglishAccidents/Data/Alldatasets.pkl')
englishsportssentencelength = MyToolWordsPerRef(currentpath + '/EnglishSports/Data/Tempdataset.pkl', 'n')
englishsportssentencelengthtrain = ProdigyWordsPerRef(englishsportstrain)
englishsportssentencelengthdev = ProdigyWordsPerRef(englishsportsdev)
englishsportssentencelengthtest = ProdigyWordsPerRef(englishsportstest)
#englishstockstrain = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksTrain.jsonl')
englishstockssentencelengthtrain = ProdigyWordsPerRef(englishstockstrain)
englishstockssentencelengthdev = ProdigyWordsPerRef(englishstocksdev)
englishstockssentencelengthtest = ProdigyWordsPerRef(englishstockstest)
#englishweathertrain = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather.jsonl')
#englishweatherdev = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Dev.jsonl')
#englishweathertest = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Test.jsonl')
englishweathersentencelengthtrain = ProdigyWordsPerRef(englishweathertrain)
englishweathersentencelengthdev = ProdigyWordsPerRef(englishweatherdev)
englishweathersentencelengthtest = ProdigyWordsPerRef(englishweathertest)
englishallsentencelengthlist = englishaccidentssentencelength + englishsportssentencelength + englishsportssentencelengthtrain + englishsportssentencelengthdev + englishsportssentencelengthtest + englishweathersentencelengthtrain + englishweathersentencelengthdev + englishweathersentencelengthtest + englishstockssentencelengthtrain + englishstockssentencelengthdev + englishstockssentencelengthtest
englishtotalsentencelength = sum(englishallsentencelengthlist)
englishaveragesentencelength = englishtotalsentencelength / len(englishallsentencelengthlist)
print('English words per ref: ' + str(englishaveragesentencelength))