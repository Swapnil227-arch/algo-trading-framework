
import csv
from dateutil import parser
from tabulate import tabulate

file1 = 'output1.csv'
file2 = 'output2.csv'

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data


data1 = read_csv(file1)
data2 = read_csv(file2)

merged_data = data1 + data2

def parse_time(row):
    time_str = row[1]
    return parser.isoparse(time_str)

sorted_data = sorted(merged_data, key=parse_time)

netp = 0.0
for i in range(0,len(sorted_data)):
    netp += float(sorted_data[i][10])
    sorted_data[i].append(netp)
#print(tabulate(sorted_data, headers=['SNO', 'Time', 'Open', 'High', 'Low', 'Close', 'Status', 'Target Profit', 'Stop Loss', 'Lot Size', 'Profit/Loss', 'Net Profit'],tablefmt='grid'))

finalprof = float(sorted_data[len(sorted_data)-1][11])

maxloss = finalprof
starttime = sorted_data[0][1]
endtime = sorted_data[len(sorted_data)-1][1]
for i in range(0,len(sorted_data)):
    for j in range(i+1,len(sorted_data)):
        if float(sorted_data[j][11])-float(sorted_data[i][11])<maxloss:
            maxloss = float(sorted_data[j][11])-float(sorted_data[i][11])
            starttime = sorted_data[i][1]
            endtime = sorted_data[j][1]
            
startdate = sorted_data[0][1][0:10]
maxdailyloss = 0.0
dayloss = 0.0
losday = startdate
for i in range(0,len(sorted_data)):
    curdate = sorted_data[i][1][0:10]
    if(curdate==startdate):
        dayloss+= float(sorted_data[i][10])
    else:
        if dayloss<-1100:
            print(f"Daily loss is {dayloss} at {startdate}\n")
        if dayloss<maxdailyloss:
            maxdailyloss = dayloss
            losday = startdate
        dayloss = float(sorted_data[i][10])
        startdate = curdate
if dayloss<maxdailyloss:
    maxdailyloss = dayloss
    losday = startdate

print("Maximum loss is ",maxloss," if the trade starts at  ",starttime," and maxloss is achieved at ", endtime)
print("Max daily loss is ", maxdailyloss, " on ", losday)
print("net profit is ",sorted_data[-1][-1])