import urllib
from bs4 import BeautifulSoup

def main():
    site = simple_get() #Makes a request to the site
    siteToParse = class_finder(site)
    results = href_finder(siteToParse)
    links = []
    for x in results: 
       links.append(str(x))
    f = open("links.txt", "w")
    f.write('\n'.join(links))
    f.close


def simple_get():
    url = 'https://www.classifiedads.com/search.php?cid=326&lid=rx8008&lname=Seattle%2C+WA&from=s&keywords='
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    return response


def class_finder(site):
    site = site
    soup = BeautifulSoup(site, "html.parser")
    results = soup.find_all('div',{"class": "resultitem"})
    return results


def href_finder(site):
    site = site
    soup = BeautifulSoup(str(site), "html.parser")
    results = soup.find_all('a')
    return results
    
main()
