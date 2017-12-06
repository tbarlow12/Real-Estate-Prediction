import csv
import pdb
import geopy
from geopy.geocoders import ArcGIS, Bing, Nominatim, OpenCage, GeocoderDotUS, GoogleV3, OpenMapQuest
from datetime import datetime
from dateutil import parser
import time
import re
import math

# geolocator = Nominatim()
#
# arcgis = ArcGIS(timeout=100)
# bing = Bing('Ak1GEcWya63nbRV4w_negXAFv1qJhX6nB0uAAlcBk24BlNy06VCAAJnlq6rnGvLv',timeout=100)
# nominatim = Nominatim(timeout=100)
# opencage = OpenCage('640fbdc889384bc0b823f5a61d5c77ac',timeout=100)
# geocoderDotUS = GeocoderDotUS(timeout=100)
# googlev3 = GoogleV3(timeout=100)
# openmapquest = OpenMapQuest(timeout=100)

# geocoders = [nominatim, googlev3, bing, geocoderDotUS, opencage, openmapquest, arcgis]

zip_code_data = {}
all_crime_codes = set()
all_victim_ages = set()
all_victim_sexes = set()
all_victim_descents = set()

zips = {}

california = 90000

with open('Sample Data/zipcodes_and_coords.csv') as f:
    reader = csv.DictReader(f)

    for r in reader:

        current_zip = int(r['ZIP'])
        if current_zip < california:
            continue

        latitude = float(r['LAT'])

        longitude = float(r['LNG'])
        zips[current_zip] = [latitude,longitude]



def increment_or_create(data_dict, key):
    if key in data_dict:
        data_dict[key] += 1
    else:
        data_dict[key] = 1


def get_col_value(row, name):
    raw = row[name]
    if len(raw) == 0:
        val = 'NONE'
    else:
        val = raw
    return '{}={}'.format(name, val)


def euclidean(lat1,lon1,lat2,lon2):
    return math.sqrt((lat2 - lat1)**2+(lon2 - lon1)**2)


def coords_to_zip(lat,lon):
    smallest_dist = float('inf')
    closest_zip = None
    for zip in zips:
        coords = zips[zip]
        dist = euclidean(coords[0],coords[1],lat,lon)
        if dist < smallest_dist:
            smallest_dist = dist
            closest_zip = zip
    return closest_zip

zip_p = re.compile('(9[0-9][0-9][0-9][0-9])')

with open('data/Crime_Data_from_2010_to_Present.csv') as f:
    reader = csv.DictReader(f)
    i = 0
    for row in reader:
        if 'Location ' in row:
            location_s = row['Location '].split(', ')

            if location_s[0][1:]=='':
                continue

            if location_s[1][1:]=='':
                continue

            lat = float(location_s[0][1:])
            lon = float(location_s[1][0:-1])
            zip_code = coords_to_zip(lat,lon)
            

            dt = parser.parse(row['Date Occurred'])

            monthId = dt.year * 12 + dt.month

            crime_code = get_col_value(row,'Crime Code')
            description = get_col_value(row,'Crime Code Description')
            crime_code += ' ' + description
            victim_age = get_col_value(row,'Victim Age')
            victim_sex = get_col_value(row,'Victim Sex')
            victim_descent = get_col_value(row,'Victim Descent')

            all_crime_codes.add(crime_code)
            all_victim_ages.add(victim_age)
            all_victim_sexes.add(victim_sex)
            all_victim_descents.add(victim_descent)

            if zip_code in zip_code_data:
                if monthId in zip_code_data[zip_code]:
                    try:
                        increment_or_create(zip_code_data[zip_code][monthId]['total_crime'], 'total')
                        increment_or_create(zip_code_data[zip_code][monthId]['crime_codes'],crime_code)
                        increment_or_create(zip_code_data[zip_code][monthId]['victim_ages'],victim_age)
                        increment_or_create(zip_code_data[zip_code][monthId]['victim_sexes'],victim_sex)
                        increment_or_create(zip_code_data[zip_code][monthId]['victim_descents'],victim_descent)
                    except KeyError:
                        pdb.set_trace()
                else:
                    zip_code_data[zip_code][monthId] = {
                        'total_crime': {
                            'total': 1
                        },
                        'crime_codes' : {
                            crime_code : 1
                        },
                        'victim_ages' : {
                            victim_age : 1
                        },
                        'victim_sexes' : {
                            victim_sex : 1
                        },
                        'victim_descents' : {
                            victim_descent : 1
                        }
                    }
            else:
                zip_code_data[zip_code] = {
                    monthId: {
                        'total_crime': {
                            'total': 1
                        },
                        'crime_codes' : {
                            crime_code : 1
                        },
                        'victim_ages' : {
                            victim_age : 1
                        },
                        'victim_sexes' : {
                            victim_sex : 1
                        },
                        'victim_descents' : {
                            victim_descent : 1
                        }
                    }
                }
            i += 1
            print(i)
            


def add_data(row, data_dict, data_list, name):
    for element in data_list:
        if element in data_dict[name]:
            row.append(data_dict[name][element])
        else:
            row.append(0)


with open('Sample Data/final_crime_data.csv', 'w') as f:
    writer = csv.writer(f)

    cc = list(all_crime_codes)
    va = list(all_victim_ages)
    vs = list(all_victim_sexes)
    vd = list(all_victim_descents)

    tc = ['total']

    headers = ['Zip Code', 'MonthId'] + tc + cc + va + vs + vd
    rows = [headers]

    for zip_code in zip_code_data:
        for monthId in zip_code_data[zip_code]:
            row = [zip_code, monthId]
            data_dict = zip_code_data[zip_code][monthId]

            if 'total_crime' in data_dict:
                row.append(data_dict['total_crime']['total'])
            else:
                row.append(0)

            add_data(row,data_dict,cc,'crime_codes')
            add_data(row,data_dict,va,'victim_ages')
            add_data(row,data_dict,vs,'victim_sexes')
            add_data(row,data_dict,vd,'victim_descents')


            rows.append(row)
    writer.writerows(rows)
