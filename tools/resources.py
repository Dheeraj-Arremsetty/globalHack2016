#!/usr/bin/env python2.7

import pymongo
import csv

# Connection to Mongo DB
conn = pymongo.MongoClient()
db = conn.resources


donationquestions = {}
documents = ['DonationQuestions', 'ghresource', 'UtilityAssistance']

reader = csv.DictReader(open('Resources/'+ 'ghresource' + '.csv'), delimiter=',')
for row in reader:
    print row
    db['ghresource'].insert(row)




