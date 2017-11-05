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

def get_files_in_dir(dir):
    return [f for f in listdir(dir) if isfile(join(dir, f))]

def make_sure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)