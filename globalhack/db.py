from pymongo import MongoClient

class Database(object):
    DATABASE_NAME = 'cale'

    def __init__(self):
        self.client = MongoClient()

    def validateUser(self, username, password):
        user = self.client[Database.DATABASE_NAME].users.find_one({ 'username': username })
        print(user)
        if not user:
            print 'User %s not found!' % username
            return None

        if 'password' not in user:
            print 'User %s has no password!' % username
            return None

        if user['password'] != password:
            print 'User %s login attempt did not match saved password!' % username
            return None

        return str(user['_id'])

    def getProviderInfo(self, provider_id):
        provider = self.client[Database.DATABASE_NAME].providers.find_one({ '_id': provider_id })
        print 'Provider: %s' % provider
        if not provider:
            print 'Provider %s not found!' % provider
            return None

        return provider

    def getProvideeInfo(self, providee_id):
        providee = self.client[Database.DATABASE_NAME].providees.find_one({ '_id': providee_id })
        print 'Providee: %s' % providee
        if not providee:
            print 'Providee %s not found!' % providee
            return None

        return providee
