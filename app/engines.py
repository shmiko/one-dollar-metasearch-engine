from apiclient.errors import HttpError
from httplib2 import HttpLib2Error
import requests
from apiclient.discovery import build
from bs4 import BeautifulSoup

def get_google_results(query):
    try:
        google = build("customsearch", "v1", developerKey="AIzaSyA4bQ5NdaPpoJBVuC-cZatqCCdTvc570QE")
        res = google.cse().list(q=query, cx='017576662512468239146:omuauf_lfve').execute()
        return res['items']
    except (HttpError, HttpLib2Error, Exception):
        return []

def get_bing_results(query):
    url = "http://www.bing.com/search?q=%s" % query
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        results = BeautifulSoup(res.text, 'lxml').find("div", {"id": "results"}).find_all('li', {'class': 'sa_wr'})

        docs = []
        for result in results:
            title = result.find('div', {'class': 'sb_tlst'}).getText()
            link = result.find('div', {'class': 'sb_meta'}).find('cite').getText()
            snippet_tag = result.find('p')
            snippet = '' if snippet_tag is None else snippet_tag.getText()
            docs.append({'link': link, 'title': title, 'snippet': snippet})
        return docs
    return []

def get_yahoo_results(query):
    url = "http://search.yahoo.com/search?p=%s" % query
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        results = BeautifulSoup(res.text, 'lxml').find_all('div', {'class': 'res'})

        docs = []
        for result in results:
            title = result.find('h3').getText()
            link = result.find('h3').find('a', href=True)['href']
            snippet_tag = result.find('div', {'class':'abstr'})
            snippet = '' if snippet_tag is None else snippet_tag.getText()
            docs.append({'link': link, 'title': title, 'snippet': snippet})
        return docs
    return []
