import csv
import pdb
import geopy
from geopy.geocoders import Nominatim

geolocator = Nominatim()

with open('Crime_Data_from_2010_to_Present.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'Location ' in row:
            
            location_s = row['Location '].split(', ')
            lat = location_s[0][1:]
            lon = location_s[1][0:-1]
            geolocation = geolocator.reverse("{}, {}".format(lat,lon))
            zip_code = geolocation.raw['address']['postcode']