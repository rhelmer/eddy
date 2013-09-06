#!/usr/bin/env python

import flask
import tasks

app = flask.Flask(__name__)
app.debug = True

@app.route('/perf/startup')
def startup():
    appname = flask.request.args.get('appname', '')
    uuid = tasks.perftest.delay(appname)
    return 'queued %s' % uuid

@app.route('/perf/work')
def work():
    worker_name = flask.request.args.get('name', '')
    return worker_name

if __name__ == '__main__':
    app.run()
