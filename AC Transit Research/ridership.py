#Program assumes CSV file of ACT lines is sorted by Line, by day, by Direction, by sequential stop order in ascending
import csv
def div(num, den):
    if den == 0:
        return 0
    else:
        return float(num / den)
def add_column(data, col_names):
    for row in data:
        if row[0] == 'ROUTE_NAME':
            for header in col_names:
                row.append(header)
        else:
            for i in range(0, len(col_names)):
                row.append('')
    return data
def unique_val(data):
    vals = []
    dic = {}
    for d in data:
        if d[1] != "ROUTE" and d[1] not in vals:
            vals.append(d[1])
            days = {"Weekday" : None, "Saturday" : None, "Sunday" : None}
            if "Westbound" in d[3] or "Eastbound" in d[3]:
                days["Weekday"] = {"Westbound" : None, "Eastbound" : None}
                days["Saturday"] = {"Westbound" : None, "Eastbound" : None}
                days["Sunday"] = {"Westbound" : None, "Eastbound" : None}
            else:
                days["Weekday"] = {"Northbound" : None, "Southbound" : None}
                days["Saturday"] = {"Northbound" : None, "Southbound" : None}
                days["Sunday"] = {"Northbound" : None, "Southbound" : None}
            metric = {"on" : days.copy() , "off": days.copy(), "total": days.copy()}
            dic[d[1]] = metric 
    return vals, dic
sourcefile = "/Users/darrell/Desktop/AC Transit Research/Stop_Summary_Daily_Totals_Spring_2023.csv"
destfile = "/Users/darrell/Desktop/AC Transit Research/Stop_Summary_Daily_Totals_Spring_2023_Ranks_Added.csv"
with open(sourcefile, 'r') as f:
    data =  csv.reader(f, delimiter=',')
    d = list(data)
# Pos 12, 13, 14
d = add_column(d,['ON RATIO','OFF RATIO', 'TOTAL RATIO'])
returned = unique_val(d)
l = returned[0]
dic = returned[1]
print("Start")
flag = False
days = ["Weekday", "Saturday", "Sunday"]
for line_no in l: # Going over each bus line for each day and each direction
    for day in days:
        directions = list(dic[line_no]["on"][day].keys())
        for direction in directions:
            for i, file_line in enumerate(d): #Iterating through entire file sequentially
                if flag == True: #If we've found the proper line
                    if i == (len(d) - 1) or direction != file_line[3] or file_line[1] != line_no or day != file_line[2]: # New line route or dir is found, clean up
                        if i == (len(d) - 1): #last row
                            on_sum += float(file_line[6])
                            off_sum += float(file_line[7])
                            total_sum += float(file_line[8])                          
                        dic[line_no]["on"][day][direction] = on_sum
                        dic[line_no]["off"][day][direction] = off_sum
                        dic[line_no]["total"][day][direction] = total_sum
                        flag = False
                        # print(f"{line_no} {direction} {day}: {on_sum} {off_sum} {total_sum}")
                        break #Stop searching the datafile, reset
                    else:
                        on_sum += float(file_line[6])
                        off_sum += float(file_line[7])
                        total_sum += float(file_line[8])                 
                else:
                    if file_line[1] != 'ROUTE':
                        if file_line[1] == line_no and day == file_line[2] and direction == file_line[3]:
                           #this is the start
                            on_sum = float(file_line[6])
                            off_sum = float(file_line[7])
                            total_sum = float(file_line[8])
                            flag = True
# With all AC Transit Line dic calculated, divy-up percentages for each stop in each direction
for line_stop in d:
    if line_stop[1] != "ROUTE":
        # Insert percentage of total boardings
        try:
            num = line_stop[1]
            day = line_stop[2]
            dire = line_stop[3]
            on_rank = div(float(line_stop[6]) , dic[num]["on"][day][dire])
            off_rank = div(float(line_stop[7]) , dic[num]["off"][day][dire])
            total_rank = div(float(line_stop[8]) , dic[num]["total"][day][dire])
            line_stop[12] = on_rank
            line_stop[13] = off_rank
            line_stop[14] = total_rank
        except TypeError as e:
            print(num)
# Write back
print("Writing Back")
with open(destfile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(d)
    f.close()
print("Finished.")
    
            
