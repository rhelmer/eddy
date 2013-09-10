#!/usr/bin/env python

import flask
import tasks

app = flask.Flask(__name__)
app.debug = True

@app.route('/perf/startup', methods=['POST'])
def startup():
    appname = flask.request.form.get('appname', '')
    task_id = tasks.perftest.delay(appname)
    return '%s' % task_id

@app.route('/perf/status')
def status():
    task_id = flask.request.args.get('task_id', '')
    result = tasks.celery.AsyncResult(task_id)
    return 'Status: %s<pre>%s</pre>' % (result.status, result.result)

if __name__ == '__main__':
    app.run()
