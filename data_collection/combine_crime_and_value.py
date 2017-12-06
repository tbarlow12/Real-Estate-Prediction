import csv
import os, os.path
import re
import pdb
from datetime import datetime
from dateutil import parser
import re
import helpers as h

def add_data(row, data_dict, data_list, name):
    for element in data_list:
        if element in data_dict[name]:
            row.append(data_dict[name][element])
        else:
            row.append(0)

'''
with open('Sample Data/crime_data_total.csv') as f:
    reader = list(csv.DictReader(f))
    pdb.set_trace()

    i = 0
    for row in reader:
        if row['Zip Code'] in zips:
            zips[row['Zip Code']][row['MonthId']]['Crimes'] = row['Crimes']
        else:
            zips[row['Zip Code']] = {
                row['MonthId']: {
                    'Crimes': row['Crimes'],
                    'MedianSquareValue': 0
                },
            }
'''

all_features = set()
all_zips = set()
all_months = set()

def get_dict_except(data_dict,row,exclude_titles):
    if data_dict is None:
        data_dict = {}
    for key in row:
        if key not in exclude_titles:
            data_dict[key] = row[key]
            all_features.add(key)
    return data_dict

def blank_feature_dict():
    d = {}
    for f in all_features:
        d[f] = 0.0
    return d


zips = {}

with open('Sample Data/final_crime_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_zips.add(row['Zip Code'])
        all_months.add(row['MonthId'])
        get_dict_except(None,row,['Zip Code','MonthId'])

for z in all_zips:
    for m in all_months:
        if z in zips:
            zips[z][m] = blank_feature_dict()
        else:
            zips[z] = {
                m : blank_feature_dict()
            }

with open('Sample Data/final_crime_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_zip = row['Zip Code']
        month_id = row['MonthId']
        if row_zip in zips:
            zips[row_zip][month_id] = get_dict_except(None,row,['Zip Code','MonthId'])
        else:
            zips[row_zip] = {
                month_id : get_dict_except(None,row,['Zip Code','MonthId'])
            }

data_path = 'Sample Data/california/'

california_real_estate_files = h.get_files_in_dir(data_path)

for real_estate in california_real_estate_files:
    zip = real_estate[0:5]
    with open(data_path + real_estate) as g:
        valueReader = csv.DictReader(g)
        i = 0
        for row in valueReader:
            region_zip = row['Region'][0:5]
            month_id = row['MonthId']
            if region_zip in zips:
                if month_id in zips[region_zip]:
                    zips[region_zip][month_id] = get_dict_except(zips[region_zip][month_id],row,['Region','Year','Month','MonthId'])

feature_list = list(all_features)
feature_list.sort(reverse=True)

missing_zips = set()

with open('Sample Data/final_feature_set.csv', 'w') as f:
    writer = csv.writer(f)

    headers = ['Zip Code', 'MonthId'] + feature_list
    rows = [headers]
    missing = 0
    for zip_code in zips:
        for monthId in zips[zip_code]:
            row = [zip_code, monthId]
            data_dict = zips[zip_code][monthId]
            for feature in feature_list:
                if feature in data_dict:
                    row.append(data_dict[feature])
                else:
                    row.append('')
            rows.append(row)
    writer.writerows(rows)

