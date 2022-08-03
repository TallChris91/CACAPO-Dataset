import pickle
import json
import jsonlines
from pysbd.utils import PySBDFactory
import spacy
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(PySBDFactory(nlp), first=True)
nlp.max_length = 1500000
import regex as re
import itertools
import en_core_web_md
import nl_core_news_md
from lexicalrichness import LexicalRichness
import csv
import sys
maxInt = sys.maxsize
from nltk.util import ngrams
import collections
import openpyxl
from somajo import SoMaJo
import statistics

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

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

def MyToolGetText(datasetpath, multipledomains='y'):
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

    mrstring = '\n'.join(mrlist)
    return mrstring

def ProdigyGetText(domaindata):
    mrlist = []

    for text in domaindata:
        for paragraph in text:
            for sentencedict in paragraph:
                mrlist.append(sentencedict['text'])

    mrstring = '\n'.join(mrlist)
    return mrstring

def DutchTopFrequencies():
    topwords = []
    newtopwords = []

    #Download the SONAR500 word frequency tsv file here: https://taalmaterialen.ivdnt.org/download/tstc-sonar-corpus/
    with open("SONARFILE", 'r', encoding='utf-8') as f:
        reader = f.readlines()
        for row in reader:
            topwords.append(re.search(r'^(.*?)\t', row).group(1))

    for word in topwords[:3000]:
        if (re.search(r"^\p{P}+$", word) == None) and (word.lower() not in newtopwords):
            newtopwords.append(word.lower())

    return newtopwords[:2000]

def EnglishTopFrequencies():
    topwords = []
    newtopwords = []

    #Get the all.num file from the British National Corpus here: https://www.kilgarriff.co.uk/bnc-readme.html
    with open('BNCFILE', 'r', encoding='utf-8') as f:
        reader = f.readlines()
        for row in reader:
            topwords.append(re.search(r'^\d+\s(.*?)\s', row).group(1))

    for word in topwords[1:3000]:
        if (re.search(r"^\p{P}+$", word) == None) and (word.lower() not in newtopwords):
            newtopwords.append(word.lower())

    return newtopwords[:2000]

def LexicalSophistication(text, topfrequencies, languagenlp):
    nldoc = languagenlp(text)
    dutchtokens = [token.text.lower() for token in nldoc if (re.search(r"^\p{P}+$", token.text) == None) and (token.text != '\n')]
    dutchtypes = list(set(dutchtokens))
    uncommontypes = []
    for dt in dutchtypes:
        if dt not in topfrequencies:
            uncommontypes.append(type)
    ls = len(uncommontypes) / len(dutchtypes)
    return ls

def WordNGrams(text, languagenlp, language):
    nldoc = languagenlp(text)
    tokenlist = [token.text.lower() for token in nldoc if (re.search(r"^\p{P}+$", token.text) == None) and (token.text != '\n')]

    newbigrams = []
    newtrigrams = []

    bigrams = ngrams(tokenlist, 2)
    bigramscounter = collections.Counter(bigrams)
    #bigramscounter = bigramscounter.most_common()
    bigramsdict = dict(bigramscounter)

    bigramssingleappearance = [k for k, v in bigramsdict.items() if v == 1]
    print(language + ' proportion bigrams appearing 1x: ' + str(len(bigramssingleappearance) / len(bigramsdict)))
    multipleappearance = [v for k, v in bigramsdict.items() if v > 1]
    print(language + ' average bigrams appearing > 1x: ' + str(statistics.mean(multipleappearance)))

    #for bigram in bigramscounter[:50]:
        #bigrampart = ' '.join(list(bigram[0]))
        #bigramlist = [bigrampart, bigram[1]]
        #newbigrams.append(bigramlist)

    trigrams = ngrams(tokenlist, 3)
    trigramscounter = collections.Counter(trigrams)
    #trigramscounter = trigramscounter.most_common()
    trigramsdict = dict(trigramscounter)

    trigramssingleappearance = [k for k, v in trigramsdict.items() if v == 1]
    print(language + ' proportion trigrams appearing 1x: ' + str(len(trigramssingleappearance) / len(trigramsdict)))
    multipleappearance = [v for k, v in trigramsdict.items() if v > 1]
    print(language + ' average trigrams appearing > 1x: ' + str(statistics.mean(multipleappearance)))

    #for trigram in trigramscounter[:50]:
        #trigrampart = ' '.join(list(trigram[0]))
        #trigramlist = [trigrampart, trigram[1]]
        #newtrigrams.append(trigramlist)

    '''
    # Now that we've got all the rows, we can save the Excel-file
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Ngram', 'Frequency'])
    for row in newbigrams:
        ws.append(row)

    wb.create_sheet('Trigrams')
    ws = wb['Trigrams']

    ws.append(['Ngram', 'Frequency'])
    for row in newtrigrams:
        ws.append(row)

    # And save this beauty!
    wb.save(os.getcwd() + '/Data/WordNGrams' + language + '.xlsx')
    '''

def GetSentenceList(englishstring):
    tokenizer = SoMaJo(language="en_PTB")
    sentences = tokenizer.tokenize_text([englishstring])
    sentencelist = []
    for sentence in sentences:
        tokenlist = []
        for token in sentence:
            tokenlist.append(token.text)
        sentencelist.append(tokenlist)
    return sentencelist

def GetJsonLines(filename):
    alllines = []

    with jsonlines.open(filename, mode='r') as reader:
        for obj in reader:
            alllines.append(obj['text'])
    # print(alllines[0:2])
    alllines = [x.strip() for x in alllines]
    allstring = '\n'.join(alllines)
    return allstring

