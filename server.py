#!/usr/bin/env python2.7

import flask
import os
import sys

from flask import redirect, url_for

from globalhack.services import register_services


WSGI_PATH_PREFIX = ''

class Config():
    def __init__(self,app,WSGI_PATH_PREFIX):
        self.app = app
        # register managers and then services
        print'----------------------------------------------------------------------------'
        print '                   WSGIPrefix set to %s'%WSGI_PATH_PREFIX
        self.srvs = register_services(app, WSGI_PATH_PREFIX)

# create application
application = flask.Flask(__name__)
application.config['CONFIG_PATH'] = os.path.join(os.path.basename(__file__), "config/")
cfg = None

@application.route(WSGI_PATH_PREFIX + '/globalhack')
def index():
    print 'Index entry'
    return "<b>hello</b>"

def set_wsgi_prefix(prefix='/'):
    print 'setWsgi entry'
    WSGI_PATH_PREFIX = prefix
    cfg = Config(application, WSGI_PATH_PREFIX)

@application.route(WSGI_PATH_PREFIX + '/')
def root():
    print 'Root entry'
    return redirect(url_for('index'))

if __name__ == '__main__':
    WSGI_PATH_PREFIX = '/globalhack'
    cfg = Config(application, WSGI_PATH_PREFIX)
    dport = int(sys.argv[1]) if len(sys.argv) > 1 else 5050

    application.run(host='0.0.0.0',
                    port=dport,
                    debug=True,
                    use_reloader=True,
                    processes=100,
                    static_files={'/':'static'})
else:
    cfg = Config(application, WSGI_PATH_PREFIX)
