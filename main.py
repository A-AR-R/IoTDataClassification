# -*- coding: utf-8 -*-
from libs.GoogleSnippet import GoogleSnippet
from libs.Snippet import Snippet
from libs.TextProcessing import TextProcessing
from libs.DPW import DPW
from libs.DPWC import DPWC
import math

file = open("en-mc-30.csv","r")
line = file.readline()

_snippets=Snippet().load_from_file("snippets5")
print "loaded"
dataset_cosines=[]
our_cosines=[]
while line:
    query1,query2,similarity=line.strip().split(",")

    # _snippet1=Snippet()
    _textProcessing1=TextProcessing()
    _dpw1=DPW()
    filtered_snippets1=[]

    for item in _snippets[query1]:
        item=item.lower()
        data=_textProcessing1.filter_printable(item)
        data=_textProcessing1.filter_date(data)
        data=_textProcessing1.filter_integer(data)
        tokens=_textProcessing1.tokenize(data)
        tokens=_textProcessing1.remove_stop_words(tokens)
        tokens=_textProcessing1.remove_long_short_words(tokens)
        _dpw1.all_tokens.extend(tokens)
        filtered_snippets1.append(data)
    all_words=_dpw1.all_tokens
    _dpw1.all_tokens = _dpw1.stem_filter()
    _dpw1.create_dpw(_textProcessing1.tokenize(query1))
    _dpw1.optimize_dpw(_dpw1.all_tokens,pvalue=0.1)
    _dpwc1=DPWC(_dpw1.optimized_dpw,filtered_snippets1)
    # _dpwc1.calc_co_occurrence()
    # _dpwc1.affinity_propagation()
    # print _dpwc1.calculate_profile()
    # _snippet2=Snippet()
    _textProcessing2=TextProcessing()

    _dpw2=DPW()
    filtered_snippets2=[]

    for item in _snippets[query2]:
        data=_textProcessing2.filter_printable(item)
        data=_textProcessing2.filter_date(data)
        data=_textProcessing2.filter_integer(data)
        tokens=_textProcessing2.tokenize(data)
        tokens=_textProcessing2.remove_stop_words(tokens)
        tokens=_textProcessing2.remove_long_short_words(tokens)

        _dpw2.all_tokens.extend(tokens)
        filtered_snippets2.append(data)
    all_words=_dpw2.all_tokens

    _dpw2.all_tokens = _dpw2.stem_filter()

    _dpw2.create_dpw(_textProcessing2.tokenize(query2))

    _dpw2.optimize_dpw(_dpw2.all_tokens,pvalue=0.1)
    _dpwc2=DPWC(_dpw2.optimized_dpw,filtered_snippets2)
    # _dpwc2.calc_co_occurrence()


    cosine = DPW.get_cosine(_dpw1.optimized_dpw, _dpw2.optimized_dpw)

    print _dpw1.optimized_dpw
    print _dpw2.optimized_dpw
    print query1,query2,float(similarity),cosine
    dataset_cosines.append(float(similarity))
    our_cosines.append(float(cosine))
    line = file.readline()
def pearson_correlation(numbers_x, numbers_y):
    mean_x = sum(numbers_x)/len(numbers_x)
    mean_y = sum(numbers_y)/len(numbers_y)

    subtracted_mean_x = [i - mean_x for i in numbers_x]
    subtracted_mean_y = [i - mean_y for i in numbers_y]

    x_times_y = [a * b for a, b in list(zip(subtracted_mean_x, subtracted_mean_y))]

    x_squared = [i * i for i in numbers_x]
    y_squared = [i * i for i in numbers_y]

    return sum(x_times_y) / math.sqrt(sum(x_squared) * sum(y_squared))
print pearson_correlation(our_cosines,dataset_cosines)