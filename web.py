#!/usr/bin/env python

import flask
import tasks

app = flask.Flask(__name__)
app.debug = True

@app.route('/perf/startup')
def startup():
    appname = flask.request.args.get('appname', '')
    task_id = tasks.perftest.delay(appname)
    return 'queued as task ID: %s' % task_id

@app.route('/perf/status')
def status():
    task_id = flask.request.args.get('task_id', '')
    return tasks.celery.AsyncResult(task_id).state

if __name__ == '__main__':
    app.run()
