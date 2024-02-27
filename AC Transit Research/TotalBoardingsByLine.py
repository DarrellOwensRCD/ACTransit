'''This program will calculate the total boardings of each AC Transit line by direction 
and day and put into one sheet.
The format of each row in the CSV file I will write to is as follows:
Row: {LINE}_{DIR}_{DAY} , TOTAL ON, TOTAL OFF 
Example: 52_Eastbound_Saturday, 100.10, 100.05'''
import re
import csv
filename = "/Users/darrell/Desktop/ACTransit/AC Transit Research/Fall2019/Stop_Summary_Daily_Totals_Fall_2019.csv"
fp = open(filename, 'r')
data = list(csv.reader(fp))
output = [["LINE NAME", "LINE CODE", "DIRECTION", "DAY", "BOARDINGS", "DEBOARDINGS"]]
for i, row in enumerate(data):
	if i > 0: 
		if row[4] == '1': # Prepare new row for data
			if i > 1: #Excluding first row in sheet, write back previous row data
				output.append(line_row)
			name = re.split(r'\s\(', row[0])
			line_row = [name[0], row[1], row[3],row[2],float(row[6]),float(row[7])]
		else:
			line_row[4] += float(row[6])
			line_row[5] += float(row[7])
		if i == len(data) - 1: # EOF check, write back
			output.append(line_row)
with open("/Users/darrell/Desktop/ACTransit/AC Transit Research/Fall2019/BoardingsByLineDirDayF19.csv", 'w') as f:
	csv_writer = csv.writer(f)
	for row in output:
		csv_writer.writerow(row)
	f.close()

