#!/usr/bin/env python2.7

import pymongo
import csv

# Connection to Mongo DB
conn = pymongo.MongoClient()
db = conn['cale']

apath = 'tools/Sample Dataset/'

def import_users():
    MAPPING = { 'source_db': 'Client',
                'target_db': 'users' }

    db[MAPPING['target_db']].drop()
    db[MAPPING['target_db']].create_index('username')

    reader = csv.DictReader(open(apath + MAPPING['source_db'] + '.csv'), delimiter=',')
    for row in reader:
        del row['']
        deletable_keys = []
        for column in row.keys():
            if row[column] == '':
                deletable_keys

        for column in deletable_keys:
            del row[column]

        row['username'] = row['First_Name'].lower() + row.get('Last_Name', '').lower()
        row['password'] = row['UUID']

#        print row
        db[MAPPING['target_db']].insert(row)

def import_addresses():
    MAPPING = { 'source_db': 'Enrollment',
                'target_db': 'users' }

    reader = csv.DictReader(open(apath + MAPPING['source_db'] + '.csv'), delimiter=',')
    for row in reader:
        if db[MAPPING['target_db']].find_one({'UserID': row['UserID']}):
            result = db[MAPPING['target_db']].update({'UserID': row['UserID']},
                                                     {"$set": { "street_address": row['LastPermanentStreet'],
                                                                "city": row['LastPermanentCity'],
                                                                "zip_code": row['LastPermanentZIP'],
                                                                "state": row['LastPermanentState'] }})

            print result


import_users()
import_addresses()
