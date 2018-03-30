__author__ = 'Alipour'
from collections import Counter
from nltk.stem import PorterStemmer
from libs.utils import SearchSequence

class DPW_Extractor():
    def __init__(self):
        self.all_tokens=[]
        self.dpw=[]
    def stem_filter(self):
        tokens=[]
        ps = PorterStemmer()
        for token in self.all_tokens:
            tokens.append(ps.stem(token))
        return tokens
    def stem_list(self,l):
        tokens=[]
        ps = PorterStemmer()
        for token in l:
            tokens.append(ps.stem(token))
        return tokens
    def create_dpw(self,query):
        ps = PorterStemmer()
        q=[]
        for token in query:
            q.append(ps.stem(token))
        for index in SearchSequence(self.all_tokens,q):
            l=len(q)
            self.dpw.extend(self.all_tokens[index-7:index])
            self.dpw.extend(self.all_tokens[index+l:index+l+7])
        c=Counter(self.dpw)
        return c.most_common()