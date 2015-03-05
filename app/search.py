from Queue import Queue, Empty
from collections import defaultdict
from threading import Thread
import time
from HTMLParser import HTMLParser
import re
from flask import render_template, request, redirect, url_for
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
    return redirect(url_for('hello'))

def _fetch_results(query):
    query = _format_query(query)
    q = Queue()

    threads = [Thread(target = get_google_results, args = (query, q)),
               Thread(target = get_bing_results, args = (query, q)),
               Thread(target = get_yahoo_results, args = (query, q))]

    for t in threads:
        t.start()
        t.join()
    return queue_get_all(q)


def _format_query(query):
    query = re.sub(r'[^\w\s]', ' ', query).lower()
    tokens = re.split(r'\s+', query)
    tokens = [token.strip() for token in tokens]
    return '+'.join(tokens)


def _merge(candidates):
    retrieved_docs = []
#    url_set = set()
    for doc in candidates:
#        if doc['link'] not in url_set:
        retrieved_docs.append(doc)
#            url_set.add(doc['link'])

    results = defaultdict(list)
    for doc in retrieved_docs:
        results[doc['source']].append(doc)
    return results


def queue_get_all(q):
    items = []
    max_cnt = 30
    cnt = 0
    while cnt < max_cnt:
        try:
            items.append(q.get(True, 2))
            cnt += 1
        except Empty:
            break
    return items
