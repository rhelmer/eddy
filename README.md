eddy is an on-demand performance testing service intended for 3rd-party
packaged FirefoxOS apps.

Apps are downloaded from the Firefox Marketplace, and tested on a B2G phone
with Marionette installed, right now a single unagi running:
https://pvtbuilds.mozilla.org/pub/mozilla.org/b2g/nightly/mozilla-b2g18-unagi-eng/

Install:
  # create a virtualenv and activate it
  virtualenv -p python2.6 env
  . env/bin/activate

Run:
  ./eddy appname

You can run ```eddy``` with no arguments (or --help) to see all options:
  ./eddy --help
