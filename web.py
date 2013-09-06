#!/usr/bin/env python

import eddy
import flask

app = flask.Flask(__name__)

@app.route('/perf/startup')
def startup():
    appname = flask.request.args.get('appname', '')
    name = eddy.loadApp(appname)
    return eddy.testApp(name)

if __name__ == '__main__':
    app.run(debug=True)
