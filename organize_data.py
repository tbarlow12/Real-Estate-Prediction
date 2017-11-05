import csv
import pdb
import os
from os import listdir
from os.path import isfile, join
import helpers as h
import re

def get_data_dict(path):
    data_dict = {}
        files = h.get_files_in_dir(path)
        p = re.compile(dir, re.I)
        for f in files:
            if p.match(f):
                print(f)
                name = f[0:-4]
                data_dict[name] = h.csv_to_list_of_dicts(current_path + '/' + f)
    return data_dict

def transform(data_dict):
    transformed = []
    

def output_transformed_data(root_dir,target_dir):
    for dir in h.get_immediate_subdirectories(root_dir):
        data_dict = get_data_dict(root_dir + '/' + dir)
        t = transform(data_dict)


def main():
    output_transformed_data('data/zillow','transformed')


    #m = csv_to_list_of_dicts('data/zillow/Neighborhood_MedianValuePerSqft_AllHomes.csv')

if __name__ == '__main__':
    main()