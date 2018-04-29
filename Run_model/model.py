# Importing the libraries
import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM, Activation
# Importing the Keras libraries and packages
from keras.models import Sequential
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# training parameters passed to "model.fit(...)"
from sklearn.preprocessing import MinMaxScaler
import keras.backend as K
import time

start= time.time()
batch_size = 10
epochs = 10

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
			month+=1
	return frame, date, month

def reg_accuracy(y_true, y_pred):
	return K.mean(K.equal(K.round(y_true), K.round(y_pred)))

output= open('E:\code\Run_model\output.csv','w')
datasegmentIdframe= pd.read_csv('E:\code\Run_model\Dataset.csv')
data_segmentId= datasegmentIdframe.values
list_data=[]
for i in range(len(data_segmentId)-1):
	if data_segmentId[i,0]!= data_segmentId[i+1,0]:
		list_data.append(data_segmentId[i])
list_data.append(data_segmentId[len(data_segmentId)-1])


# Importing the dataset
dataframe = pd.read_csv('E:\code\Run_model\data_input.csv')
datasetX = dataframe.values
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(datasetX)

# Transform dataset from data frame to array
input_dataset = dataset[:, 0:3]
output_dataset = dataset[:, 3]

# Splitting the dataset into the Training set and Test set
input_train, input_test, output_train, output_test = train_test_split(input_dataset, output_dataset, test_size=0.2)

input_train = np.reshape(input_train, (input_train.shape[0], 1, 3))
input_test = np.reshape(input_test, (input_test.shape[0], 1, 3))

# Initializing Neural Network
print('Build model...')
lstm = Sequential()
lstm.add(LSTM(100, input_shape=(1, 3), dropout=0.2))
lstm.add(Dense(1))
lstm.add(Activation('linear'))
#lstm.summary()
lstm.compile(optimizer='adam', loss='mse', metrics=[reg_accuracy])
print('Train...')
history = lstm.fit(input_train, output_train, batch_size=batch_size, epochs=epochs,
                   validation_data=(input_test, output_test))
loss, acc = lstm.evaluate(input_test, output_test, batch_size=batch_size)
print('Model loss:', loss)
print('Model acc:', acc)

#train_predict = lstm.predict(input_train)
test_predict = lstm.predict(input_test)
output_test = np.reshape(output_test, (1, test_predict.shape[0])).T
rmse = np.math.sqrt(mean_squared_error(output_test[:, 0], test_predict[:, 0]))
print("RMSE=",rmse)

output.write("segment_Id,speed,frame,date\n")

i=0
while i<len(list_data):
	idx= list_data[i][0]
	frame= list_data[i][2] 
	speedX= list_data[i][1]
	Y= list_data[i][8]
	date= int(Y[0]+Y[1])
	month= int(Y[3] + Y[4])
	year= int(Y[6:])
	#frame, date, month= check_frame(frame,date,count)
	while month<6: 
		datasetX[0,0]=idx
		datasetX[0,1]=frame
		datasetX[0,2]=speedX
		maxSpeed=max(datasetX[:,2])
		minSpeed=min(datasetX[:,2])
		X = scaler.fit_transform(datasetX)
		Y=X[0:3,0:3]
		test_in=np.reshape(Y, (Y.shape[0], 1,3 ))
		test_out= lstm.predict(test_in)
		speedX= round(test_out[0][0]*(maxSpeed-minSpeed) + minSpeed,4)
		frame+=1
		frame, date, month= check_frame(frame,date,month)
		if date<10:
			strdate= "0"+str(date)
		else:
			strdate= str(date)
		if month<10:
			strmonth= "0"+str(month)
		else:
			strmonth= str(month)
		stryear= str(year)
		output.write(str(idx)+","+str(speedX)+","+str(frame)+","+strdate+"/"+strmonth+"/"+stryear+"\n")
		print(frame," ",date,"-",month,"-",year)
	i+=1


output.close()
end= time.time()
print("Time: ", round(end-start,4))

