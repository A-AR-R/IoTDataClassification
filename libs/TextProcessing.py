__author__ = 'Alipour'
from nltk.tokenize import word_tokenize
import nltk.corpus
import string
import re


class TextProcessing():
    printable = set(string.printable)
    stopwords = nltk.corpus.stopwords.words('english')
    def filter_printable(self,data):
        filtered = filter(lambda x: x in TextProcessing.printable, data)
        return filtered
    def filter_google_specific(self,data):
        filtered = re.sub( r'^\D{3}\s+\d{1,2}, \d{4} -',"", data, re.M|re.I)
        return filtered
    def tokenize(self,data):
        tokens=word_tokenize(data.lower())
        return tokens
    def remove_stop_words(self,tokens):
        tokens_copy = list(tokens)
        for item in tokens_copy:
            if item in TextProcessing.stopwords:
                tokens.remove(item)
        return tokens
    def remove_long_short_words(self,tokens):
        tokens_copy = list(tokens)
        for item in tokens_copy:
            if len(item)<=3 or len(item)>=14:
                tokens.remove(item)
        return tokens
    def remove_query(self,tokens,query):
        tokenized_query = word_tokenize(query.lower())
        tokens_new = filter(lambda i: i not in tokenized_query, tokens)
        return tokens_new