currentpath = os.getcwd()
dutchaccidentstext = MyToolGetText(currentpath + '/DutchAccidents/Data/Alldatasets.pkl')
dutchsportstext = MyToolGetText(currentpath + '/DutchSports/Data/Alldatasets.pkl')
dutchweathertext = MyToolGetText(currentpath + '/DutchWeather/Data/Alldatasets.pkl')
dutchweatherdev = Convert_Prodigy(currentpath + '/DutchWeather/Data/DutchWeatherDev.jsonl')
dutchweatherdevtext = ProdigyGetText(dutchweatherdev)
dutchweathertest = Convert_Prodigy(currentpath + '/DutchWeather/Data/DutchWeatherTest.jsonl')
dutchweathertesttext = ProdigyGetText(dutchweathertest)
dutchstockstrain = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksTrain.jsonl')
dutchstockstraintext = ProdigyGetText(dutchstockstrain)
dutchstocksdev = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksDev.jsonl')
dutchstocksdevtext = ProdigyGetText(dutchstocksdev)
dutchstockstest = Convert_Prodigy(currentpath + '/DutchStocks/DutchStocksTest.jsonl')
dutchstockstesttext = ProdigyGetText(dutchstockstest)
dutchstring = dutchaccidentstext + '\n\n' + dutchsportstext + '\n\n' + dutchweathertext + '\n\n' + dutchweatherdevtext + '\n\n' + dutchweathertesttext + '\n\n' + dutchstockstraintext + '\n\n' + dutchstocksdevtext + '\n\n' + dutchstockstesttext

dutchlex = LexicalRichness(dutchstring)

print('Dutch Tokens: ' + str(dutchlex.words))
print('Dutch Types: ' + str(dutchlex.terms))
print('Dutch Type-Token Ratio: ' + str(dutchlex.ttr))
print('Dutch Mean Segmental Type-Token Ratio: ' + str(dutchlex.msttr(segment_window=25)))

dutchtopfrequencies = DutchTopFrequencies()
nlnlp = nl_core_news_md.load()
dutchls = LexicalSophistication(dutchstring, dutchtopfrequencies, nlnlp)
print('Dutch Lexical Sophistication: ' + str(dutchls))

#dutchtopfrequencies = DutchTopFrequencies()
#nlnlp = nl_core_news_md.load()
WordNGrams(dutchstring, nlnlp, 'Dutch')

englishaccidentstext = MyToolGetText(currentpath + '/EnglishAccidents/Data/Alldatasets.pkl')
englishsportstext = MyToolGetText(currentpath + '/EnglishSports/Data/Tempdataset.pkl', 'n')
englishsportstrain = GetJsonLines(currentpath + '/EnglishSports/Data/FullTrain.jsonl')
englishsportsdev = GetJsonLines(currentpath + '/EnglishSports/Data/FullDev.jsonl')
englishsportstest = GetJsonLines(currentpath + '/EnglishSports/Data/FullTest.jsonl')
englishstockstrain = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksTrain.jsonl')
englishstockstraintext = ProdigyGetText(englishstockstrain)
englishstocksdev = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksDev.jsonl')
englishstocksdevtext = ProdigyGetText(englishstocksdev)
englishstockstest = Convert_Prodigy(currentpath + '/EnglishStocks/EnglishStocksTest.jsonl')
englishstockstesttext = ProdigyGetText(englishstockstest)
englishweathertrain = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather.jsonl')
englishweatherdev = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Dev.jsonl')
englishweathertest = Convert_Prodigy(currentpath + '/EnglishWeather/Data/English_Weather_Test.jsonl')
englishweathertextttrain = ProdigyGetText(englishweathertrain)
englishweathertextdev = ProdigyGetText(englishweatherdev)
englishweathertexttest = ProdigyGetText(englishweathertest)
englishstring = englishaccidentstext + '\n\n' + englishsportstext + englishsportstrain + '\n\n' + englishsportsdev + '\n\n' + englishsportstest + '\n\n' + englishstockstraintext + '\n\n' + englishstocksdevtext + '\n\n' + englishstockstesttext + '\n\n' + englishweathertextttrain + '\n\n' + englishweathertextdev + '\n\n' + englishweathertexttest

accidentsentences = GetSentenceList(re.sub(r'\n+', ' ', englishaccidentstext))
sportssentences = GetSentenceList(re.sub(r'\n+', ' ', englishsportstext))
stockssentences = GetSentenceList(re.sub(r'\n+', ' ', englishstockstest))
weathertrainsentences = GetSentenceList(re.sub(r'\n+', ' ', englishweathertextttrain))
weatherdevsentences = GetSentenceList(re.sub(r'\n+', ' ', englishweathertextdev))
weathertestsentences = GetSentenceList(re.sub(r'\n+', ' ', englishweathertexttest))
allsentences = accidentsentences + sportssentences + stockssentences + weathertrainsentences + weatherdevsentences + weathertestsentences

englishlex = LexicalRichness(englishstring)

print('English Tokens: ' + str(englishlex.words))
print('English Types: ' + str(englishlex.terms))
print('English Type-Token Ratio: ' + str(englishlex.ttr))
print('English Mean Segmental Type-Token Ratio: ' + str(englishlex.msttr(segment_window=25)))

englishtopfrequencies = EnglishTopFrequencies()
ennlp = en_core_web_md.load()
ennlp.max_length = 1500000
englishls = LexicalSophistication(englishstring, englishtopfrequencies, ennlp)
print('English Lexical Sophistication: ' + str(englishls))

#ennlp = en_core_web_md.load()
#ennlp.max_length = 1500000
WordNGrams(englishstring, ennlp, 'English')
