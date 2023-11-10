# Program calculates share of on / off/ total boardings by city for all bus lines
import csv
import copy
import json
import time
from shapely.geometry import shape, Point
# Helper function to print table
def print_table(d):
    for key in d.keys():
        print(key, d[key])
# Division 
def div(num, den):
    if den == 0:
        return 0
    else:
        return float(num / den)
# Adds a len(col_names) amount of columns to the csv data instance
def add_column(data, col_names):
    for row in data:
        if row[0] == 'ROUTE_NAME':
            for header in col_names:
                row.append(header)
        else:
            for i in range(0, len(col_names)):
                row.append('')
    return data
# Determines which city name and its GISJOIN a point is located; None returned if no city is found
def point_location(point, polygon, last_bou, last_name):
    if last_bou:
        if last_bou.contains(point):
                return ( last_name , last_bou)
    for city in polygon["features"]:
        city_limits = shape(city['geometry'])
        if city_limits.contains(point):
            return (city["properties"]["NAME"] , city_limits)
    return None
def make_city_dic(cities):
    #Dictionary structure: City(s) Area -> (On -> Ridership / Off -> Ridership  / Total -> Ridership)
    sub = {"on" : 0, "off" : 0, "total" : 0 }
    days = {"Weekday" : copy.deepcopy(sub), "Saturday": copy.deepcopy(sub), "Sunday": copy.deepcopy(sub)}
    d = {"all" : copy.deepcopy(days)}
    for city in cities:
        d[city] = copy.deepcopy(days)
    return d
def add_city_dic(dic, city):
    # Commuter cities I cant think of like Menlo Park or Pittsburg can be added to the dictionary here
    sub = {"on" : 0, "off" : 0, "total" : 0 }
    days = {"Weekday" : copy.deepcopy(sub), "Saturday": copy.deepcopy(sub), "Sunday": copy.deepcopy(sub)}
    dic[city] = days
    return dic
def make_metro_dic():
    #Dictionary structure: Metro Area -> (On -> Ridership / Off -> Ridership  / Total -> Ridership)
    sub = {"on" : 0, "off" : 0, "total" : 0 }
    days = {"Weekday" : copy.deepcopy(sub), "Saturday": copy.deepcopy(sub), "Sunday": copy.deepcopy(sub)}
    d = {"all" : copy.deepcopy(days), "m1": copy.deepcopy(days), "m2": copy.deepcopy(days), "m3" : copy.deepcopy(days), "m4" : copy.deepcopy(days)}
    return d
sourcefile = "/Users/darrell/Desktop/ACTransit/AC Transit Research/2019/Stop_Summary_Daily_Totals_Fall_2019.csv"
destfile = "/Users/darrell/Desktop/ACTransit/AC Transit Research/2019/Stop_Summary_Daily_Totals_Fall_2019_Ranks_Added_CityVer.csv"
destfile2 = "/Users/darrell/Desktop/ACTransit/AC Transit Research/2019/ACTFa19RidershipByMetroArea.csv"
destfile3 = "/Users/darrell/Desktop/ACTransit/AC Transit Research/2019/ACTFa19RidershipByCity.csv"
cityfile = "/Users/darrell/Desktop/Census2020/Census2020Cities/california_cities.geojson"
with open(sourcefile, 'r') as f:
    data =  csv.reader(f, delimiter=',')
    d = list(data)
    f.close()
# Add the additional columns: Metro Region ID, City, Metro Ratio On, MR Off, MR Total, Systemwide Ratio On, SR Off, SR Total            
header = ["Metro ID", "Metro Cities", "City", "Metro Ratio On", "Metro Ratio Off", "Metro Ratio Total", "Systemwide Ratio On", "Systemwide Ratio Off", "Systemwide Ratio Total"]
d = add_column(d, header)
with open(cityfile, 'r') as f:
    cities = json.load(f)
# Run through each stop, determine which CDP or city its in, then add its entry/exits to city dictionary
unique_cities = []
m1 = ["Richmond", "Kensington", "El Cerrito", "East Richmond Heights", "North Richmond",
      "San Pablo", "Rollingwood", "El Sobrante", "Tara Hills", "Hercules", "Pinole"]
