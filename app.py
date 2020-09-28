# -*- coding: utf-8 -*-

import os
import ibm_db
import ibm_db_dbi
from flask import Flask,render_template, request  
       
app = Flask(__name__)    
         
ibm_db_conn =  ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=XXX;PWD=XXX;", "", "")
conn = ibm_db_dbi.Connection(ibm_db_conn)

@app.route("/")                   
def hello(): 
      return render_template('index.html')

@app.route("/lareq", methods=['GET','POST'])                   # at the end point /
def search(): 
      num = request.form['num']
      curr= conn.cursor()
      query= "SELECT PLACE, MAG FROM EQDATA ORDER BY MAG DESC LIMIT {};".format(num)
      curr.execute(query)
      data= curr.fetchall()
      return render_template('display.html', col1="Place",col2="Mag",data = data )

@app.route("/daterange", methods=['POST'])                   
def daterange(): 
      date1 = request.form['date1']
      date2 = request.form['date2']
      curr= conn.cursor()
      query= "SELECT COUNT(PLACE) FROM EQDATA WHERE MAG >3 AND TIME BETWEEN '{}' AND '{}';".format(date1,date2)
      curr.execute(query)
      data= curr.fetchall()
      for row in data:
          num=row[0]
      return str(num) + " quakes greater than 3 on Richter scale between " + date1 + " and " + date2

@app.route("/ricrange", methods=['POST'])                   
def ricrange(): 
      num1 = request.form['num1']
      curr= conn.cursor()
      query= "SELECT RANGE, COUNT(*) FROM (SELECT CASE WHEN MAG BETWEEN 1.0 AND 2.0 THEN '1.0 TO 2.0'"
      query+= " WHEN MAG BETWEEN 2.1 AND 3.0 THEN '2.1 TO 3.0' WHEN MAG BETWEEN 3.1 AND 4.0 THEN '3.1 TO 4.0'"
      query+= " WHEN MAG BETWEEN 4.1 AND 7.0 THEN '4.1 TO 7.0' ELSE  '7.1 TO 10' END AS RANGE"
      query+= " FROM (SELECT *  FROM EQDATA  WHERE TIMESTAMPDIFF(16, CHAR(NOW() - TIME)) < {} ORDER BY TIME ASC)) GROUP BY RANGE;".format(num1)
      curr.execute(query)
      data= curr.fetchall()
      return render_template('display.html', col1="Range",col2="Count",data = data )

@app.route("/dist", methods=['POST'])                   
def dist(): 
      dist = request.form['dist']
      curr= conn.cursor()
      query= "SELECT PLACE, MAG FROM EQDATA WHERE 6371*2 * ASIN(SQRT(POWER(SIN((RADIANS(LATITUDE) - RADIANS(32.8))/2), 2)+ COS(RADIANS(32.8))* COS(RADIANS(LATITUDE)) * POWER(SIN((RADIANS(LONGITUDE) -RADIANS(-96.8))/2),2))) <{}".format(dist)
      curr.execute(query)
      data= curr.fetchall()
      return render_template('display.html', col1="Place",col2="Mag",data = data )

@app.route("/distComp", methods=['POST'])                   
def distComp(): 
      dist = request.form['dist']
      curr= conn.cursor()
      query= "SELECT COUNT(PLACE) FROM EQDATA WHERE 6371*2 * ASIN(SQRT(POWER(SIN((RADIANS(LATITUDE) - RADIANS(61))/2), 2)+ COS(RADIANS(61))* COS(RADIANS(LATITUDE)) * POWER(SIN((RADIANS(LONGITUDE) -RADIANS(-150))/2),2))) <{}".format(dist)
      curr.execute(query)
      data1= curr.fetchall()
      query2= "SELECT COUNT(PLACE) FROM EQDATA WHERE 6371*2 * ASIN(SQRT(POWER(SIN((RADIANS(LATITUDE) - RADIANS(32.8))/2), 2)+ COS(RADIANS(32.8))* COS(RADIANS(LATITUDE)) * POWER(SIN((RADIANS(LONGITUDE) -RADIANS(-96.8))/2),2))) <{}".format(dist)
      curr.execute(query2)
      data2= curr.fetchall()
      for row in data1 :
          count1= row[0]  
      for row in data2 :
            count2= row[0]   
      if count1 > count2 :
            result = "Anchorage"
      else:
            result = "Dallas"
      return "Quakes are more common in " + result

@app.route("/largesteq", methods=['POST'])                   
def largesteq(): 
      dist = request.form['dist']
      curr= conn.cursor()
      query= "SELECT PLACE FROM EQDATA WHERE  6371*2 * ASIN(SQRT(POWER(SIN((RADIANS(LATITUDE) - RADIANS(32.8))/2), 2)+ COS(RADIANS(32.8))* COS(RADIANS(LATITUDE)) * POWER(SIN((RADIANS(LONGITUDE) -RADIANS(-96.8))/2),2))) <{} ORDER BY MAG ASC".format(dist)
      curr.execute(query)
      data= curr.fetchall()
      for row in data:
          place=row[0]
      return "Largest quake within " + dist + "km of Dallas occured in " + place

@app.route("/lareqweek", methods=['POST'])                   
def lareqweek(): 
      dist = request.form['dist']
      curr= conn.cursor()
      query= "SELECT PLACE,MAG FROM (SELECT *  FROM EQDATA  WHERE TIMESTAMPDIFF(16, CHAR(NOW() - TIME)) < 7 ORDER BY TIME ASC)"
      query+= " WHERE  6371*2 * ASIN(SQRT(POWER(SIN((RADIANS(LATITUDE) - RADIANS(32.729641))/2), 2)+ COS(RADIANS(32.729641))* COS(RADIANS(LATITUDE)) * POWER(SIN((RADIANS(LONGITUDE) -RADIANS(-97.110566))/2),2))) <{} ORDER BY MAG ASC".format(dist)
      curr.execute(query)
      data= curr.fetchall()
      for row in data:
          place=row[0]
      return "Largest quake within " + dist + "km of Arlington occured within a week is " + place

@app.route("/cloeqmag", methods=['POST'])                   
def cloeqmag(): 
      num = request.form['num']
      curr= conn.cursor()
      query= "SELECT PLACE,TIME FROM EQDATA WHERE MAG>{} ORDER BY 6371*2 * ASIN(SQRT(POWER(SIN((RADIANS(LATITUDE) - RADIANS(32.729641))/2), 2)+ COS(RADIANS(32.729641))* COS(RADIANS(LATITUDE)) * POWER(SIN((RADIANS(LONGITUDE) -RADIANS(-97.110566))/2),2))) DESC".format(num)
      curr.execute(query)
      data= curr.fetchall()
      for row in data:
          place=row[0]
          tim=row[1]
      return "Closet quake occured with magnitude: " + num + " at place " + place + " at time " + str(tim)
  
@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return render_template('500.html')


port = int(os.getenv('PORT', '5000'))
app.run(host='0.0.0.0', port=port)  