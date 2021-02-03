import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    print('Server received request for home page...')
    return (
        f'Welcome to the home page. These are the available routes: <br/>'
        f'/api/v1.0/precipitation: returns dictionary of with dates as keys, and precipitation amount as values, for the last 12 months in the dataset<br/>'
        f'/api/v1.0/stations: returns list of stations <br/>'
        f'/api/v1.0/tobs: returns date and temperature observations for the most active station in the dataset<br/>'
        f'/api/v1.0/<start>: returns list of min temperature, max temperature and average temperature for a given start date range<br/>'
        f'/api/v1.0/<start>/<end>: returns list of min temperature, max temperature and average temperature for a given start/end date range'
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precip and date data for last 12 months 
    #getting most recent date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    #getting one year before most recent date
    year_before = (dt.date(2017, 8, 23) - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #creating the precip dict for display
    prcp_dict = {}
    pdata = session.query(Measurement).filter(Measurement.date >= year_before).all()
    for row in pdata:
        prcp_dict[row.date] = row.prcp

    session.close()

    # Display jsonified dict
    return jsonify(prcp_dict)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    stations_list = []

    for row in session.query(Measurement.station, Station.name).filter(Measurement.station == Station.station).group_by(Station.name):
        stations_list.append(row[1])

    session.close()

    return jsonify(stations_list)  

@app.route('/api/v1.0/tobs')
def temps():
    session = Session(engine)

    #getting most recent date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    #getting one year before most recent date
    year_before = (dt.date(2017, 8, 23) - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #getting the most_active_station_id
    station_activity = session.query(Measurement.station, Measurement.id).group_by(Measurement.station).order_by(Measurement.id.desc())
    most_active_station_id = station_activity[0][0]

    #filling the list of temperatures for the most active station, w/in the last year
    temps_list = []
    for row in session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= year_before):
        temps_list.append(row[0])

    session.close()

    return jsonify(temps_list)  


if __name__ == '__main__':
    app.run(debug=True)