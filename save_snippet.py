__author__ = 'Alipour'
from libs.Snippet import Snippet
import os
import time
_snippet1=Snippet()
words=[]
file=open("en-mc-30.csv","r")
line=file.readline()
if not os.path.exists("snippets7"):
    os.makedirs("snippets7")
while line:
    words.append(line.strip().split(",")[0])
    words.append(line.strip().split(",")[1])
    line=file.readline()
for item in list(set(words)):
    print item
    word_file=open("snippets7/"+item+".txt","w+")
    for snippet in _snippet1.get_snippets("\""+item+" is a\""):
        word_file.write(snippet.strip()+"\n")
    word_file.close()
    time.sleep(10)