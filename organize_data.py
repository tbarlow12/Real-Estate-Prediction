import csv
import pdb
import os
from os import listdir
from os.path import isfile, join
import helpers as h
import re

def get_data_dict(root_dir,dir):
    data_dict = {}
    path = root_dir + '/' + dir
    files = h.get_files_in_dir(path)
    p = re.compile(dir, re.I)
    for f in files:
        if p.match(f):
            print(f)
            name = f[0:-4]
            data_dict[name] = h.csv_to_list_of_dicts(path + '/' + f)
    return data_dict

def encode_categorical_features(feature_indices,feature_vector):
    for index in feature_indices:
        distict_values = set([item[index] for item in feature_vector])
        value_d = {}
        value = 1
        for item in distict_values:
            value_d[item] = value
            value += 1
        for instance in feature_vector:
            h = hash(instance[index])
            pdb.set_trace()
            instance[index] = value_d[instance[index]]
        #TODO: Hash it so you can do the same thing in the prediction models

def get_feature_vector(data_dict,filename):
    transformed = []
    date_p = re.compile('(?P<year>[0-9]+)-(?P<month>[0-9]+)')
    failed_parses = []
    max_rank = 0
    for instance in data_dict[filename]:
        region_name = instance['RegionName']
        state = instance['State'] if 'State' in instance else region_name
        county = instance['County'] if 'County' in instance else region_name
        metro = instance['Metro'] if 'Metro' in instance else region_name
        city = instance['City'] if 'City' in instance else region_name
        for key in instance:
            if date_p.match(key):
                date_d = [m.groupdict() for m in date_p.finditer(key)]
                year = int(date_d[0]['year'])
                month = int(date_d[0]['month'])
                if len(instance[key].strip()) > 0:
                    try:
                        value = float(instance[key])
                    except ValueError:
                        value = 0
                    size_rank = -1
                    try:
                        size_rank = int(instance['SizeRank'])
                        if size_rank > max_rank:
                            max_rank = size_rank
                        transformed.append([
                            region_name,state,county,metro,city,size_rank,year,month,value
                        ])
                    except ValueError:
                        failed_parses.append([
                            region_name,state,county,metro,city,size_rank,year,month,value
                        ])
    if len(failed_parses) > 0:
        for instance in failed_parses:
            instance[8] = max_rank + 1
        transformed.extend(failed_parses)
    return transformed

def transform(data_dict,filename):
    feature_vector = get_feature_vector(data_dict,filename)
    encode_categorical_features([1,2,3,4],feature_vector)
    return feature_vector

def output_feature_vector(target_path,feature_vector):
    print('Outputting ' + target_path)
    with open(target_path,mode='w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'RegionName','State','County','Metro','City','SizeRank','Year','Month','Value'
        ])
        writer.writerows(feature_vector)

def output_aggregate(target_path,feature_vector):
    print('Outputting ' + target_path)
    with open(target_path,mode='w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'RegionName','State','County','Metro','City','SizeRank','Year','Month','Bedrooms','Value'
        ])
        writer.writerows(feature_vector)


def output_transformed_data(root_dir):
    bedroom_p = re.compile('(?P<name>.*)_(?P<bedrooms>[0-9]+)bedroom',re.I)
    for dir in h.get_immediate_subdirectories(root_dir):
        data_dict = get_data_dict(root_dir,dir)
        target_dir = root_dir + '/' + dir + '/transformed/'
        h.make_sure_dir_exists(target_dir)
        aggregates = {}
        for filename in data_dict:
            feature_vector = transform(data_dict,filename)
            output_feature_vector(target_dir + filename + '.csv' ,feature_vector)
            if bedroom_p.match(filename):
                bedroom_d = [m.groupdict() for m in bedroom_p.finditer(filename)][0]
                name = bedroom_d['name']
                bedrooms = int(bedroom_d['bedrooms'])
                for row in feature_vector:
                    row.insert(-1,bedrooms)
                if name in aggregates:
                    aggregates[name].extend(feature_vector)
                else:
                    aggregates[name] = feature_vector
        for name in aggregates:
            aggregate_dir = target_dir + 'aggregate/'
            h.make_sure_dir_exists(aggregate_dir)
            output_aggregate(aggregate_dir + name + '.csv',feature_vector)
        

def main():
    output_transformed_data('data/zillow')

if __name__ == '__main__':
    main()