import array

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

    def createUser(self, username, password):
        return str(self.client[Database.DATABASE_NAME].users.insert_one({ 'username': username, 'password': password }).inserted_id)

    def getVolunteerCount(self):
        return self.client[Database.DATABASE_NAME].providers.count()

    def getConnectionCount(self):
        return self.client[Database.DATABASE_NAME].providee.count()

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

    def createProvider(self, name, address, zipcode, phone_number,createProvider):
        id = str(self.client[Database.DATABASE_NAME].providers.insert_one({ 'name': name,'address': address, 'zipcode': zipcode, 'phone_number': phone_number,'willing_to_provide':createProvider }).inserted_id)
        self.client[Database.DATABASE_NAME].providers.create_index("zipcode")
        return id

    def registerForHelp(self, name, zipcode, phone_number):
        return str(self.client[Database.DATABASE_NAME].providee.insert_one({ 'name': name,'zipcode': zipcode, 'phone_number': phone_number }).inserted_id)

    def findProvidersWithZipcodes(self, zipcodes, needs = None):
        query = { 'zipcode': { "$in" : zipcodes }}
        if needs != None and len(needs) > 0:
            query['willing_to_provide'] = { "$in" : zipcodes }

        return self.client[Database.DATABASE_NAME].providers \
                   .find(query).limit(5)

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

    def getProvidedNeedsFor(self, need_id, need_item_id=None):
        collection_name = 'need_%s' % need_id
        print 'Trying to list collection: %s' % collection_name

        if not need_item_id:
            if collection_name not in self.client[Database.DATABASE_NAME].collection_names():
                print 'Nothing found in collection %s' % collection_name
                return dumps({ 'result': [] })

            return dumps({'result': self.client[Database.DATABASE_NAME][collection_name].find()})
        print 'Trying to get record "%s" for "%s"' % (need_item_id, collection_name)
        if collection_name not in self.client[Database.DATABASE_NAME].collection_names():
            raise RecordNotFound('Cannot find record "%s" for "%s"' % (need_item_id, collection_name))

        item = self.client[Database.DATABASE_NAME][collection_name].find({ '_id': ObjectId(need_item_id)})
        return dumps({ 'result': item })

    def getProvidersDetails(self):
        user = self.client[Database.DATABASE_NAME].providers.find()
        print "#"*30
        print user
        print "#" * 30
        _list = []
        for d in user:
            _list.append(d)
        return _list

