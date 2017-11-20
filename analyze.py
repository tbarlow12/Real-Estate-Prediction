# Converts the csv file into a feature set

import csv


def featurize():
	with open("Sample Data/84070-UT.csv", "rb") as source, open("result", "wb") as result:
		rdr = csv.reader(source)
		wtr = csv.writer(result)

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
				if headers[index] == 'Year':
					year = int(c) - 1990 # Base Year
					year = year * 12
					month = int(r[index + 1])

					# combine year and month

					combine = year + month

					example.append(combine)
					print(combine)
				else:
					example.append(c)
				index += 1

			examples.append(example)







