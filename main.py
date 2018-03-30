# -*- coding: utf-8 -*-
from libs.GoogleSnippet import GoogleSnippet
from libs.TextProcessing import TextProcessing
from libs.DPW_Extractor import DPW_Extractor
import scipy.misc
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk.corpus
import string
import datetime
import re
g=GoogleSnippet()
tp=TextProcessing()
de=DPW_Extractor()

query="moisture"

for item in g.get_snippets(query,count=100):
    data=tp.filter_printable(item)
    data=tp.filter_google_specific(data)
    tokens=tp.tokenize(data)
    tokens=tp.remove_stop_words(tokens)
    tokens=tp.remove_long_short_words(tokens)
    de.all_tokens.extend(tokens)

all_words=de.all_tokens
de.all_tokens = de.stem_filter()
vector1= dict(de.create_dpw(tp.tokenize(query)))
print de.all_tokens
print de.dpw
print vector1

for item in vector1.keys():
    k=vector1[item]
    p=len(all_words)
    v=len(vector1.keys())*1.0
    s=0
    for i in range(1,k+1):
        r=scipy.misc.comb(p,i)
        for index in range(p-i):
            r=r*((v-1)/v)
        for j in range(i):
            r=r/v
        s+=r
        # s+=itertools.combinations(p,i)*math.pow(v-1,p-i)

    print item,1-s

g=GoogleSnippet()
tp=TextProcessing()
de=DPW_Extractor()


query="humidity"
for item in g.get_snippets(query,count=100):
    data=tp.filter_printable(item)
    data=tp.filter_google_specific(data)
    tokens=tp.tokenize(data)
    tokens=tp.remove_stop_words(tokens)
    tokens=tp.remove_long_short_words(tokens)
    de.all_tokens.extend(tokens)

all_words=de.all_tokens
de.all_tokens = de.stem_filter()
vector2= dict(de.create_dpw(tp.tokenize(query)))
print de.all_tokens
print de.dpw
print vector2

for item in vector2.keys():
    k=vector2[item]
    p=len(all_words)
    v=len(vector2.keys())*1.0
    s=0
    for i in range(1,k+1):
        r=scipy.misc.comb(p,i)
        for index in range(p-i):
            r=r*((v-1)/v)
        for j in range(i):
            r=r/v
        s+=r
        # s+=itertools.combinations(p,i)*math.pow(v-1,p-i)

    print item,1-s

import re, math
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator
cosine = get_cosine(vector1, vector2)
print cosine