import sys
import os
import numpy as np
import nltk
import glob
from sklearn.preprocessing import normalize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from pathlib import Path
import pandas as pd
import math
import decimal
from sklearn.utils.extmath import randomized_svd

decimal.getcontext().rounding = decimal.ROUND_DOWN

import re
def comment_remover_py(code):
    code = str(code)
    return re.sub(r'(?m)^ *#.*\n?', ' ', code)

        # file names in directory
def comment_remover_java(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def extract_files ():
    dirname = [file for file in glob.glob(sys.argv[1]+"/*")]
    return dirname


def global_frequency():
    glcounts = dict()    #global dict to store df

    stop_words = set(stopwords.words('english'))

    for filename in extract_files():
        fhand = open(filename)
        content = fhand.read()
        if filename[-3:] == ".py" :
            content_without_comments = comment_remover_py(content)
            words = word_tokenize(content_without_comments)
        elif filename[-5:] == ".java" or filename[-4:]==".cpp" or filename[-2:]==".c":
            content_without_comments = comment_remover_java(content)
            words = word_tokenize(content_without_comments)
        else :
            words = word_tokenize(content)          

        for word in words:  
            if word not in stop_words: 
                if word.isalnum(): 
                    glcounts[word] = glcounts.get(word, 0) + 1   #add elements to glcount

    return glcounts

def tf():
    fileseq = []
    idtm = []
    glcounts=global_frequency()
    stop_words = set(stopwords.words('english'))
    for filename in extract_files():
        icounts = dict()           #to store term frequency
        fhand = open(filename)
        content = fhand.read()
        if filename[-3:] == ".py" :
            content_without_comments = comment_remover_py(content)
            words = word_tokenize(content_without_comments)
        elif filename[-5:] == ".java" or filename[-4:]==".cpp" or filename[-2:]==".c":
            content_without_comments = comment_remover_java(content)
            words = word_tokenize(content_without_comments)
        else :
            words = word_tokenize(content)  

        for word in words:  
            if word not in stop_words:  
                if word.isalnum():
                    icounts[word] = icounts.get(word, 0) + 1

        counts = dict()               #to store freq (tf*idf form) of each word in glcounts in THIS paticluar file
        for word in glcounts:
            counts[word] = icounts.get(word, 0)

        valist =  list(counts.values())
        idtm.append(valist)
        fileseq.append(os.path.basename(filename)) 

    return [fileseq, idtm]

def dtm_idf():
    idf = dict()
    glcounts=global_frequency()
    idtm = tf()[1]
    fileseq = tf()[0]
    i=0
    for word in glcounts:
        count=0
        for j in range(len(fileseq)):
            if idtm[j][i] != 0:
                count = count + 1
        idf[word] = math.log((1+len(fileseq))/(count))+1
        i=i+1

    i=0
    for word in glcounts:
        for j in range(len(fileseq)):
            idtm[j][i] = idtm[j][i]*idf[word] 
        i=i+1 


    return [fileseq, idtm]
    

def dim_k ( dtm ):
    u, s, vt = np.linalg.svd(dtm)

    emax=0
    for x in s:
        emax=emax+x*x
    k_req=0
    e=0
    for x in s:
        e=e+x*x
        k_req=k_req+1
        if e>0.9*emax:
            break
    return k_req


def main():

    dtm = np.array(dtm_idf()[1])
    k_req = dim_k(dtm)
    Ufunc = TruncatedSVD(k_req, algorithm = 'arpack')

    US = Ufunc.fit_transform(dtm)
    V=Ufunc.components_
    dtm_lsa = Normalizer(copy=False).fit_transform(US)
    similarity = np.asarray(np.asmatrix(dtm_lsa) * np.asmatrix(dtm_lsa).T)
    for i in range(len(dtm_idf()[0])):
        for j in range(len(dtm_idf()[0])):
            similarity[i][j] = float(round(similarity[i][j],3))
    df = pd.DataFrame(similarity,index=dtm_idf()[0], columns=dtm_idf()[0]).head(len(dtm_idf()[0]))
    result = df.to_csv('results.csv', index = True)

main()