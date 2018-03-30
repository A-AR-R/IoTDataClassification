import re
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def _SearchSequence(forward, source, target, start=0, end=None):
    """Naive search for target in source."""
    indexs=[]
    m = len(source)
    n = len(target)
    if end is None:
        end = m
    else:
        end = min(end, m)
    if n == 0 or (end-start) < n:
        # target is empty, or longer than source, so obviously can't be found.
        return indexs
    if forward:
        x = range(start, end-n+1)
    else:
        x = range(end-n, start-1, -1)
    for i in x:
        if source[i:i+n] == target:
            indexs.append(i)
    return indexs

import functools
SearchSequence = functools.partial(_SearchSequence, True)