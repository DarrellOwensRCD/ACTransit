#Adding per capita numbers to city bus ridership
import csv
file1 = "/Users/darrell/Desktop/AC Transit Research/ACTSp23RidershipByCity.csv"
file2 = "/Users/darrell/Desktop/Census2020/AllCACities2020Census.csv"
def add_column(data, col_names):
    for row in data:
        if row[0] == 'CITY':
            for header in col_names:
                row.append(header)
        else:
            for i in range(0, len(col_names)):
                row.append('')
    return data
def div(num, den):
    if den == 0:
        return 0
    else:
        return float(num / den)
print("START")
with open(file1, 'r') as f:
    data =  csv.reader(f, delimiter=',')
    cities = list(data)
    f.close()
with open(file2, 'r') as d:
    data =  csv.reader(d, delimiter=',')
    census = list(data)
    d.close()
cities = add_column(cities, ["POPULATION (2020)", "BOARDINGS PER CAPITA", "EXITS PER CAPITA", "TOTAL PER CAPITA"])
for city in cities:
    if city != "all":
        for line in census:
            if line[0] == city[0]:
                print(city)
                pop = int(line[2])
                city[6] = pop
                city[7] = div(float(city[3]), pop)
                city[8] = div(float(city[4]), pop)
                city[9] = div(float(city[5]), pop)
print("FINISHED")
with open(file1, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(cities)
    f.close()
                
