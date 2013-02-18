import re
import gevent
from flask import render_template, request
from app import app
from app.engines import get_google_results, get_bing_results

@app.route('/')
def hello():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    if len(query.strip()) > 0:
        candidates = _fetch_results(query)
        results = _merge(candidates)
        return render_template('results.html',
                               results = results)

def _fetch_results(query):
    query = _format_query(query)
    #TODO: use twisted or tornado
    jobs = [gevent.spawn(get_google_results, query), gevent.spawn(get_bing_results, query)]
    gevent.joinall(jobs)
    results = [job.get() for job in jobs]
    return results

def _format_query(query):
    query = re.sub(r'[^\w\s]', ' ', query).lower()
    tokens = re.split(r'\s+', query)
    tokens = [token.strip() for token in tokens]
    return '+'.join(tokens)

def _merge(candidates):
    retrieved_docs = candidates[0]
    baseline_urls = set([doc['link'] for doc in retrieved_docs])

    for docs in candidates[1:]:
        for doc in docs:
            if doc['link'] not in baseline_urls:
                retrieved_docs.append(doc)
    return retrieved_docs
