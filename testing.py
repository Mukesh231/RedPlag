import sys
import numpy as np
import nltk
import glob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from pathlib import Path
import pandas as pd

dirname = [file for file in glob.glob(sys.argv[1]+"/*")]

fileseq = []
idtm = []

glcounts = dict()    #global dict to store df

stop_words = set(stopwords.words('english'))

for filename in dirname:
    fhand = open(filename)
    content = fhand.read()

    words = word_tokenize(content)  

    for word in words:  
        if word not in stop_words: 
            if word.isalnum(): 
                glcounts[word] = glcounts.get(word, 0) + 1   #add elements to glcount

for filename in dirname:
    icounts = dict()           #to store term frequency
    fhand = open(filename)
    content = fhand.read()
    words = word_tokenize(content)  

    for word in words:  
        if word not in stop_words:  
            if word.isalnum():
                icounts[word] = icounts.get(word, 0) + 1

    counts = dict()               #to store freq (tf*idf form) of each word in glcounts in THIS paticluar file
    for word in glcounts:
        counts[word] = icounts.get(word, 0)/glcounts[word]

    valist =  list(counts.values())
    idtm.append(valist)
    fileseq.append(filename)  #extract string

dtm = np.array(idtm)
Ufunc = TruncatedSVD(3, algorithm = 'arpack')
U = Ufunc.fit_transform(dtm)
U = Normalizer(copy=False).fit_transform(U)
similarity = np.asarray(np.asmatrix(U) * np.asmatrix(U).T)
df = pd.DataFrame(similarity,index=fileseq, columns=fileseq).head(len(fileseq))
result = df.to_csv('results.csv', index = True) 