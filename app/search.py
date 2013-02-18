import time
import re
import gevent
from flask import render_template, request
from app import app
from app.engines import get_google_results, get_bing_results, get_yahoo_results

@app.route('/')
def hello():
    return render_template('search.html')


@app.route('/search', methods = ['POST'])
def search():
    query = request.form['query']
    if len(query.strip()) > 0:
        t0 = time.time()
        candidates = _fetch_results(query)
        results = _merge(candidates)
        t1 = time.time()
        print "Query Execution Time: %f" % (t1 - t0)
        return render_template('results.html',
                               results = results)


def _fetch_results(query):
    query = _format_query(query)
    #TODO: use twisted or tornado
    jobs = [gevent.spawn(get_google_results, query),
            gevent.spawn(get_bing_results, query),
            gevent.spawn(get_yahoo_results, query)]
    gevent.joinall(jobs)
    candidates = [job.get() for job in jobs]
    return candidates


def _format_query(query):
    query = re.sub(r'[^\w\s]', ' ', query).lower()
    tokens = re.split(r'\s+', query)
    tokens = [token.strip() for token in tokens]
    return '+'.join(tokens)


def _merge(candidates):
    retrieved_docs = candidates[0]
    url_set = set([doc['link'] for doc in retrieved_docs])

    for docs in candidates[1:]:
        for doc in docs:
            if doc['link'] not in url_set:
                retrieved_docs.append(doc)
                url_set.add(doc['link'])

    return retrieved_docs