m2 = ["Albany", "Berkeley", "Oakland","Emeryville", "Piedmont","Alameda"]
m3 = ["San Leandro", "Ashland", "Castro Valley", "San Lorenzo","Fairview","Cherryland", "Hayward"]
m4 = ["Union City", "Newark", "Fremont", "Milpitas"]
m5 = ["Stanford", "Palo Alto", "Pittsburg", "Contra Costa Centre", "Dublin", "San Francisco"]
all_cities = m1 + m2 + m3 + m4 + m5
dic = make_metro_dic()
dic2 = make_city_dic(all_cities)
con = False
unknown = []
remainder = 0
last_bou = None
last_city = None
print("START")
start_time = time.time()
for stop in d:
    if con is True:
        line = stop[1]
        day = stop[2]
        stopname = stop[5]
        entries = float(stop[6])
        exits = float(stop[7])
        both = entries + exits
        lat = float(stop[8])
        lon = float(stop[9])
        lat_str = stop[8]
        lon_str = stop[9]
        point = Point(lon, lat)
        place = point_location(point, cities, last_bou, last_city)
        while place == None:
            #Sometimes AC Transit has imprecise stop coordinates
            #Check identical stop name strings for valid coordinates
            print(f"Cannot find: {line}, {stopname}, {lat}, {lon}")
            for sub_stop in d:
                if stopname in sub_stop[5] or stopname == sub_stop[5]:
                    if lat != sub_stop[8] and lon != sub_stop[9]:
                        print(f"Trying: {sub_stop[5]} {sub_stop[8]} {sub_stop[9]}")
                        point = Point(float(sub_stop[9]), float(sub_stop[8]))
                        place = point_location(point, cities, None, None)
                        if place:
                            town = place[0]
                            print(f"City found: {town}")
                            break
            scalar = 1
            nlat = lat
            nlon = lon
            slat = lat
            slon = lon
            print("Attemping Dragnet Search North and South")
            while place == None:
                # This is likely a regional parks district like Tilden or Joaquin Miller
                # this means we need to start moving around the map to find nearest town
                # I propose moving 2,000 ft East, West North South till a city is found
                feet = 1000.0 * scalar
                #south
                slat -= (float) (feet / 364000)
                point = Point(slon, slat)
                place = point_location(point, cities, None, None)
                #north
                if place == None:
                    nlat += (float) (feet / 364000)
                    point = Point(slon, slat)
                    place = point_location(point, cities, None, None)
                scalar += 1
            print(f"Found. Place is: {place[0]}")
        city = place[0]
        last_bou = place[1] #Save so we dont have to do for-loop linear search, stops are beside each other
        last_city = city
        # All Ridership
        dic["all"][day]["on"] += entries
        dic["all"][day]["off"] += exits
        dic["all"][day]["total"] += both
        if city not in dic2:
            dic2 = add_city_dic(dic2, city)
        dic2[city][day]["on"] += entries
        dic2[city][day]["off"] += exits
        dic2[city][day]["total"] += both  
        if city in m1:
            dic["m1"][day]["on"] += entries
            dic["m1"][day]["off"] += exits
            dic["m1"][day]["total"] += both
        elif city in m2:
            dic["m2"][day]["on"] += entries
            dic["m2"][day]["off"] += exits
            dic["m2"][day]["total"] += both
        elif city in m3:
            dic["m3"][day]["on"] += entries
            dic["m3"][day]["off"] += exits
            dic["m3"][day]["total"] += both
        elif city in m4:
            dic["m4"][day]["on"] += entries
            dic["m4"][day]["off"] += exits
            dic["m4"][day]["total"] += both
        else:
            if city not in unknown:
                print(city)
                unknown.append(city)
            if city not in all_cities:
                all_cities.append(city)
            if day == "Weekday":
                remainder += entries
            #It's far flung commuter San Francisco or Palo Alto etc.
    else:
        i = 0
        for n in stop:
            print(f"{i}.{n}") 
            i+= 1
        con = True
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")
# Re-run again, find which city each stop's in, then divide its exit/entry against the city's aggreagte in dict
print("Writing Back")
# Saving City Ridership Calcs
with open(destfile3, 'w', newline='') as f:
    new_file = [["CITY", "METRO ID", "DAY", "ON", "OFF", "TOTAL"]]
    for city in all_cities:
        for day in ["Weekday", "Saturday", "Sunday"]:
            if city in m1:
                metro = 1
            elif city in m2:
                metro = 2
            elif city in m3:
                metro = 3
            elif city in m4:
                metro = 4
            else:
                metro = 0
            new_file.append([city, metro, day, dic2[city][day]["on"], dic2[city][day]["off"], dic2[city][day]["total"]])
    new_file.append(["all", 0, "Weekday", dic["all"]["Weekday"]["on"], dic["all"]["Weekday"]["off"], dic["all"]["Weekday"]["total"]])
    new_file.append(["all", 0, "Saturday", dic["all"]["Saturday"]["on"], dic["all"]["Saturday"]["off"], dic["all"]["Saturday"]["total"]])
    new_file.append(["all", 0, "Sunday", dic["all"]["Sunday"]["on"], dic["all"]["Sunday"]["off"], dic["all"]["Sunday"]["total"]])
    writer = csv.writer(f)
    writer.writerows(new_file)
    f.close()
#Saving Regional Ridership Calculations by Metro
with open(destfile2, 'w', newline='') as f:
    new_file = [["METRO ID", "DAY", "ON", "OFF", "TOTAL"]]
    for metro in ["m1","m2","m3", "m4", "all"]:
        for day in ["Weekday", "Saturday", "Sunday"]:
            new_file.append([metro, day, dic[metro][day]["on"], dic[metro][day]["off"], dic[metro][day]["total"]])
    writer = csv.writer(f)
    writer.writerows(new_file)
    f.close()
with open(destfile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(d)
    f.close()
print("Finished.")
    
            
