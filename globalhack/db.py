from bson import ObjectId
from bson.json_util import dumps

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

    def getUserInfo(self, uid):
        if not uid:
            print 'User %s not specified!' % user
            return None

        user = self.client[Database.DATABASE_NAME].users.find_one({ '_id': ObjectId(uid) })
        print 'User: %s' % uid
        if not user:
            print 'User "%s" not found!' % user
            return None

        return user

    def getProvidedNeedsFor(self, need_id):
        collection_name = 'need_%s' % need_id
        print 'Trying to list collection: %s' % collection_name

        if collection_name not in self.client[Database.DATABASE_NAME].collection_names():
            print 'Nothing found in collection %s' % collection_name
            return dumps({'result': [] })

        return dumps({'result': self.client[Database.DATABASE_NAME][collection_name].find()})
