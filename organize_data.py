import csv
import pdb
import os
from os import listdir
from os.path import isfile, join

def csv_to_list_of_dicts(path):
    with open(path) as csvfile:
        return list(csv.DictReader(csvfile))

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
        
def get_all_data(root_dir):
    data_dict = {}
    for dir in get_immediate_subdirectories(root_dir):
        print(dir)
        data_dict[dir] = {}
        current_path = root_dir + '/' + dir
        files = [f for f in listdir(current_path) if isfile(join(current_path, f))]
        for f in files:
            print(f)
            name = f[0:-4]
            data_dict[dir][name] = csv_to_list_of_dicts(current_path + '/' + f)
    return data_dict

def main():
    all_data = get_all_data('data/zillow')
    print(all_data)


    #m = csv_to_list_of_dicts('data/zillow/Neighborhood_MedianValuePerSqft_AllHomes.csv')

if __name__ == '__main__':
    main()