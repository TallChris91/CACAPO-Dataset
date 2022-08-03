import pickle
import zipfile
import regex as re
import os
from pysbd.utils import PySBDFactory
import spacy
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(PySBDFactory(nlp), first=True)
import json

currentpath = os.getcwd()

allfile = currentpath + '/Corpus/EnglishAccidentReportsSample.zip'
alltexts = []

allfilenames = []

with zipfile.ZipFile(allfile) as z:
    for filename in z.namelist():
        with z.open(filename) as f:
            data = f.read()
            d = json.loads(data.decode("utf-8"))
            fulltext = d['text']
            #fulltext = fulltext.decode('utf-8-sig')
            paragraphs = re.split(r'[\n\r]+', fulltext)
            paragraphs = [re.sub(r'^\s+', '', x) for x in paragraphs]
            paragraphs = [re.sub(r'\s+$', '', x) for x in paragraphs]
            paragraphslines = []
            for paragraph in paragraphs:
                doc = nlp(paragraph)
                lines = [sent.string.strip() for sent in doc.sents]
                paragraphslines.append(lines)

            paragraphslines = [x for x in paragraphslines if x != []]

            alltexts.append(paragraphslines)
            allfilenames.append(filename)


alltexts = [alltexts]
allfilenames = [allfilenames]

print(len(alltexts))
print(len(alltexts[0]))

with open(currentpath + '/Data/Textlist.pkl', 'wb') as f:
    pickle.dump(alltexts, f)

with open(currentpath + '/Data/Filenamelist.pkl', 'wb') as f:
    pickle.dump(allfilenames, f)