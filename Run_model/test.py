
'''
import pandas as pd

def count_date(month):
	if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
		return 31
	elif month==4 or month==6 or month==9 or month==11:
			return 30
	else:
		return 28

def check_frame(frame,date,month):
	if frame>95:
		frame=0
		date +=1
		if date > count_date(month):
			date=1
			month+1
	return frame, date, month

dataset= pd.read_csv('E:\code\Run_model\Dataset.csv')
data= dataset.values
data_segmentId=[]
for i in range(len(data)-1):
	if data[i,0]!= data[i+1,0]:
		data_segmentId.append(data[i])
data_segmentId.append(data[len(data)-1])

for X in data_segmentId:
	frame= X[2]
	speed= X[1]
	Y= X[8]
	date= int(Y[0]+Y[1])
	month= int(Y[3] + Y[4])
	#print(str(frame) + " " + str(speed)+" "+ str(date)+" "+ str(month))

for X in data_segmentId:
	print(X)
print(len(data_segmentId))
'''
from datetime import datetime
now = datetime.now()

if int(now.month)<10:
	month= "0" + str(now.month)
else:
	month= str(now.month)
if int(now.day) < 10:
	day= "0" + str(now.day)
else:
	day= str(now.day)
date= day + "/" + month + "/" + str(now.year)
print(date)
