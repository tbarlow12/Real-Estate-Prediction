import csv
import pdb

def csv_to_list_of_dicts(path):
    with open(path) as csvfile:
        reader = list(csv.DictReader(csvfile))
        pdb.set_trace()
        

def main():
    m = csv_to_list_of_dicts('data/zillow/Neighborhood_MedianValuePerSqft_AllHomes.csv')

if __name__ == '__main__':
    main()