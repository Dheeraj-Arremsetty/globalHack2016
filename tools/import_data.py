#!/usr/bin/env python2.7

import pymongo
import csv

# Connection to Mongo DB
conn = pymongo.MongoClient()
db = conn.cale_users_data

# 1. Put in terminal to create collections
# use cale_users_data
#db.createCollection("Client")
#db.createCollection("Disabilities")
#db.createCollection("EmploymentEducation")
#db.createCollection("Enrollment")
#db.createCollection("Exit")
#db.createCollection("Funder")
#db.createCollection("HealthAndDV")
#db.createCollection("IncomeBenefits")
#db.createCollection("Services")

## 2. Change path to where dataset csvs are saved
apath = 'Sample Dataset/'

DATABASES = [ 'Services',
              'Client',
              'Disabilities',
              'EmploymentEducation',
              'Enrollment',
              'Exit',
              'Funder',
              'HealthAndDV',
              'IncomeBenefits',
              'Services' ]

for database_name in DATABASES:
    reader = csv.DictReader(open(apath + database_name + '.csv'), delimiter=',')
    for row in reader:
        result = db[database_name].insert(row)
        print result
