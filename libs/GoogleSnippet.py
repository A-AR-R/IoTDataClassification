import urllib
import urllib2
from bs4 import BeautifulSoup
from utils import cleanhtml

class GoogleSnippet():
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = ".srg .rc .s"
    TOTAL_SELECTOR = "#resultStats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
        ('User-Agent', USER_AGENT),
        ("Accept-Language", "en-US,en;q=0.5"),
        ("accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        ]
    def get_snippets(self,query,count=30,language = "en"):
        start=0
        results=[]
        while len(results) < count and start < count:
            opener = urllib2.build_opener()
            opener.addheaders = GoogleSnippet.DEFAULT_HEADERS
            response = opener.open(GoogleSnippet.SEARCH_URL + "?q="+ urllib2.quote(query) + "&hl=" + language + ("" if start == 0 else ("&start=" + str(start))))

            data=response.read()
            soup = BeautifulSoup(data, "lxml")
            response.close()
            for item in soup.select(GoogleSnippet.RESULT_SELECTOR):
                soup = BeautifulSoup(str(item), "lxml")
                if soup.select(".TXwUJf"):
                    continue
                s=soup.select(".st")
                if s:
                    results.append(cleanhtml(str(s[0])))

            start+=GoogleSnippet.RESULTS_PER_PAGE
        return results
