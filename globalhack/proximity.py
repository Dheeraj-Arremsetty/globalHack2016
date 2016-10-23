#!/usr/bin/env python2.7

import csv
import math

class Proximity(object):
    db_path = '../data/zipcodes.txt'

    zipcode_db = {}

    @staticmethod
    def read_data():
        with open(Proximity.db_path) as db_file:
            reader = csv.DictReader(db_file, delimiter=',')
            for row in reader:
               Proximity.zipcode_db[row['ZIP']] = (float(row['LAT']), float(row['LNG']))
#               print row['ZIP']

    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        R = 6371e3;
        f1 = math.radians(lat1)
        f2 = math.radians(lat2)
        df = math.radians(lat2-lat1)
        dl = math.radians(lon2-lon1)

        a = math.sin(df/2) * math.sin(df/2) + \
            math.cos(f1) * math.cos(f2) * \
            math.sin(dl/2) * math.sin(dl/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    @staticmethod
    def find_close_zipcodes(zip_code, max_distance = 15):
        if len(Proximity.zipcode_db) == 0:
            Proximity.read_data()

        max_distance_in_meters = 1609.34 * max_distance
        lat1, lon1 = Proximity.zipcode_db[zip_code]
        matching_zipcodes = []
        for zip_code2 in Proximity.zipcode_db.keys():
            lat2, lon2 = Proximity.zipcode_db[zip_code2]

            distance = Proximity.distance(lat1, lon1, lat2, lon2)
            if distance < max_distance_in_meters:
                matching_zipcodes.append(zip_code2)

        for matching_zipcode in matching_zipcodes:
            print 'Matching: %s' % matching_zipcode

        return matching_zipcodes

if __name__ == '__main__':
    Proximity.read_data()
    Proximity.find_close_zipcodes("63109")
