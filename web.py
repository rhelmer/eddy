#!/usr/bin/env python

import flask
import json
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
    if not task_id:
        result = tasks.celery.control.inspect()
    else:
        result = tasks.celery.AsyncResult(task_id)

    return flask.Response(json.dumps(result.scheduled()),
                          mimetype='application/json')

if __name__ == '__main__':
    app.run()
