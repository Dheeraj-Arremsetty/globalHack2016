#!/usr/bin/env python2.7

import flask
import os
import pymongo
import sys

from flask import jsonify, redirect, render_template, url_for

from globalhack.errors import BadRequestError, InternalError, RecordNotFound, UnauthorizedError
from globalhack.services import register_services


class Config():
    def __init__(self, app, prefix):
        self.app = app
        self.srvs = register_services(app, prefix)

# create application
application = flask.Flask(__name__, static_url_path='/static')
application.config['CONFIG_PATH'] = os.path.join(os.path.basename(__file__), "config/")
application.config['FOOTER'] = '(c) 2016'
application.config['TITLE'] = 'Cale | Care and Compassion at Your Fingertips'

@application.route('/globalhack')
def index():
    print 'Index entry'
    return "<b>hello</b>"

@application.route('/')
def root():
    print 'Root entry'
    return render_template('home.html')

@application.errorhandler(BadRequestError)
@application.errorhandler(InternalError)
@application.errorhandler(UnauthorizedError)
@application.errorhandler(RecordNotFound)
def handle_error(error):
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
