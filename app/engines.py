import urllib
from apiclient.discovery import build
from bs4 import BeautifulSoup

def get_google_results(query):
    google = build("customsearch", "v1", developerKey="AIzaSyA4bQ5NdaPpoJBVuC-cZatqCCdTvc570QE")
    res = google.cse().list(q=query, cx='017576662512468239146:omuauf_lfve').execute()
    return res['items']

def get_bing_results(query):
    url = "http://www.bing.com/search?q=%s" % query
    doc = urllib.urlopen(url).read()
    results = BeautifulSoup(doc).find("div", {"id": "results"}).findAll('li', {'class': 'sa_wr'})

    res = [{'link': result.find('div', {'class': 'sb_meta'}).find('cite').getText(),
            'title': result.find('div', {'class': 'sb_tlst'}).getText(),
            'snippet': result.find('p').getText()}
           for result in results]
    return res
