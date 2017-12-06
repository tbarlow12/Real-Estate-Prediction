import csv
import pdb
import geopy
from geopy.geocoders import Nominatim
from datetime import datetime
from dateutil import parser
import re

geolocator = Nominatim()

zip_code_data = {}
all_crime_codes = set()
all_victim_ages = set()
all_victim_sexes = set()
all_victim_descents = set()

coords = {}


with open('Sample Data/zipcodes_and_coords.csv') as f:
    reader = list(csv.DictReader(f))
    num_lines = len(reader)

    for r in reader:

        current_zip = r['ZIP']

        latitude = r['LAT']
        latitude = str(round(float(latitude), 2))

        longitude = r['LNG']
        longitude = str(round(float(longitude), 2))

        if latitude in coords:
            coords[latitude][longitude] = {
                'ZIP': current_zip
            }
        else:
            coords[latitude] = {
                longitude: {
                    'ZIP': current_zip
                }
            }

        print(latitude + ", " + longitude)

        print(coords[latitude][longitude]['ZIP'])


def increment_or_create(data_dict,key):
    if key in data_dict:
        data_dict[key] += 1
    else:
        data_dict[key] = 1

def get_col_value(row,name):
    raw = row[name]
    if len(raw) == 0:
        val = 'NONE'
    else:
        val = raw
    return '{}={}'.format(name,val)

zip_p = re.compile('(9[0-9][0-9][0-9][0-9])')

with open('data/Crime_Data_from_2010_to_Present.csv') as f:
    reader = list(csv.DictReader(f))
    num_lines = len(reader)
    i = 0
    for row in reader:
        if 'Location ' in row:
            location_s = row['Location '].split(', ')

            if location_s[0][1:]=='':
                continue

            if location_s[1][1:]=='':
                continue

            lat = location_s[0][1:]
            lon = location_s[1][0:-1]

            lat = str(round(float(lat),2))

            lon = str(round(float(lon),2))

            if lat in coords:
                if lon in coords[lat]:
                    zip_code = coords[lat][lon]['ZIP']
                else:
                    while lon not in coords[lat]:
                        lon = str(0.01 + float(lon))
                    zip_code = coords[lat][lon]['ZIP']
            else:
                while lat not in coords:
                    lat = str(0.01 + float(lat))
                if lon in coords[lat]:
                    zip_code = coords[lat][lon]['ZIP']
                else:
                    while lon not in coords[lat]:
                        lon = str(0.01 + float(lon))
                    zip_code = coords[lat][lon]['ZIP']


            print(zip_code)

            # try:
            #     geolocation = geolocator.reverse("{}, {}".format(lat,lon))
            #     zip_code = geolocation.raw['address']['postcode']
            #     zip_code = zip_p.search(zip_code).group(1)
            # except AttributeError:
            #     print('Got an error: {}'.format(row))
            #     continue

            dt = parser.parse(row['Date Occurred'])

            monthId = dt.year * 12 + dt.month

            crime_code = get_col_value(row,'Crime Code')
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
                        increment_or_create(zip_code_data[zip_code][monthId]['crime_codes'],crime_code)
                        increment_or_create(zip_code_data[zip_code][monthId]['victim_ages'],victim_age)
                        increment_or_create(zip_code_data[zip_code][monthId]['victim_sexes'],victim_sex)
                        increment_or_create(zip_code_data[zip_code][monthId]['victim_descents'],victim_descent)
                    except KeyError:
                        pdb.set_trace()
                else:
                    zip_code_data[zip_code][monthId] = {
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
                    monthId : {
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
            print('{} out of {}'.format(i,num_lines))


def add_data(row,data_dict,data_list,name):
    for element in data_list:
        if element in data_dict[name]:
            row.append(data_dict[name][element])
        else:
            row.append(0)

with open('Sample Data/crime_data.csv','w') as f:
    writer = csv.writer(f)

    cc = list(all_crime_codes)
    va = list(all_victim_ages)
    vs = list(all_victim_sexes)
    vd = list(all_victim_descents)

    headers = ['Zip Code','MonthId'] + cc + va + vs + vd

    rows = [headers]

    for zip_code in zip_code_data:
        for monthId in zip_code_data[zip_code]:
            row = [zip_code,monthId]
            data_dict = zip_code_data[zip_code][monthId]
            add_data(row,data_dict,cc,'crime_codes')
            add_data(row,data_dict,va,'victim_ages')
            add_data(row,data_dict,vs,'victim_sexes')
            add_data(row,data_dict,vd,'victim_descents')
            rows.append(row)
    writer.writerows(rows)
        