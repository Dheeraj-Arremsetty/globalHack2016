#!/usr/bin/env python2.7

import flask
import os
import pymongo
import sys

from flask import jsonify, redirect, url_for

from globalhack.errors import BadRequestError, RecordNotFound, UnauthorizedError
from globalhack.services import register_services


class Config():
    def __init__(self, app, prefix):
        self.app = app
        # register managers and then services
        print '-' * 50
        print '                   WSGIPrefix set to %s' % prefix
        self.srvs = register_services(app, prefix)

# create application
application = flask.Flask(__name__, static_url_path='/static')
application.config['CONFIG_PATH'] = os.path.join(os.path.basename(__file__), "config/")

@application.route('/globalhack')
def index():
    print 'Index entry'
    return "<b>hello</b>"

@application.route('/')
def root():
    print 'Root entry'
    return redirect('home.html')



@application.errorhandler(UnauthorizedError)
def handle_unauthorized_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(BadRequestError)
def handle_bad_request_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(RecordNotFound)
def handle_bad_request_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    Config(application, '')
    dport = int(sys.argv[1]) if len(sys.argv) > 1 else 5050

    application.run(host='0.0.0.0',
                    port=dport,
                    debug=True,
                    use_reloader=True,
                    processes=100,
                    static_files={'/':'static'})
