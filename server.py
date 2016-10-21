#!/usr/bin/env python2.7

import flask
import os
import sys

from flask import redirect, url_for

from globalhack.services import register_services


class Config():
    def __init__(self, app, prefix):
        self.app = app
        # register managers and then services
        print '-' * 50
        print '                   WSGIPrefix set to %s' % prefix
        self.srvs = register_services(app, prefix)

# create application
application = flask.Flask(__name__)
application.config['CONFIG_PATH'] = os.path.join(os.path.basename(__file__), "config/")

@application.route('/globalhack')
def index():
    print 'Index entry'
    return "<b>hello</b>"

@application.route('/')
def root():
    print 'Root entry'
    return redirect(url_for('index'))

if __name__ == '__main__':
    Config(application, '/globalhack')
    dport = int(sys.argv[1]) if len(sys.argv) > 1 else 5050

    application.run(host='0.0.0.0',
                    port=dport,
                    debug=True,
                    use_reloader=True,
                    processes=100,
                    static_files={'/':'static'})
