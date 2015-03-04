import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

def get_google_results(query, queue):
    url = "http://www.google.com/search?q=%s" % query
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        results = BeautifulSoup(res.text, 'lxml').find_all('li', {'class': 'g'})
        print("results from google", results)
        for result in results:
            title = result.find('h3', {'class': 'r'}).getText()
            link = _format_google_url(result.find('h3', {'class': 'r'}).find('a', href = True)['href'])
            snippet_tag = result.find('span', {'class': 'st'})
            snippet = '' if snippet_tag is None else snippet_tag.getText()
            queue.put({'link': link, 'title': title, 'snippet': snippet, 'source': 'google'})


def get_bing_results(query, queue):
    url = "http://www.bing.com/search?q=%s" % query
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        results = BeautifulSoup(res.text, 'lxml').find("div", {"id": "results"}).find_all('li', {'class': 'sa_wr'})

        for result in results:
            title = result.find('div', {'class': 'sb_tlst'}).getText()
            link = _format_url(result.find('div', {'class': 'sb_tlst'}).find('a', href = True)['href'])
            snippet_tag = result.find('p')
            snippet = '' if snippet_tag is None else snippet_tag.getText()
            queue.put({'link': link, 'title': title, 'snippet': snippet, 'source': 'bing'})


def get_yahoo_results(query, queue):
    url = "http://search.yahoo.com/search?p=%s" % query
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        results = BeautifulSoup(res.text, 'lxml').find_all('div', {'class': 'res'})
        print("results from yahoo", results)
        for result in results:
            title = result.find('h3').getText()
            link = _format_url(result.find('h3').find('a', href = True)['href'])
            snippet_tag = result.find('div', {'class': 'abstr'})
            snippet = '' if snippet_tag is None else snippet_tag.getText()
            queue.put({'link': link, 'title': title, 'snippet': snippet, 'source': 'yahoo'})


def _format_url(url):
    return url.strip().rstrip('/')


def _format_google_url(url):
    if url.startswith('/'):
        return "http://www.google.com" + url
    else:
        return url.strip().rstrip('/')
