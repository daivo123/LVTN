# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import datetime
from pymongo import MongoClient
#using mongoDB
Client= MongoClient()

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    X = TextField('lng:', validators=[validators.required()])
    Y = TextField('lat:', validators=[validators.required()])
    time = TextField('time:', validators=[validators.required(), validators.Length(min=5, max=5)])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        x=request.form['lng']
        y=request.form['lat']
        time=request.form['time']
        #print(x, " ", y, " ", time)
            
        if x and y and time:
            db= Client['segmentId']
            dbframe= Client['dataframe']
            dbdata= Client['data']
            #Tìm frame
            hours=time[:2]
            minutes=time[3:5]
            dataframe= list(dbframe.dataframe.find({"hours":int(hours),"minutes":int(minutes)}))
            frame= dataframe[0]["frame"]            
            #lấy ngày hiện tại
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
            #Tìm segmentId
            k=-1
            idx=0
            segmentId= list(db.segmentId.find())
            for i in range(len(segmentId)):
                X=segmentId[i]
                print(str(X['X1'])+" " + str(type(X['X1'])))
                if X['X1']<=round(float(x),7) and round(float(x),7)<= X['X2'] and X['Y1']<=round(float(y),7) and round(float(y),7)<= X['Y2']:
                    k=i
                    idx= X["segment_Id"]
                    break
            #Kiểm tra xem có segmentId hay không        
            if k>=0:
                dataSpeed= list(dbdata.data.find({"segment_Id":idx, "frame":frame, "date": date }))
                speed=round(dataSpeed[0]["speed"],2)
                # Save the comment here.
                flash("Vận tốc tại thời điểm "+ str(hours)+":"+str(minutes)+" ngày "+str(date)+" là: "+str(speed)+" km/h"  )
            else:
                flash('Error: Không tìm được segmentId. ') 
        else:
            flash('Error: Chưa đủ thông tin để dự báo. ')
 
    return render_template('index.html', form=form)
 
if __name__ == "__main__":
    app.run(port=5003)
