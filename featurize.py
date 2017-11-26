# Converts the csv file into a feature set
import csv

examples = []

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







