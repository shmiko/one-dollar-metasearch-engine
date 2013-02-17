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
    except (HttpError, HttpLib2Error):
        return []

def get_bing_results(query):
    url = "http://www.bing.com/search?q=%s" % query
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        results = BeautifulSoup(res.text).find("div", {"id": "results"}).findAll('li', {'class': 'sa_wr'})

        doc = [{'link': result.find('div', {'class': 'sb_meta'}).find('cite').getText(),
                'title': result.find('div', {'class': 'sb_tlst'}).getText(),
                'snippet': result.find('p').getText()}
               for result in results]
        return doc
    return []
