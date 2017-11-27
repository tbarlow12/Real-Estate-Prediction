import csv
import os, os.path
import re
import pdb
from datetime import datetime
from dateutil import parser
import re

def add_data(row, data_dict, data_list, name):
    for element in data_list:
        if element in data_dict[name]:
            row.append(data_dict[name][element])
        else:
            row.append(0)

zips = {}

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

regex = '^[0-9]*-[A-Z][A-Z]$'

DIR = 'Sample Data'
directory_length = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

for name in os.listdir(DIR):
    if os.path.isfile(os.path.join(DIR, name)):
        if re.match(regex, name):
            zip = name[:4]

            with open('data/' + name + '.csv') as g:
                valueReader = list(csv.DictReader(g))

                i = 0
                for row in valueReader:
                    region_zip = row['Region'][:4]
                    if region_zip in zips:
                        zips[region_zip][row['MonthId']]['MedianSquareValue'] = row['Zip_MedianValuePerSqft_AllHomes']
                    else:
                        zips[row['Zip Code']] = {
                            row['MonthId']: {
                                'Crimes': 0,
                                'MedianSquareValue': row['Zip_MedianValuePerSqft_AllHomes']
                            },
                        }

with open('Sample Data/crime_and_value.csv', 'w') as f:
    writer = csv.writer(f)

    tc = ['total']

    headers = ['Zip Code', 'MonthId', 'Total', 'MedianSquareValue']
    rows = [headers]

    for zip_code in zips:
        for monthId in zips[zip_code]:
            row = [zip_code, monthId]
            data_dict = zips[zip_code][monthId]
            add_data(row, data_dict, tc, 'Crimes')
            rows.append(row)
    writer.writerows(rows)

