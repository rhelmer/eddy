#!/usr/bin/env python

import argparse
import settings
import logging
import requests
import subprocess
import tempfile
import json

BASEURL='https://marketplace.firefox.com/api/v1/apps/app'
#BASEURL='http://localhost:8000/api/v1/apps/app'
ADB_PATH='/Users/rhelmer/src/android-platform-tools/'

def loadApp(app_slug):
    market_request = requests.get('%s/%s' % (BASEURL, app_slug))
    logging.info('requesting app manifest from marketplace')
    manifest_url = market_request.json()['manifest_url']
    app_name = market_request.json()['name']
    market_request.close()

    manifest_request = requests.get(manifest_url)
    logging.info('requesting app url from manifest')
    app_url = manifest_request.json()['package_path']
    manifest_request.close()

    logging.info('create appdir on device')
    subprocess.check_call(['adb', 'shell', 'mkdir',
        '/data/local/webapps/%s' % app_slug])

    with tempfile.NamedTemporaryFile() as temp:
        for chunk in manifest_request.iter_content(chunk_size=1024):
            if chunk:
                temp.write(chunk)
                temp.flush()
        logging.info('add location_path to webapp.manifest')
        with open(temp.name, 'r+') as f:
            manifest_json = json.loads(f.read())
            if 'launch_path' not in manifest_json:
                manifest_json['launch_path'] = '/index.html'
                f.seek(0)
                f.write(json.dumps(manifest_json))
        logging.info('load manifest onto device')
        subprocess.check_call(['adb', 'push', temp.name,
            '/data/local/webapps/%s/manifest.webapp' % app_slug])

    app_request = requests.get(app_url, stream=True)
    logging.info('downloading app')
    with tempfile.NamedTemporaryFile() as temp:
        for chunk in app_request.iter_content(chunk_size=1024):
            if chunk:
                temp.write(chunk)
                temp.flush()
        logging.info('load app onto device')
        subprocess.check_call(['adb', 'push', temp.name,
            '/data/local/webapps/%s/application.zip' % app_slug])

    subprocess.check_call(['adb', 'pull',
        '/data/local/webapps/webapps.json', '.'])
    with open('webapps.json', 'r') as f:
        webapps = json.loads(f.read())

    if app_slug in webapps:
        del webapps[app_slug]

    localId = max([v['localId'] for k,v in webapps.iteritems()]) + 1

    webapps[app_slug] = {
        'origin': 'app://%s' % app_slug,
        'installOrigin': 'app://%s' % app_slug,
        'manifestURL': 'app://%s/manifest.webapp' % app_slug,
        'appStatus': 1,
        'installTime': 1379012730464,
        'installState': 'installed',
        'removable': True,
        'id': app_slug,
        'basePath': '/data/local/webapps',
        'localId': localId,
        'name': app_name,
    }

    with open('webapps-new.json', 'w') as f:
        f.write(json.dumps(webapps))

    subprocess.check_call(['adb', 'push', 'webapps-new.json',
        '/data/local/webapps/webapps.json'])

    return app_name

def testApp(app_name, app_slug):
    logging.info('forward port for marionette')
    subprocess.check_call(['adb', 'forward','tcp:2828', 'tcp:2828'])
    logging.info('run b2gperf with app: %s' % app_name)
    # FIXME should this be importing b2gperf directly instead?
    # TODO switch to subprocess.check_output on python2.7+
    p = subprocess.Popen(['env/bin/python', 'env/bin/b2gperf', app_name,
                          '--settle-time=%s' % settings.SETTLE_TIME,
                          '--iterations=%s' % settings.ITERATIONS,
                          '--dz-project=%s' % settings.DZ_PROJECT,
                          '--dz-branch=%s' % settings.DZ_BRANCH,
                          '--dz-test-suite=%s' % app_slug,
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
    parser.add_argument('--load-only', action='store_true',
        help='load app from marketplace onto device but do not test')
    parser.add_argument('--test-only', action='store_true',
        help='test already-installed app')
    args = parser.parse_args()

    if args.load_only:
        loadApp(args.appname)
    elif args.test_only:
        testApp(args.appname)
    else:
        app_name, app_slug = loadApp(args.appname)
        testApp(app_name, app_slug)

if __name__ == '__main__':
    main()
