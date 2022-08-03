import pickle
import json
import jsonlines
import regex as re
import itertools
from lexicalrichness import LexicalRichness
import csv
import sys
maxInt = sys.maxsize
from somajo import SoMaJo
from nltk.util import ngrams
import collections
import statistics
import os

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def MyToolGetText(rdflist):
    textlist = []

    for rdf in rdflist:
        textlist.append(rdf['text'])

    textstring = '\n'.join(textlist)
    return textstring

def EnglishTopFrequencies():
    topwords = []
    newtopwords = []

    # Get the all.num file from the British National Corpus here: https://www.kilgarriff.co.uk/bnc-readme.html
    with open('BNCFILE', 'r', encoding='utf-8') as f:
        reader = f.readlines()
        for row in reader:
            topwords.append(re.search(r'^\d+\s(.*?)\s', row).group(1))

    for word in topwords[1:3000]:
        if (re.search(r"^\p{P}+$", word) == None) and (word.lower() not in newtopwords):
            newtopwords.append(word)

    return newtopwords[:2000]

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

def LexicalSophistication(text, topfrequencies):
    alltokens = word_tokenize(text)
    alltokens = [x.lower() for x in alltokens]

    alltypes = list(set(alltokens))
    uncommontypes = []
    for dt in alltypes:
        if dt not in topfrequencies:
            uncommontypes.append(type)
    ls = len(uncommontypes) / len(alltypes)
    return ls

def WordNGrams(rdflist, tokenizer, language):
    allbigrams = {}
    alltrigrams = {}

    for rdf in rdflist:
        sentencelist = []
        sentences = tokenizer.tokenize_text([rdf])
        for sentence in sentences:
            tokenlist = []
            for token in sentence:
                tokenlist.append(token.text)
            tokenlist = [token for token in tokenlist if (re.search(r"^\p{P}+$", token) == None) and (re.search('\n', token) == None)]
            bigrams = ngrams(tokenlist, 2)
            bigramscounter = collections.Counter(bigrams)
            bigramsdict = dict(bigramscounter)
            for bigram in bigramsdict:
                if bigram in allbigrams:
                    allbigrams[bigram] += bigramsdict[bigram]
                else:
                    allbigrams.update({bigram: bigramsdict[bigram]})

            trigrams = ngrams(tokenlist, 3)
            trigramscounter = collections.Counter(trigrams)
            trigramsdict = dict(trigramscounter)
            for trigram in trigramsdict:
                if trigram in alltrigrams:
                    alltrigrams[trigram] += trigramsdict[trigram]
                else:
                    alltrigrams.update({trigram: trigramsdict[trigram]})

    bigramssingleappearance = [k for k, v in allbigrams.items() if v == 1]
    print(language + ' proportion bigrams appearing 1x: ' + str(len(bigramssingleappearance) / len(allbigrams)))
    multipleappearance = [v for k, v in allbigrams.items() if v > 1]
    print(language + ' average bigrams appearing > 1x: ' + str(statistics.mean(multipleappearance)))

    trigramssingleappearance = [k for k, v in alltrigrams.items() if v == 1]
    print(language + ' proportion trigrams appearing 1x: ' + str(len(trigramssingleappearance) / len(alltrigrams)))
    multipleappearance = [v for k, v in alltrigrams.items() if v > 1]
    print(language + ' average trigrams appearing > 1x: ' + str(statistics.mean(multipleappearance)))

currentpath = os.getcwd()
#Get txt files of E2E
with open('$E2E DEVFILE$', 'rb') as f:
    englishrdfsdev = f.readlines()

with open('$E2E TESTFILE$', 'rb') as f:
    englishrdfstest = f.readlines()

with open('$E2E TRAINFILE$', 'rb') as f:
    englishrdfstrain = f.readlines()

englishrdfs = englishrdfsdev + englishrdfstest + englishrdfstrain
englishrdfs = [x.decode('utf-8') for x in englishrdfs]
englishrdfs = [re.sub(r'\n', '', x) for x in englishrdfs]

englishstring = '\n'.join(englishrdfs)
englishtokenizer = SoMaJo(language="en_PTB")
WordNGrams(englishrdfs, englishtokenizer, 'English')

#englishstring = MyToolGetText(englishrdfs)

englishlex = LexicalRichness(englishstring)

print('English Tokens: ' + str(englishlex.words))
print('English Types: ' + str(englishlex.terms))
print('English Type-Token Ratio: ' + str(englishlex.ttr))
print('English Mean Segmental Type-Token Ratio: ' + str(englishlex.msttr(segment_window=25)))

englishtopfrequencies = EnglishTopFrequencies()
englishls = LexicalSophistication(englishstring, englishtopfrequencies)
print('English Lexical Sophistication: ' + str(englishls))