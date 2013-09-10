eddy is an on-demand performance testing service intended for 3rd-party
packaged FirefoxOS apps.

Apps are downloaded from the Firefox Marketplace, and tested on a B2G phone
with Marionette installed, right now a single unagi running:
https://pvtbuilds.mozilla.org/pub/mozilla.org/b2g/nightly/mozilla-b2g18-unagi-eng/

Install:
```
# create a virtualenv and activate it
virtualenv -p python2.6 env
. env/bin/activate
```

Run commandline/dev tool:

```
# make sure adb is on your path
export PATH=$PATH:`pwd`/android-platform-tools
./eddy appname
```

You can run ```eddy``` with no arguments (or --help) to see all options:

```
./eddy --help
```

Or, run the web service (in standalone/dev mode):

```
./web.py
```

See ```eddy.wsgi``` if you want to run this from a WSGI server (Apache, etc)

Jobs can be queued by passing the name of the application in the marketplace,
such as:

curl -X POST -d 'appname=stopwatch-1' 'http://localhost:5000/perf/startup'

A task ID is returned, which can be used to query the status of a job:

http://localhost:5000/perf/status?task_id=84006869-3d4e-4a70-a291-6146fa030200

The web service will push tasks into a queue using celery, which supports
multiple backends. To actually run the test jobs on the phone, you must
configure celery (see tasks.py) and make sure it can connect to a supported
backend.

By default, eddy will try to connect to a local RabbitMQ install.
Mac (homebrew) users can install it like this:

```
brew install rabbitmq
```

Then run at least one celery worker:

```
# make sure adb is on your path
export PATH=$PATH:`pwd`/android-platform-tools
# NOTE - one job per worker (i.e. per phone), and send events
celery -A tasks worker -c 1 -E --loglevel=info
```
