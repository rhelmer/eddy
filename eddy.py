#!/usr/bin/env python

import logging
import requests
import subprocess
import tempfile

BASEURL='https://marketplace.firefox.com/api/v1/apps/app'
APPNAME='stopwatch-1'

def loadApp(appname):
    market_request = requests.get('%s/%s' % (BASEURL, appname))
    logging.info('requesting app manifest from marketplace')
    manifest_url = market_request.json()['manifest_url']
    market_request.close()

    manifest_request = requests.get(manifest_url)
    logging.info('requesting app url from manifest')
    app_url = manifest_request.json()['package_path']
    manifest_request.close()

    app_request = requests.get(app_url, stream=True)
    logging.info('downloading app')
    with tempfile.NamedTemporaryFile() as temp:
        for chunk in app_request.iter_content(chunk_size=1024):
            if chunk:
                temp.write(chunk)
                temp.flush()
        logging.info('FIXME load %s onto phone' % temp.name)

def testApp(appname):
    logging.info('forward port for marionette')
    subprocess.check_call(['adb', 'shell', 'forward', 'tcp:2828', 'tcp:2828'])
    logging.info('run b2gperf')
    subprocess.check_call(['env/bin/python', 'env/bin/b2gperf', appname])

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('started')
    # FIXME handle command-line args
    loadApp(APPNAME)
    testApp(APPNAME)

if __name__ == '__main__':
    main()
