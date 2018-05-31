import urllib2
results=[]

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
DEFAULT_HEADERS = [
    ('User-Agent', USER_AGENT),
    ("Accept-Language", "en-US,en;q=0.5"),
    ("accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    # ("accept","application/json, text/javascript, */*; q=0.01")
]
import jsonpickle
opener = urllib2.build_opener()
opener.addheaders = DEFAULT_HEADERS
# opener.addheaders.append(("Cookie","hash=Swisscows_bpftgwarps2j00socmogyu2c"))
# opener.addheaders.append(("referer","https://swisscows.com/"))
# opener.addheaders.append(("authority","swisscows.com"))
opener.addheaders.append(("x-requested-with","XMLHttpRequest"))
# response = opener.open("https://www.ecosia.org/search?q=atomobile")

for i in range(30):
    response = opener.open("https://swisscows.com/?query=\"chord+is+a\"&region=browser&uiLanguage=browser&_=1527744565363&apiGuard=bOcKoGyOpwJtnnhsSvhyPla8bCcZXAsC7xuUM%2Bxb%2FkhNHuzU68sBP1Wckiy5Pev%2FYEx88li2qrAonn7o&page="+str(i))
    data=response.read()
    for item in jsonpickle.decode(data)["Results"]["items"]:
        print item["Description"]