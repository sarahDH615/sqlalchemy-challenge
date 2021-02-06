#dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import pandas as pd
import datetime as dt
#---------------------------------------------------------------------------------------------


# Database Setup
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#---------------------------------------------------------------------------------------------

#creating variables for later use
session = Session(engine)
#getting most recent date
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

#getting one year before most recent date
ld_year = int(latest_date[0][0:4])
ld_month = int(latest_date[0][5:7])
ld_day = int(latest_date[0][-2:])

year_before = (dt.date(ld_year, ld_month, ld_day) - dt.timedelta(days=365)).strftime('%Y-%m-%d')

#getting the most_active_station_id
station_count = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc())
most_active_station_id = station_count[0][0]

#finding acceptable years list
years_list = []
for row in session.query(Measurement.date):
    years_list.append(row[0][0:4])
unique_years_list = sorted(list(set(years_list)))

session.close()

#---------------------------------------------------------------------------------------------

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route('/')
def home():
    print('Server received request for home page...')
    return (
        f'<h3>Welcome to the home page. These are the available routes: </h3><br/>'
        f'/api/v1.0/precipitation: returns dictionary with dates as keys, and precipitation amounts as values, for the last 12 months in the dataset<br/>'
        f'/api/v1.0/stations: returns list of stations <br/>'
        f'/api/v1.0/tobs: returns date and temperature observations for the most active station ({most_active_station_id}) in the dataset<br/>'
        f'/api/v1.0/start: returns list of minimum temperature, maximum temperature and average temperature for a date range between a user-input start date, and the end date of the dataset ({ld_year}-0{ld_month}-{ld_day})<br/>'
        f'/api/v1.0/start/end: returns list of minimum temperature, maximum temperature and average temperature for a user-input start/end date range<br/>'
        f'<h4>Note: for the last two routes, please use the format yyyymmdd, using a zero before a single-digit month or day. The dataset contains information for the years {unique_years_list[0]} to {unique_years_list[-1]}.</h4>'
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    print('Server received request for precipitation page...')
    # Create our session (link) from Python to the DB
    session = Session(engine)

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
    print('Server received request for stations page...')
    session = Session(engine)

    stations_list = []

    for row in session.query(Measurement.station, Station.name).filter(Measurement.station == Station.station).group_by(Station.name):
        stations_list.append(row[1])

    session.close()

    return jsonify(stations_list)  

@app.route('/api/v1.0/tobs')
def temps():
    print('Server received request for temperatures page...')
    session = Session(engine)

    #filling the list of temperatures for the most active station, w/in the last year
    temps_list = []
    for row in session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= year_before):
        temps_list.append(row[0])

    session.close()

    return jsonify(temps_list)  

#route for only start date given
@app.route('/api/v1.0/<start>')
def start_date_lookup(start):
    print('Server received request for start-input temperature data page...')
    session = Session(engine)
    
    #if date format or wrong year is put in, return error message
    if start[0:4] not in unique_years_list:
        return (
            f'error: date not found. Reminder: use yyyymmdd format<br/>'
            f'Years available: {unique_years_list}'
        )
    #reformatting start date
    start_year = str(start)[0:4]
    start_month = str(start)[4:6]
    start_day = str(start)[-2:]
    start_search = dt.date(int(start_year), int(start_month), int(start_day)).strftime('%Y-%m-%d')

    #querying for temps for station id, dates after the start date
    max_temp = session.query(
        func.max(Measurement.tobs)).filter(
            Measurement.station == most_active_station_id, Measurement.date >= start_search
            ).scalar()
    min_temp = session.query(func.min(Measurement.tobs)).filter(
        Measurement.station == most_active_station_id, Measurement.date >= start_search
        ).scalar()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(
        Measurement.station == most_active_station_id, Measurement.date >= start_search
        ).scalar()

    session.close()

    temp_for_station_dict = {
        f'minimum temperature in date range {start_search} to {latest_date[0]}': min_temp,
        f'maximum temperature in date range {start_search} to {latest_date[0]}': max_temp,
        f'average temperature in date range {start_search} to {latest_date[0]}': round(avg_temp, 2)
    }
    return jsonify(temp_for_station_dict)  


#route for start and end dates given
@app.route('/api/v1.0/<start>/<end>')
def full_date_lookup(start, end):
    print('Server received request for start- and end-input temperature data page...')
    session = Session(engine)
    
    #if date format or wrong year is put in, return error message
    if start[0:4] not in unique_years_list:
        return (
            f'error: date not found. Reminder: use yyyymmdd format<br/>'
            f'Years available: {unique_years_list}'
        )

    if end[0:4] not in unique_years_list:
        return (
            f'error: date not found. Reminder: use yyyymmdd format<br/>'
            f'Years available: {unique_years_list}'
        )  
          
    #reformatting start and end dates
    start_year = str(start)[0:4]
    start_month = str(start)[4:6]
    start_day = str(start)[-2:]
    start_search = dt.date(int(start_year), int(start_month), int(start_day)).strftime('%Y-%m-%d')

    end_year = str(end)[0:4]
    end_month = str(end)[4:6]
    end_day = str(end)[-2:]
    end_search = dt.date(int(end_year), int(end_month), int(end_day)).strftime('%Y-%m-%d')

    #querying for temps for station id, btwn the time frames
    max_temp = session.query(
        func.max(Measurement.tobs)).filter(
            Measurement.station == most_active_station_id, Measurement.date >= start_search, Measurement.date >= end_search
            ).scalar()
    min_temp = session.query(func.min(Measurement.tobs)).filter(
        Measurement.station == most_active_station_id, Measurement.date >= start_search, Measurement.date >= end_search
        ).scalar()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(
        Measurement.station == most_active_station_id, Measurement.date >= start_search, Measurement.date >= end_search
        ).scalar()

    session.close()

    temp_for_station_dict = {
        f'minimum temperature in date range {start_search} to {end_search}': min_temp,
        f'maximum temperature in date range {start_search} to {end_search}':max_temp,
        f'average temperature in date range {start_search} to {end_search}': round(avg_temp, 2)
    }
    return jsonify(temp_for_station_dict)  

if __name__ == '__main__':
    app.run(debug=True)