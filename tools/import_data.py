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
apath = '/Users/eileenschweiss/Desktop/Sample Dataset/'


# 3. Run
reader = csv.DictReader(open(apath + 'Services' + '.csv'), delimiter=',')
for row in reader:
    result = db.Services.insert(row)
    print result


reader = csv.DictReader(open(apath + 'Client' + '.csv'), delimiter=',')
for row in reader:
    result = db.Client.insert(row)
    print result


reader = csv.DictReader(open(apath + 'Disabilities' + '.csv'), delimiter=',')
for row in reader:
    result = db.Disabilities.insert(row)
    print result


reader = csv.DictReader(open(apath + 'EmploymentEducation' + '.csv'), delimiter=',')
for row in reader:
    result = db.EmploymentEducation.insert(row)
    print result


reader = csv.DictReader(open(apath + 'Enrollment' + '.csv'), delimiter=',')
for row in reader:
    result = db.Enrollment.insert(row)
    print result


reader = csv.DictReader(open(apath + 'Exit' + '.csv'), delimiter=',')
for row in reader:
    result = db.Exit.insert(row)
    print result


reader = csv.DictReader(open(apath + 'Funder' + '.csv'), delimiter=',')
for row in reader:
    result = db.Funder.insert(row)
    print result


reader = csv.DictReader(open(apath + 'HealthAndDV' + '.csv'), delimiter=',')
for row in reader:
    result = db.HealthAndDV.insert(row)
    print result

reader = csv.DictReader(open(apath + 'IncomeBenefits' + '.csv'), delimiter=',')
for row in reader:
    result = db.IncomeBenefits.insert(row)
    print result





