import csv
import pdb
from datetime import datetime
from dateutil import parser
import re

zips = {}

with open('data/Crime_Data_from_2010_to_Present.csv') as f:
    reader = list(csv.DictReader(f))



    num_lines = len(reader)
    i = 0
    for row in reader:
        if row['Zip Code'] in zips:
            zips[row['Zip Code']][row['MonthId']]['Crimes'] = row['Crimes']
        else:
            zips[row['Zip Code']] = {
                row['MonthId']: {
                'Crimes': row['Crimes']
                }
            }