from flask import render_template, request
import re
from app import app
from app.engines import get_google_results, get_bing_results

@app.route('/')
def hello():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    if len(query.strip()) > 0:
        results = _fetch_results(query)
        return render_template('results.html',
                               results = results)

def _fetch_results(query):
    query = _format_query(query)
    #TODO: fetch results in parallel
    google_results = get_google_results(query)
    bing_results =  get_bing_results(query)
    final = _merge(google_results, bing_results)
    return final

def _format_query(query):
    query = re.sub(r'[^\w\s]', ' ', query).lower()
    tokens = re.split(r'\s+', query)
    tokens = [token.strip() for token in tokens]
    return '+'.join(tokens)

def _merge(google_results, bing_results):
    results = google_results
    links = [google_result['link'] for google_result in google_results]
    google_urls = set(links)
    for bing_result in bing_results:
        if bing_result['link'] not in google_urls:
            results.append(bing_result)
    return results
