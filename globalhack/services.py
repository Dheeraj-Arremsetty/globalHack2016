import importlib
import json
import os

from flask import jsonify, request, Response, redirect, render_template

from .db import Database
from .errors import BadRequestError, InternalError, RecordNotFound, UnauthorizedError
from .needs import Needs

def register_services(app, prefix):
    BaseServices(app, prefix)

class BaseServices:
    def __init__(self, app, prefix):
        self.session_users = {}
        self.app = app
        print '-' * 50
        for endpoint in [ 'contact',
                          'about',
                          'login',
                          'needs',
                          'provider',
                          'providee',
                          'register' ]:
            self.app.add_url_rule(prefix + '/%s' % endpoint,
                                  endpoint,
                                  getattr(self, endpoint),
                                  methods=['POST', 'GET'])

        self.app.add_url_rule(prefix + '/need/<need_id>',
                              'need',
                              getattr(self, 'need'),
                              methods=['POST', 'GET'])

        self.app.add_url_rule(prefix + '/need/<need_id>/<need_item_id>',
                              'need_item_id',
                              getattr(self, 'need_item_id'),
                              methods=['GET', 'DELETE', 'PUT'])


    def about(self):
        return render_template('about.html')

    def contact(self):
        return render_template('contact.html')

    def need_item_id(self, need_id, need_item_id):
        import_module = 'globalhack.need.%s' % need_id
        try:
            need_module = importlib.import_module(import_module)
        except ImportError:
            raise InternalError('No need module found for "%s"!' % need_id, status_code=400)

        need_class = getattr(need_module,need_id.title())

        resp = Response(response=getattr(need_class(),request.method.lower())(need_item_id),
                                 status=200,
                                 mimetype="application/json")
        return(resp)

    def need(self, need_id):
        import_module = 'globalhack.need.%s' % need_id
        try:
            need_module = importlib.import_module(import_module)
        except ImportError:
            raise InternalError('No need module found for "%s"!' % need_id, status_code=400)

        need_class = getattr(need_module,need_id.title())

        resp = Response(response=getattr(need_class(),request.method.lower())(),
                                 status=200,
                                 mimetype="application/json")
        return(resp)

    def providee(self):
        params = self.getparams(request)
        uid = params.get('providee_id', None)

        print 'Uid: %s' % uid
        if not uid:
            print 'Missing uid!'
            raise RecordNotFound('Missing uid!', status_code=403)

        user = Database().getUserInfo(uid)
        if not user:
            raise RecordNotFound('User not found!', status_code=403)

        providee_of = []
        if 'providee_of' in user:
            providee_of = user['providee_of']

        return jsonify({ 'result': providee_of })

    def provider(self):
        params = self.getparams(request)
        uid = params.get('provider_id', None)

        print 'Uid: %s' % uid
        if not uid:
            print 'Missing uid!'
            raise RecordNotFound('Missing uid!', status_code=403)

        user = Database().getUserInfo(uid)
        if not user:
            raise RecordNotFound('User not found!', status_code=403)

        provider_of = []
        if 'provider_of' in user:
            provider_of = user['provider_of']

        return jsonify({ 'result': provider_of })

    def needs(self):
        return jsonify({ 'result': Needs.get_needs() })

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
