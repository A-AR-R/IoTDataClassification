__author__ = 'Alipour'
from collections import Counter
from nltk.stem import PorterStemmer
from libs.utils import SearchSequence
import scipy
import math
class DPW():
    def __init__(self):
        self.all_tokens=[]
        self.dpw=[]
        self.final_dpw={}
        self.optimized_dpw={}
    def stem_filter(self):
        tokens=[]
        ps = PorterStemmer()
        for token in self.all_tokens:
            tokens.append(ps.stem(token))
            # tokens.append(token)
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
            self.dpw.extend(self.all_tokens[index+l:index+7])
        c=Counter(self.dpw)
        # print c
        # return c.most_common(n=8)
        self.final_dpw=dict(c)
        return dict(c)
    def optimize_dpw(self,all_words,pvalue=0.3):
        p=0
        for item in self.final_dpw.keys():
            p+=self.final_dpw[item]
        for item in self.final_dpw.keys():
            k=self.final_dpw[item]
            # p=len(all_words)
            v=len(self.final_dpw.keys())*1.0
            s=0
            for i in range(1,k+1):
                r=scipy.misc.comb(p,i)
                for index in range(p-i):
                    r=r*((v-1)/v)
                for j in range(i):
                    r=r/v
                s+=r
                # s+=itertools.combinations(p,i)*math.pow(v-1,p-i)
            # print 1-s
            if 1-s < pvalue:
                self.optimized_dpw.update({item:self.final_dpw[item]})
        return self.optimized_dpw
    @staticmethod
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