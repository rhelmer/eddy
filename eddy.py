#!/usr/bin/env python

import logging
import requests
import tempfile

BASEURL='https://marketplace.firefox.com/api/v1/apps/app'
APPNAME='stopwatch-1'

def loadApp():
    market_request = requests.get('%s/%s' % (BASEURL, APPNAME))
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

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('started')
    loadApp()

if __name__ == '__main__':
    main()
