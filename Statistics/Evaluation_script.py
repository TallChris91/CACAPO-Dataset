import sacrebleu
import regex as re
from sacremoses import MosesDetokenizer
import string
from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.meteor_score import meteor_score
from nltk.translate.nist_score import corpus_nist
import os
import warnings
from bert_score import score
import statistics

##Add the locations of the resulting TGen output file and the Reference Test file
tgenoutput = "TGen output here!"
referencefile = "Reference test file here!"

def bleu_score(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f:
        references = f.readlines()
    with open(file2, 'r', encoding='utf-8') as f:
        candidates = f.readlines()

    md = MosesDetokenizer(lang='en')
    references = [re.sub(r'\n', '', x) for x in references]
    candidates = [re.sub(r'\n', '', x) for x in candidates]
    #references = [x.strip(string.punctuation) for x in references]
    #candidates = [x.strip(string.punctuation) for x in candidates]
    bleu = sacrebleu.corpus_bleu(candidates, [references])
    return bleu

#Get the BLEU score
bleu = bleu_score(tgenoutput, referencefile)
print(bleu)

def nist_score(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f:
        references = f.readlines()
    with open(file2, 'r', encoding='utf-8') as f:
        candidates = f.readlines()

    references = [x.split() for x in references]
    references = [[x] for x in references]
    candidates = [x.split() for x in candidates]
    #print(len(references))
    #print(len(candidates))
    score = corpus_nist(references, candidates)
    return score

#Get the NIST score
warnings.filterwarnings(action='ignore', category=UserWarning)
nist = nist_score(tgenoutput, referencefile)
print("Nist score: " + str(nist))

def bert_score(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f:
        references = f.readlines()
    with open(file2, 'r', encoding='utf-8') as f:
        candidates = f.readlines()

    P, R, F1 = score(candidates, references, lang='en', verbose=True)
    return P, R, F1

#Get the BertScore score
bertp, bertr, bertf1 = bert_score(tgenoutput, referencefile)
print(f"System level Precision score: {bertp.mean():.6f}")
print(f"System level Recall score: {bertr.mean():.6f}")
print(f"System level F1 score: {bertf1.mean():.6f}")

#Mean meteor score
def ms_function(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f:
        references = f.readlines()
    with open(file2, 'r', encoding='utf-8') as f:
        candidates = f.readlines()

    allscores = []

    for idx, val in enumerate(references):
        ms = meteor_score([references[idx]], candidates[idx])
        allscores.append(ms)

    meanscore = statistics.mean(allscores)
    return meanscore

ms = ms_function(tgenoutput, referencefile)

print(ms)