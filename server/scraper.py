import urllib.request
from bs4 import BeautifulSoup
import csv

WEIGHTING = [0, 10, 40, 60, 80, 120]

def main(html, url='replaceme.com'):
    link_matches = {}
    terms = get_terms('bad_terms.csv')
    if 'classifiedads.com' in url:
        #site = simple_get("https://www.classifiedads.com/search.php?cid=326&lid=rx8008&lname=Seattle%2C+WA&from=s&keywords=") #Makes a request to the site
        site = simple_get(url)
        siteToParse = class_finder(site)
        links = href_finder(siteToParse)
        html_blobs = open_links(links)
        link_matches = search_terms(terms, html_blobs)
    root_matches = root_search(terms, html)


    return {'root_matches': root_matches, 'link_matches': link_matches}


def simple_get(url):
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
    soup = BeautifulSoup(site, "html.parser")
    results = soup.find_all('div',{"class": "resultitem"})
    return results


def href_finder(site):
    soup = BeautifulSoup(str(site), "html.parser")
    links = []
    for link in soup.find_all('a'):
        links.append("https:" + link.get('href'))
    return links


def get_terms(fname):
    bad_terms = []
    with open(fname, "r", encoding='utf-8') as file:
        csvreader = csv.reader(file)
        #discard headers
        next(csvreader)
        for row in csvreader:
            bad_terms.append(row)
    return bad_terms

def open_links(links):
    results = []
    for url in links:
        try:
            sites = simple_get(url)
            soup = BeautifulSoup(sites, "html.parser")
            results.append((url, str(soup)))
        except Exception as e:
            print(e)
    return results

def search_terms(bad_terms, blobs):
    results = {}
    for row in bad_terms:
        term = row[0]
        for i in blobs:
            url = i[0]
            html = i[1].lower()
            num_matches = html.count(term.lower().strip())
            if num_matches > 0:
                print('we found something')
                if url in results:
                    print('return trip')
                    results[url]['terms'].add(term)
                    results[url]['risk'].append(int(row[2]))
                else:
                    print('first timer')
                    terms = set()
                    terms.add(term)
                    result = {'terms':terms, 'risk': [int(row[2])]}
                    results[url] = result
    for k,v in results.items():
        v['terms'] = list(v['terms'])

    #calculate Score
    denom = sum(WEIGHTING)

    for k,v in results.items():
        denom = 0
        numerator = 0
        for score in v['risk']:
            print(f'init score is {score}')
            print(f'init weight is {WEIGHTING[score]} ')
            numerator += score * WEIGHTING[score]
            denom += WEIGHTING[score]
        denom = 1 if denom ==0 else denom
        v['score'] = round(numerator/denom, 2)
        print(f'score is {v["score"]}')

    return results

def root_search(bad_terms, html):
    html = html.lower()
    results = {}
    for row in bad_terms:
        term = row[0]
        num_matches = html.count(term.lower().strip())
        if num_matches > 0:
            if term in results:
                results[term]['count'] += num_matches
            else:
                result = {'count': num_matches, 'reason': row[1], 'risk': int(row[2])}
                results[term] = result

    denom = 0
    scores = []
    numerator = 0
    for k,v in results.items():

        numerator += v['risk'] * WEIGHTING[v['risk']]
        denom += WEIGHTING[v['risk']]
    results['score'] = round(numerator/denom, 2)
    return results



