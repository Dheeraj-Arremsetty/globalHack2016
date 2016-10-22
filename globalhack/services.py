import importlib
import json
import os
# import math.ra
from flask import flash, jsonify, request, Response, redirect, render_template, url_for

from .db import Database
from .errors import BadRequestError, InternalError, RecordNotFound, UnauthorizedError
from .needs import Needs

def register_services(app, prefix):
    BaseServices(app, prefix)

    @app.errorhandler(BadRequestError)
    @app.errorhandler(InternalError)
    @app.errorhandler(UnauthorizedError)
    @app.errorhandler(RecordNotFound)
    def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

class BaseServices:
    def __init__(self, app, prefix):
        self.session_users = {}
        self.app = app
        print '-' * 50

        self.app.add_url_rule(prefix + '/',
                              'root',
                              getattr(self, 'root'),
                              methods=['GET'])
        self.app.add_url_rule(prefix + '/food.html',
                              'food.html',
                              getattr(self, 'food_ui'),
                              methods=['GET'])
        self.app.add_url_rule(prefix + '/help.html',
                              'help.html',
                              getattr(self, 'help_ui'),
                              methods=['GET'])

        for endpoint in [ 'contact',
                          'about',
                          'login',
                          'needs',
                          'provider',
                          'providee',
                          'register',
                          'register_user',
                          'want_to_help',
                          'register_provider',
                          'register_user','food' ]:
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

    def register_for_help(self):
        params = self.getparams(request)
        name = params.get('name', None)
        zipcode = params.get('zipcode',  None)
        phone_number = params.get('phone_number',  None)

        if not name:
            flash('Name was not specified!', 'danger')
            return render_template('want_to_help.html')


        if not zipcode:
            flash('Zipcode was not specified!', 'danger')
            return render_template('want_to_help.html')

        if not phone_number:
            flash('Zipcode was not specified!', 'danger')
            return render_template('want_to_help.html')

        print 'Name: %s' % name
        # print 'Password: %s' % password

        Database().registerForHelp(name, zipcode, phone_number)
        return redirect(url_for('root'))



    def want_to_help(self):
        return render_template('want_to_help.html')

    def root(self):
        return render_template('home.html')

    def food_ui(self):
        return render_template('food.html')

    def help_ui(self):
        return render_template('needHelp.html')

    def register_user(self):
        return render_template('register_user.html')

    def about(self):
        return render_template('about.html')

    def contact(self):
        return render_template('contact.html')

    def need_item_id(self, need_id, need_item_id):
        import_module = 'globalhack.api.need.%s' % need_id
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

    def food(self):
        list = []
        print "In food function"
        for i in range(5):
            list.append({"name": "name"+str(i), "address": "address"+str(1), "number_of_meals": str(i), "available_till": "MM-DD-YYYY"})
        return jsonify({ 'result': list })

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

    def register_provider(self):
        params = self.getparams(request)
        name = params.get('name', None)
        address = params.get('address',  None)
        zipcode = params.get('zipcode',  None)
        phone_number = params.get('phone_number',  None)

        if not name:
            flash('Name was not specified!', 'danger')
            return render_template('want_to_help.html')

        if not address:
            flash('Address was not specified!', 'danger')
            return render_template('want_to_help.html')

        if not zipcode:
            flash('Zipcode was not specified!', 'danger')
            return render_template('want_to_help.html')

        if not phone_number:
            flash('Zipcode was not specified!', 'danger')
            return render_template('want_to_help.html')

        print 'Name: %s' % name
        # print 'Password: %s' % password

        Database().createProvider(name, address, zipcode, phone_number)
        return redirect(url_for('root'))

    def register(self):
        params = self.getparams(request)
        username = params.get('username', None)
        password = params.get('password',  None)
        confirm_password = params.get('confirm_password',  None)

        if password == None:
            flash('Password was not specified!', 'danger')
            return render_template('register_user.html')

        if password != confirm_password:
            flash('Passwords did not match!', 'danger')
            return render_template('register_user.html')

        print 'Username: %s' % username
        # print 'Password: %s' % password

        uid = Database().createUser(username, password)
        return redirect(url_for('root'))

    def getparams(self, request):
        return request.form if (request.method == 'POST') else request.args
