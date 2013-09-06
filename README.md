eddy is an on-demand performance testing service intended for 3rd-party
packaged FirefoxOS apps.

Apps are downloaded from the Firefox Marketplace, and tested on a B2G phone
with Marionette installed, right now a single unagi running:
https://pvtbuilds.mozilla.org/pub/mozilla.org/b2g/nightly/mozilla-b2g18-unagi-eng/

Install:
  # create a virtualenv and activate it
  virtualenv -p python2.6 env
  . env/bin/activate

Run commandline/dev tool:
  # make sure adb is on your path
  export PATH=$PATH:`pwd`/android-platform-tools
  ./eddy appname

You can run ```eddy``` with no arguments (or --help) to see all options:
  ./eddy --help

Or, run the web service (in standalone/dev mode):
  ./web.py

See ```eddy.wsgi``` if you want to run this from a WSGI server (Apache, etc)

The web service will push tasks into a queue using celery, which supports
multiple backends. To actually run the test jobs on the phone, you must
run at least one celery worker:
  # make sure adb is on your path
  export PATH=$PATH:`pwd`/android-platform-tools
  celery -A tasks worker --loglevel=info
