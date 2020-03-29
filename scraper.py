import urllib.request
from bs4 import BeautifulSoup

def main():
    site = simple_get("https://www.classifiedads.com/search.php?cid=326&lid=rx8008&lname=Seattle%2C+WA&from=s&keywords=") #Makes a request to the site
    #site = html
    siteToParse = class_finder(site)
    results = href_finder(siteToParse)
    matches = open_links(results)
    if matches:
        print("Matches Found!")
        print(matches)


def simple_get(url):
    url = url
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
    links = []
    for link in soup.find_all('a'):
        links.append("https:" + link.get('href'))
    return links

def open_links(links):
    sitesToScan = []
    for x in links:
        sites = simple_get(x)
        soup = BeautifulSoup(sites, "html.parser")

        sitesToScan.append(str(soup).lower())
        sitesToScan.append("<a href=Pedolandasdfasdfasdf</a>")
    return termSearch(sitesToScan)

def termSearch(htmlToScan):
    bad_terms = []
    with open("bad terms.txt", "r") as term:
        for x in term:
            bad_terms.append(x)

    sitesToScan = htmlToScan #list of strings
    result = {} 
    for i in bad_terms:
        i = i.lower().strip()
        for x in sitesToScan:
            if i in x:
                if i in result:
                    result[i] += 1
                else:
                    result[i] = 1
    return str(result)
            
main()
