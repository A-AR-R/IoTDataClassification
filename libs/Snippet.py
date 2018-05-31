__author__ = 'Alipour'
import urllib2
from bs4 import BeautifulSoup
from utils import cleanhtml
from utils import Pool
import time
import os

class Snippet():
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    DEFAULT_HEADERS = [
    ('User-Agent', USER_AGENT),
    ("Accept-Language", "en-US,en;q=0.5"),
    ("accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    ]

    def __init__(self):
        pass
    def yandex(self,query,page=0):
        results=[]
        opener = urllib2.build_opener()
        opener.addheaders = Snippet.DEFAULT_HEADERS
        # response = opener.open("https://www.ecosia.org/search?q=atomobile")
        response = opener.open("https://yandex.com/search/?text=%s&p=%s"%(query,page))
        data=response.read()
        soup = BeautifulSoup(data, "lxml")
        response.close()
        if "Unfortunately, it looks like the search requests sent from your IP address are " in data:
            print "yandex is out"
            return
        for item in soup.select(".serp-item .text-container"):
            results.append(cleanhtml(str(item)).lower())

        return results
    def ecosia(self,query,page=0):
        results=[]
        opener = urllib2.build_opener()
        opener.addheaders = Snippet.DEFAULT_HEADERS
        # response = opener.open("https://www.ecosia.org/search?q=atomobile")
        response = opener.open("https://www.ecosia.org/search?q=%s&p=%s"%(query,page))
        data=response.read()
        soup = BeautifulSoup(data, "lxml")
        response.close()
        for item in soup.select(".result .result-snippet"):
            results.append(cleanhtml(str(item)).lower())
        return results
    def swisscows(self,query,page):
        results=[]
        opener = urllib2.build_opener()
        opener.addheaders = Snippet.DEFAULT_HEADERS
        opener.addheaders.append(("x-requested-with","XMLHttpRequest"))
        response = opener.open("https://swisscows.com/?query="+query+"&region=browser&uiLanguage=browser&_=1527744565363&apiGuard=bOcKoGyOpwJtnnhsSvhyPla8bCcZXAsC7xuUM%2Bxb%2FkhNHuzU68sBP1Wckiy5Pev%2FYEx88li2qrAonn7o&page="+str(page+1))
        data=response.read()
        import jsonpickle
        for item in jsonpickle.decode(data)["Results"]["items"]:
            results.append(cleanhtml(item["Description"]).encode("utf-8").lower())
        return results
    def bing(self,query,page):
        results=[]
        opener = urllib2.build_opener()
        opener.addheaders = Snippet.DEFAULT_HEADERS
        # response = opener.open("https://www.ecosia.org/search?q=atomobile")
        response = opener.open("https://www.bing.com/search?q=%s&first=%s"%(query,(page*10)))
        data=response.read()
        soup = BeautifulSoup(data, "lxml")
        response.close()
        for item in soup.select(".b_algo .b_caption p"):
            results.append(cleanhtml(str(item)).lower())
        return results
    def google(self,query,page):
        results=[]
        opener = urllib2.build_opener()
        opener.addheaders = Snippet.DEFAULT_HEADERS
        response = opener.open("https://google.com/search?q=%s&first=%s"%(query,(page*10)))
        data=response.read()
        soup = BeautifulSoup(data, "lxml")
        response.close()

        for item in soup.select(".srg .rc .sa"):
                soup = BeautifulSoup(str(item), "lxml")
                if soup.select(".TXwUJf"):
                    continue
                s=soup.select(".st")
                if s:
                    results.append(cleanhtml(str(s[0])))

        return results
    def load_from_file(self,path):
        snippets_dict={}
        for item in os.listdir(path):
            file = open(path+"/"+item,"r")
            line = file.readline()
            snippets=[]
            while line:
                snippets.append(line.strip())
                line = file.readline()
            file.close()
            snippets_dict.update({
                item.split(".")[0]:list(snippets)
            })
        return snippets_dict
    def get_snippets(self,query):
        results=[]
        p=Pool(2)
        query=urllib2.quote(query)
        for i in range(30):
            # p.enqueue(self.yandex, query,i)
            # p.enqueue(self.ecosia, query,i)
            # p.enqueue(self.swisscows, query,i)
            p.enqueue(self.google,query,i)
            # p.enqueue(self.google,query,i)
        p.run(True)
        while not p.done() or not p.idle():
            time.sleep(1)
        for result in p.results():
            results.extend(result)
        return results
