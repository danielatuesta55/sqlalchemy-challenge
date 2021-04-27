#Importing dependencies

import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask set up
app= Flask(__name__)

#Flask routes

@app.route("/")
def welcome():
    #List all routes that are available.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    '''
    Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    Return the JSON representation of your dictionary.
    '''
 #Query all dates and prcp from Measurement data set
    session = Session(engine)
    p_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = date_percipation = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= p_year).order_by(Measurement.date)
    session.close()

    precipitation_list = []
    for i in results:
        dict={}
        dict["date"] = i.date
        dict["prcp"] = i.prcp
        precipitation_list.append(dict)
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    session = Session(engine)
    stations = session.query(Station).all()

    session.close()

    # Convert list of tuples into normal list
    stations_list=[]
    for i in stations:
        dict={}
        dict["elevation"] = i.elevation
        dict["longitude"] = i.longitude
        dict["latitude"] = i.latitude
        dict["name"] = i.name
        dict["station"] =i.station
        stations_list.append(dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    #Query the dates and temperature observations of the most active station for the last year of data.
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    # Query all Measurement table
    session = Session(engine)
    temperature = session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)

    session.close()

    temperature_list = []
    for i in temperature:
        dict = {}
        dict["station"] = i.station
        dict["date"] = i.date
        dict["tobs"] = i.tobs
        temperature_list.append(dict)

    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def start(start=None):
    '''
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    '''
    # Query all Stations table
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()

    # close the session to end the communication with the database
    session.close()

    list = []
    for i in results:
        dict = {}
        dict["min"] = i[0]
        dict["avg"] = i[1]
        dict["max"] = i[2]
        list.append(dict)
        
    return jsonify(list)

@app.route("/api/v1.0/<start>/<end>")
def startend(start=None, end=None):
    '''
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    '''
    # Query all Stations table
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    session.close()

    list = []
    for i in results:
        dict = {}
        dict["min"] = i[0]
        dict["avg"] = i[1]
        dict["max"] = i[2]
        list.append(dict)
        
    return jsonify(list)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host = '0.0.0.0' , port = 5000)