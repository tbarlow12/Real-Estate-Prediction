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

def get_dataset_from_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)[1:]
        x = []
        y = []
        for line in lines:
            for i in range(0,len(line)-1):
                line[i] = int(line[i])
            x.append(line[0:-1])
            y.append(float(line[-1]))
        return x, y

def load_encoded(path):
     with open(path) as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)
        dims = int(lines[0][0])
        instances = lines[2:]
        rows = []
        for instance in instances:
            row = [0] * dims
            for item in instance:
                split = item.split(' ')
                index = int(split[0])
                row[index] = float(split[1])
            rows.append(row)
            '''
            try:
                row[index] = float(split[1])
            except TypeError:
                pdb.set_trace()
            '''
        return [row[0:-1] for row in rows],[row[-1] for row in rows]
                

 
# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

def normalize_dataset(x,y):
    mins_x = []
    maxs_x = []
    for i in range(0,len(x[0])):
        data = [row[i] for row in x]
        mins_x.append(find_min(data))
        maxs_x.append(find_max(data))
    min_y = find_min(y)
    max_y = find_max(y)
    for row in x:
        for i in range(0,len(row)):
            if maxs_x[i] == mins_x[i]:
                if maxs_x[i] == 0:
                    row[i] == 0
                else:
                    row[i] = 1
            else:
                row[i] = (row[i] - mins_x[i]) / (maxs_x[i] - mins_x[i])
    for i in range(0,len(y)):
        y[i] = (y[i] - min_y) / (max_y - min_y)


def find_max(data):
    max = float("-inf")
    for i in data:
        if i > max:
            max = i
    return max

def find_min(data):
    min = float("inf")
    for i in data:
        if i < min:
            min = i
    return min

