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


zip_p = re.compile('(9[0-9][0-9][0-9][0-9])')

with open('data/Crime_Data_from_2010_to_Present.csv') as f:
    reader = list(csv.DictReader(f))
    num_lines = len(reader)
    i = 0
    for row in reader:
        if 'Location ' in row:
            location_s = row['Location '].split(', ')
            lat = location_s[0][1:]
            lon = location_s[1][0:-1]
            try:
                geolocation = geolocator.reverse("{}, {}".format(lat, lon))
                zip_code = geolocation.raw['address']['postcode']
                zip_code = zip_p.search(zip_code).group(1)
            except:
                print('Got an error: {}'.format(row))
                continue

            dt = parser.parse(row['Date Occurred'])

            monthId = dt.year * 12 + dt.month

            if zip_code in zip_code_data:
                if monthId in zip_code_data[zip_code]:
                    try:
                        increment_or_create(zip_code_data[zip_code][monthId]['total_crime'], 'total')
                    except KeyError:
                        pdb.set_trace()
                else:
                    zip_code_data[zip_code][monthId] = {
                        'total_crime': {
                            'total': 1
                        }
                    }
            else:
                zip_code_data[zip_code] = {
                    monthId: {
                        'total_crime': {
                            'total': 1
                        }
                    }
                }
            i += 1
            print('{} out of {}'.format(i, num_lines))

        if i>100:
            break


def add_data(row, data_dict, data_list, name):
    for element in data_list:
        if element in data_dict[name]:
            row.append(data_dict[name][element])
        else:
            row.append(0)


with open('Sample Data/crime_data_total.csv', 'w') as f:
    writer = csv.writer(f)

    tc = ['total']

    headers = ['Zip Code', 'MonthId'] + tc
    rows = [headers]

    for zip_code in zip_code_data:
        for monthId in zip_code_data[zip_code]:
            row = [zip_code, monthId]
            data_dict = zip_code_data[zip_code][monthId]
            add_data(row, data_dict, tc, 'total_crime')
            rows.append(row)
    writer.writerows(rows)
