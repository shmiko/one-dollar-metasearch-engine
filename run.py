#!env/bin/python
import os
import sys
from gevent.pywsgi import WSGIServer
from app import app

host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 5000))
http = WSGIServer((host, port), app)
print 'Running on http://%s:%d/' % (host, port)
try:
    http.serve_forever()
except KeyboardInterrupt:
    print 'Shutdown requested... exiting'
except Exception:
    raise
sys.exit(0)