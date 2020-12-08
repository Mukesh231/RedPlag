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
    """!
    Removes comments from Python code.
    
    @param code Python code as a string 
    @return Code without any comments.
    
    """
    code = str(code)
    return re.sub(r'(?m)^ *#.*\n?', ' ', code)


def comment_remover_java(text):
    """!
    Removes comments from C, C++ or java code

    @param text C, C++ or Java code as a string
    @return Code without any comments.

    """
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

def extract_files():
    """!
    No parameters, Directory name is taken as input from the console.
    @return List containing relative pathways to files belonging to the given directory 

    """
    dirname = [file for file in glob.glob(sys.argv[1]+"/*")]
    return dirname

def global_frequency():

    """!
    Stop words and comments are removed. Every word is converted to lower case.
    @return A dictionary **glcounts**. This is a bag of words representation of the entire corpus
        
        
    """

    glcounts = dict()    #global dict to store df

    stop_words = set(stopwords.words('english'))

    for filename in extract_files():
        fhand = open(filename)
        content = fhand.read()
        content = content.lower()
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

    """!
    Total document frequency for each term is obtained as a result of the global_frequency() function

    Iteration through files is done via the extract_files() function.

    Every word is converted to lower case. 


    @return Term-document matrix comprising of term frequencies and a file sequence to keep track of the iteration order

    @see global_frequency(), extract_files()

    """


    fileseq = []
    idtm = []
    glcounts=global_frequency()
    stop_words = set(stopwords.words('english'))
    for filename in extract_files():
        icounts = dict()           #to store term frequency
        fhand = open(filename)
        content = fhand.read()
        content = content.lower()
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

    """!
    Computes inverse document frequency for each term. 

    Total document frequency for each term is obtained as a result of the global_frequency() function

    Term-document matrix and file sequence are obtained as a result of the tf() function

    Idf is calculated as \f$idf(t) \; = \; 1 + log((N+1)/no.of \; documents \; containing \; t)\f$. 
    
    @return The tf-idf term-document matrix and file sequence (rows index)
    
    """

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

def dim_k(dtm):

    """!
    @param dtm The document term matrix
    @return Appropriate number of topics for dimensionality reduction
    
    """
    u, s, vt = np.linalg.svd(dtm)
    if len(s)>300:
        return 300
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

    """!
    Computes degree of similarity for each pair of documents from the refined term-document matrix.
    Term document matrix is obtained from the dtm_idf() function 

    Stores the results in matrix format in a csv file.
    
    """
    dtm = np.array(dtm_idf()[1])
    k_req = dim_k(dtm)
    Ufunc = TruncatedSVD(k_req, algorithm = 'randomized')
    print(dtm.shape)
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