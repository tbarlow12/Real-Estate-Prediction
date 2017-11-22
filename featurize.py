# Converts the csv file into a feature set while combining the year and month

import csv


def featurize():
	with open("Sample Data/84070-UT.csv", "rb") as source, open("result", "wb") as result:
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
				index += 1

			examples.append(example)







