import urllib
import csv
from bs4 import BeautifulSoup
import re
import pandas as pd 


        

def main():
    site = 'https://www.classifiedads.com/search.php?keywords=&cid=15&lid=rx8008&lname=Seattle%2C+WA&from=c'
    siteList = (javascript_finder()) + (page_navi()) + (css_finder()) + (img_finder() + (php_finder()))
    siteList, extraList = getPageLink(siteList, site) #function sorts through duplicates, external links, javascript:void(0) --- it is worth checking to see if any of these are important and should be scanned
    
    f = open('links.txt', "w")
    f.write('\n'.join(siteList))
    f.write('\n'.join(extraList))
    f.close()

def simple_get():
    url = 'https://www.classifiedads.com/search.php?keywords=&cid=15&lid=rx8008&lname=Seattle%2C+WA&from=c'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    return response


def javascript_finder():
    site = simple_get()
    soup = BeautifulSoup(site, "html.parser")
    l = [i.get('src') for i in soup.find_all('script') if i .get('src')]
    l = [x.encode('utf-8') for x in l]
    return l


def page_navi():
    site = simple_get()
    soup = BeautifulSoup(site, "html.parser")
    l = [i.get('href') for i in soup.find_all('a') if i .get('href')]
    l = [x.encode('utf-8') for x in l]
    return l


def img_finder():
    site = simple_get()
    soup = BeautifulSoup(site, "html.parser")
    l = [i.get('src') for i in soup.find_all('img') if i .get('src')]
    l = [x.encode('utf-8') for x in l]
    return l


def css_finder():
    site = simple_get()
    soup = BeautifulSoup(site, "html.parser")
    l = [i.get('href') for i in soup.find_all('link') if i .get('href')]
    l = [x.encode('utf-8') for x in l]
    return l

def php_finder():
    site = simple_get()
    soup = BeautifulSoup(site, "html.parser")
    l = [i.get('href') for i in soup.find_all('/link.php') if i .get('href')]
    l = [x.encode('utf-8') for x in l]
    return l

def getPageLink(siteList, site):
    siteList = list(set(siteList))
    extraList = []
    for item in siteList:
        if "php" in str(item):
            extraList.append(item)
            siteList.remove(item)
    for item in siteList:
        if "http" in str(item):
            extraList.append(item)
            siteList.remove(item)
    for item in siteList:
        if 'tel:' in str(item):
            siteList.remove(item)
    for item in siteList:
        if item == "javascript:void(0);":
            siteList.remove(item)
    for item in siteList:
        if item == "#":
            siteList.remove(item)

    siteList = [str(site) + str(s) for s in siteList]
    return siteList, extraList

main()
