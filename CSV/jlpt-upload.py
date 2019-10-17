import csv, pprint

with open('N5.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

pprint.pprint(spamreader)