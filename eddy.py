#!/usr/bin/env python

import argparse
import settings
import logging
import requests
import subprocess
import tempfile

BASEURL='https://marketplace.firefox.com/api/v1/apps/app'
#BASEURL='http://localhost:8000/api/v1/apps/app'
ADB_PATH='/Users/rhelmer/src/android-platform-tools/'

def loadApp(appname):
    market_request = requests.get('%s/%s' % (BASEURL, appname))
    logging.info('requesting app manifest from marketplace')
    manifest_url = market_request.json()['manifest_url']
    name = market_request.json()['name']
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
        # TODO actually load onto phone...
        logging.info('TODO actually load %s onto phone...' % temp.name)

    return name

def testApp(appname):
    logging.info('forward port for marionette')
    subprocess.check_call(['adb', 'forward','tcp:2828', 'tcp:2828'])
    logging.info('run b2gperf with app: %s' % appname)
    # FIXME should this be importing b2gperf directly instead?
    # TODO switch to subprocess.check_output on python2.7+
    p = subprocess.Popen(['env/bin/python', 'env/bin/b2gperf', appname,
                          '--settle-time=%s' % settings.SETTLE_TIME,
                          '--iterations=%s' % settings.ITERATIONS,
                          '--dz-project=%s' % settings.DZ_PROJECT,
                          '--dz-branch=%s' % settings.DZ_BRANCH,
                          '--dz-key=%s' % settings.DZ_KEY,
                          '--dz-secret=%s' % settings.DZ_SECRET],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    returncode = p.returncode

    if returncode == 0:
        return out
    else:
        raise Exception('b2gperf failed, return code: %s stdout/err: %s / %s'
                        % (returncode, out, err))

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('started')

    parser = argparse.ArgumentParser(
        description='perf test third-party packaged FirefoxOS apps')
    parser.add_argument('appname', help='name of app to test')
    parser.add_argument('--download-only', const=True, nargs='?',
                        help='download app from marketplace but do not test')
    parser.add_argument('--test-only', const=True, nargs='?',
                        help='test app but do not download from marketplace')
    args = parser.parse_args()

    if args.download_only:
        loadApp(args.appname)
    elif args.test_only:
        testApp(args.appname)
    else:
        name = loadApp(args.appname)
        testApp(name)

if __name__ == '__main__':
    main()
