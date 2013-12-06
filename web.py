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

# provide a route for non-celery consumers to pop a task
@app.route('/perf/consume', methods=['GET'])
def consume():
    return tasks.consume_one()

@app.route('/perf/status')
def status():
    task_id = flask.request.args.get('task_id', '')
    appname = flask.request.args.get('appname', '')
    result = {}
    if task_id:
        result = tasks.celery.AsyncResult(task_id).status
    elif appname:
        result = {'queued': False}
        active = tasks.celery.control.inspect().active()
        reserved = tasks.celery.control.inspect().reserved()
        for queue in (reserved, active):
            for key in queue:
                for job in queue[key]:
                    if appname in job['args']:
                        result['queued'] = True

    return flask.Response(json.dumps(result),
                          mimetype='application/json')

if __name__ == '__main__':
    app.run()
