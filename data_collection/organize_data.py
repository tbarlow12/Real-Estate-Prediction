import csv
import pdb
import os
from os import listdir
from os.path import isfile, join
import helpers as h
import re

categorical_encoding_size = 10

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

def hash_value(item,size):
    final_hash = [0] * size
    for char in item:
        final_hash[hash(char) % size] += 1
    return final_hash


def encode_categorical_features(feature_indices,feature_vector):
    for index in feature_indices:
        index = index * categorical_encoding_size
        distinct_values = set([item[index] for item in feature_vector])
        hash_d = {}
        for item in distinct_values:
            hash_d[item] = hash_value(item,categorical_encoding_size)
        for i in range(0,len(feature_vector)):
            instance = feature_vector[i]
            feature_vector[i] = instance[0:index] + hash_d[instance[index]] + instance[index + 1:]

def get_feature_vector(data_dict,filename):
    transformed = []
    date_p = re.compile('(?P<year>[0-9]+)-(?P<month>[0-9]+)')
    failed_parses = []
    max_rank = 0
    for instance in data_dict[filename]:
        region_name = instance['RegionName']
        state = instance['State'] if 'State' in instance else ''
        county = instance['County'] if 'County' in instance else ''
        metro = instance['Metro'] if 'Metro' in instance else ''
        city = instance['City'] if 'City' in instance else ''
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
            instance[5] = max_rank + 1
        transformed.extend(failed_parses)
    return transformed

def transform(data_dict,filename):
    feature_vector = get_feature_vector(data_dict,filename)
    
    return feature_vector

def output_feature_vector(target_path,feature_vector):
    print('Outputting ' + target_path)
    with open(target_path,mode='w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'RegionName','State','County','Metro','City','SizeRank','Year','Month','Value'
        ])
        writer.writerows(feature_vector)

def encoded_row(row):
    result = []
    for i in range(0,len(row)):
        if row[i] != 0 and row[i] != '0':
            result.append('{} {}'.format(i,row[i]))
    return result

def output_encoded_vector(target_path,feature_vector):
    print('Outputting ' + target_path)
    with open(target_path,mode='w') as f:
        writer = csv.writer(f)
        categorical_headers = ['RegionName','State','County','Metro','City']
        headers = []
        for c in categorical_headers:
            headers.append('{} {}'.format(c,categorical_encoding_size))                
        headers.extend(['SizeRank','Year','Month','Value'])
        writer.writerow([len(feature_vector[0])])
        writer.writerow(headers)
        for row in feature_vector:
            e = encoded_row(row)
            writer.writerow(e)

def output_aggregate(aggregate,metrics,target_dir):
    
    for region in aggregate:
        with open(target_dir + '{}.csv'.format(region),mode='w') as f:
            writer = csv.writer(f)
            headers = ['Region','Year','Month','MonthId','IsDuringRecession'] + metrics
            writer.writerow(headers)
            
            region_d = aggregate[region]
            for year in region_d:
                year_d = region_d[year]
                for month in year_d:
                    month_d = year_d[month]
                    metric_values = []
                    for metric in metrics:
                        if metric in month_d:
                            metric_values.append(month_d[metric])
                        else:
                            metric_values.append('')
                    monthId = year * 12 + month
                    writer.writerow([
                        region,
                        year,
                        month,
                        monthId,
                        1 if monthId >= (2007 * 12 + 12) and monthId <= (2009 * 12 + 6) else 0
                    ] + metric_values)




def add_to_aggregate(aggregate,feature_vector,metric):

    year = feature_vector[6]
    month = feature_vector[7]
    value = feature_vector[8]

    aggregate_name = ''
    #'RegionName','State','County','Metro','City','SizeRank','Year','Month','Value'
    aggregate_name += '{}-{}'.format(feature_vector[0],feature_vector[1])
    aggregate_name = aggregate_name.replace('/',' ')
    if '/' in aggregate_name:
        pdb.set_trace()
    if aggregate_name in aggregate:
        if year in aggregate[aggregate_name]:
            if month in aggregate[aggregate_name][year]:
                aggregate[aggregate_name][year][month][metric] = value
            else:
                aggregate[aggregate_name][year][month] = {
                    metric : value
                }
        else:
            aggregate[aggregate_name][year] = {
                month : {
                    metric : value
                }
            }
    else:
        aggregate[aggregate_name] = {
            year : {
                month : {
                    metric : value
                }
            }
        }

def output_transformed_data(root_dir):
    for dir in h.get_immediate_subdirectories(root_dir):
        data_dict = get_data_dict(root_dir,dir)
        target_dir = root_dir + '/' + dir + '/transformed/'
        h.make_sure_dir_exists(target_dir)
        aggregate = {}
        metrics = []
        for filename in data_dict:
            print('Aggregating: {}'.format(filename))
            feature_vector = transform(data_dict,filename)
            for vector in feature_vector:
                add_to_aggregate(aggregate,vector,filename)  
            metrics.append(filename)
        sorted(metrics)
        output_aggregate(aggregate,metrics,target_dir)  
        '''        
            output_feature_vector(target_dir + filename + '.csv' ,feature_vector)
            encode_categorical_features([0,1,2,3,4],feature_vector)
            encoded_dir = target_dir + 'encoded/'
            h.make_sure_dir_exists(encoded_dir)
            output_encoded_vector(encoded_dir + filename + '.csv',feature_vector)
            '''

        '''    if bedroom_p.match(filename):
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
            output_aggregate(aggregate_dir + name + '.csv',feature_vector)'''
        

def main():
    output_transformed_data('data/zillow')

if __name__ == '__main__':
    main()