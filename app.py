import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

#Create engine using hawaii.sqlite database file
engine = create_engine("sqlite:///hawaii.sqlite")

#Declare a base
Base = automap_base()

#Use the base class to reflect the database tables
Base.prepare(engine, reflect=True)

# save a reference to those classes
Station = Base.classes.stations
Measurement = Base.classes.measurements

# create a session
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return temperature observation from last year"""
    # Query for the dates and temperature observations from the last year.
    year_ago = dt.date.today() - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
                                filter(Measurement.date >= year_ago).all()

    # Create a dictionary from the raw data and append to a list of all_temperatures
    precip = {date: prcp for date, prcp in results}
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return list of all stations"""
    #Return a json list of stations from the dataset
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Retun the list of temperature observations from last year"""
    #Retunr a json list of Temperature Observations (tobs) for the previous year
    
    year_ago = dt.date.today() - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
                                filter(Measurement.station == 'USC00519281').\
                                filter(Measurement.date >= year_ago).all()
    temp = list(np.ravel(results))
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start=None, end=None):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
                                    filter (Measurement.date>=start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
                                    filter (Measurement.date>=start).\
                                    filter (Measurement.date <=end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
   

if __name__ == '__main__':
    app.run(debug=True)