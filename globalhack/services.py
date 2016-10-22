import json
import os

from flask import jsonify, request, Response, redirect

from .db import Database
from .errors import BadRequestError, UnauthorizedError

def register_services(app, prefix):
    BaseServices(app, prefix)

class BaseServices:
    def __init__(self, app, prefix):
        self.session_users = {}
        self.app = app
        print '-' * 50
        print '                        Getting Elastic Config'
        # self.connections = self.app.config['Managers'].get('Database').connections
        # db = self.app.config['Managers'].get('Database')
        # self.connections = db.connections
        # con_config = self.connections['rca'][0]
        # con_config['http_auth'] = (con_config['user'], con_config['password'])
        # self.parthealth = 'rca-rca'
        # self.rcaMap = 'rca-rca_map'
        # self.reflexChain = 'rca-reflex_chain'
        # self.keymap = {
        #     'Data Models': 'file_type',
        #     'Systems': 'source',
        #     'TSL Gap': 'metric_tslgap',
        #     'DOS': 'metric_dos',
        #     'PAL': 'metric_pal',
        #     'FAC': 'metric_fac',
        #     'OTD': 'metric_otd'
        # }
        print '-' * 50
        print '                        Elastic is Stretching'
        print '-' * 50
        print '                        Register MDMDQ API'
        print '-' * 50
        #       ----------------------------------------------------------------------------
        #                                 MDMDQ Services
        #       ----------------------------------------------------------------------------
        #         self.app.add_url_rule(WSGI_PATH_PREFIX + '/services/dates', 'dates', self.dates, methods=['POST'])
        for endpoint in [ 'login', 'needs' ]:
            self.app.add_url_rule(prefix + '/%s' % endpoint,
                                  endpoint,
                                  getattr(self, endpoint),
                                  methods=['POST', 'GET'])

    def needs(self):
        return False

    def login(self):
        print "I am comming to backendddddddddd"
        params = self.getparams(request)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
        else:

            username = params.get('username', None)
            password = params.get('password',  None)

        print 'Username: %s' % username
        print 'Password: %s' % password

        uid = Database().validateUser(username, password)
        if uid == None:
            raise UnauthorizedError('Unauthorized', status_code=401)

        return jsonify({ 'token': uid })

    def register(self):
        params = self.getparams(request)
        username = params.get('username', None)
        password = params.get('password',  None)
        confirm_password = params.get('confirm_password',  None)

        if password == None:
            raise BadRequestError('Password is not specified!', status_code=400)

        if password != confirm_password:
            raise BadRequestError('Passwords do not match!', status_code=400)

        print 'Username: %s' % username
        # print 'Password: %s' % password

        uid = Database().validateUser(username, password)

        return jsonify({ 'token': uid })

    def getparams(self, request):
        return request.form if (request.method == 'POST') else request.args
