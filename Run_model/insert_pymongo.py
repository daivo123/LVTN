from pandas import read_csv
import numpy as np
from pymongo import MongoClient
Client= MongoClient()


#insert into data frame  pymongo
def insert_frame():
    dbframe= Client['dataframe']
    h=17
    m=15
    for frameX in range(96):
        frame = {}
        frame['hours'] =h
        frame['minutes'] =m
        frame['frame'] = frameX
        dbframe.dataframe.insert(frame)
        m=(m+15) %60
        if m == 0:
            h = (h+1) % 24

#insert into segmentId pymongo
def insert_segmentId():
    data_segmentId= read_csv("E:\code\Run_model\segment_Id.csv", engine="python")
    data= data_segmentId.values
    dbsegmentId= Client['segmentId']
    for X in data:
        segmentIdX={}
        segmentIdX['segment_Id']= X[0]
        segmentIdX['X1'] = round(min(X[4],X[6]),7)
        segmentIdX['Y1'] = round(min(X[5],X[7]),7)
        segmentIdX['X2'] = round(max(X[4],X[6]),7)
        segmentIdX['Y2'] = round(max(X[5],X[7]),7)
        dbsegmentId.segmentId.insert(segmentIdX)

#insert into data  pymongo
def insert_data():
    dataframe= read_csv("E:\code\Run_model\data.csv", engine="python")
    dataset= dataframe.values
    dbdata= Client['data']
    for X in dataset:
        dataX={}
        dataX['segment_Id']= X[0]
        dataX['speed']= X[1]
        dataX['frame']= X[2]
        dataX['date'] = X[3]
        dbdata.data.insert(dataX)
#insert into dataset pymongo     

insert_frame()
insert_segmentId()
insert_data()

#arrays= list(dbframe.dataframe.find())

