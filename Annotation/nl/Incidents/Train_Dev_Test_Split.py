import numpy as np
import pickle
import os

currentpath = os.getcwd()

with open(currentpath + '/Data/Alldatasets.pkl', 'rb') as f:
    datasetconcatenated = pickle.load(f)

with open(currentpath + '/Data/Filenamelist.pkl', 'rb') as f:
    filenamesconcatenated = pickle.load(f)

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

print(len(trainsample))
print(len(devsample))
print(len(testsample))

newdatalisttrain = np.array(datasetconcatenated)[trainsample]
newdatalistdev = np.array(datasetconcatenated)[devsample]
newdatalisttest = np.array(datasetconcatenated)[testsample]

newfilenamestrain = np.array(filenamesconcatenated)[trainsample]
newfilenamesdev = np.array(filenamesconcatenated)[devsample]
newfilenamestest = np.array(filenamesconcatenated)[testsample]

newdatalisttrain = newdatalisttrain.tolist()
newdatalistdev = newdatalistdev.tolist()
newdatalisttest = newdatalisttest.tolist()

newfilenamestrain = newfilenamestrain.tolist()
newfilenamesdev = newfilenamesdev.tolist()
newfilenamestest = newfilenamestest.tolist()

newdatasets = [newdatalisttrain, newdatalistdev, newdatalisttest]

newfilenames = [newfilenamestrain, newfilenamesdev, newfilenamestest]

with open(currentpath + '/Data/AlldatasetsNewSplit.pkl', 'wb') as f:
    pickle.dump(newdatasets, f)

with open(currentpath + '/Data/FilenamelistNewSplit.pkl', 'wb') as f:
    pickle.dump(newfilenames, f)
