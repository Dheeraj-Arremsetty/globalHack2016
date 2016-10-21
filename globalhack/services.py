import json
import os

from flask import jsonify, request, Response, redirect

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
        for endpoint in [ 'giveJson', 'add']:
            self.app.add_url_rule(prefix + '/services/%s' % endpoint,
                                  endpoint,
                                  getattr(self, endpoint),
                                  methods=['POST', 'GET'])

    def giveJson(self):
        _d = {i:i*'S' for i in xrange(55)}
        return jsonify(_d)

    def getparams(self, request):
        return request.form if (request.method == 'POST') else request.args

    def add(self):
        #http://0.0.0.0:5050/globalhack/services/add?a=100&b=200
        params = self.getparams(request)
        a = params.get('a', 5)
        b = params.get('b', 10)
        # print params
        # a = 5
        # b= 10
        c = int(a) + int(b)
        return str(c)
