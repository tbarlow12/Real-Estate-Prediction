# Converts the csv file into a feature set
import csv
import pdb
from models import stochasticGD
import cross_validation

examples = []

def featurize_file(path):
	with open(path) as f:
		csv_dict = csv.DictReader(f)
		x = []
		y = []
		for row in csv_dict:
			zip = row['Region'].strip()[0:-3]
			monthId = int(row['MonthId'].strip())
			if 'Zip_MedianValuePerSqft_AllHomes' in row:
				medianValue = float(row['Zip_MedianValuePerSqft_AllHomes'])
				x.append([monthId])
				y.append(medianValue)
			else:
				continue
		return x, y

features, labels = featurize_file('Sample Data/california/90001-CA.csv')

stochastic = stochastic()

print(cross_validate(stochastic,features,labels))		

def featurize():
	with open('Sample Data/crime_and_value.csv', "rb") as source:
		rdr = csv.reader(source)

		csv_headings = next(rdr)

		examples = []
		index = 0
		headers = []

		for header in csv_headings:
			headers.append(header)


		for r in rdr:
			index = 0
			example = []
			for c in r:
				example.append(c)

			examples.append(example)







