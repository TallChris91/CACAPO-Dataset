import pickle
import zipfile
import regex as re
import os
from spacy.lang.nl import Dutch
nlnlp = Dutch()
nlnlp.add_pipe(nlnlp.create_pipe('sentencizer'))

#Change this to the location of your Zip file containing all the texts
currentpath = os.getcwd()
zf = currentpath + '/All.zip'

alltexts = []
allfilenames = []

with zipfile.ZipFile(zf) as z:
    for filename in z.namelist():
        if filename.endswith('.txt'):
            with z.open(filename, 'r') as f:
                fulltext = f.read()
                fulltext = fulltext.decode('utf-8-sig')
                paragraphs = re.split(r'[\n\r]+', fulltext)
                paragraphs = [re.sub(r'^\s+', '', x) for x in paragraphs]
                paragraphs = [re.sub(r'\s+$', '', x) for x in paragraphs]
                paragraphslines = []
                for paragraph in paragraphs:
                    nldoc = nlnlp(paragraph)
                    lines = [sent.string.strip() for sent in nldoc.sents]
                    paragraphslines.append(lines)

                alltexts.append(paragraphslines)
                allfilenames.append(filename)

alltexts = [alltexts]
allfilenames = [allfilenames]

with open(currentpath + '/Data/Textlist.pkl', 'wb') as f:
    pickle.dump(alltexts, f)

with open(currentpath + '/Data/Filenamelist.pkl', 'wb') as f:
    pickle.dump(allfilenames, f)