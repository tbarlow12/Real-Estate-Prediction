import csv

with open("Sample Data/84070-UT.csv", "rb") as source, open("result", "wb") as result:
	rdr = csv.reader(source)
	wtr = csv.writer(result)
	for r in rdr:
		wtr.writerow(r[0] + [r[1] + ' ' + r[2]] + r[3:])
