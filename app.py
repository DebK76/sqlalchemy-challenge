# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, desc, distinct, inspect

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
#app.debug = True
#################################################
# Flask Routes

#################################################

# Create welcome route
@app.route("/")
def welcome():

# List all available routes
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
    
# Convert the query results from your precipitation analysis( i.e. retrieve only the last 12 months  of data) to a dictionary using date as the key and prcp as the value
# Return the Json representation of your dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create Session
    session = Session(engine)
   
    # Design a query to retrieve the last 12 months of precipitation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set
    latest_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    start_date = latest_date - dt.timedelta(days=365)

    # Return a list of all precipitation and date
    # Query all precipitation and date
    precipitation_query_results = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date >= start_date).all()
    
    # Convert list into dictionary
    all_precepitation_query_values = []
    for date,prcp in precipitation_query_results:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict['date'] = date
        all_precepitation_query_values.append(precipitation_dict)

    # Close session
    session.close()

    # Return a JSON list of precipitation query values
    return jsonify(all_precepitation_query_values)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():

    # Create Session
    session = Session(engine)

    # Query all distinct station names
    station_names = session.query(Station.station).distinct().all()

    # Convert the query results into a list
    stations_list = [station[0] for station in station_names]

    # Close session
    session.close()

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create Session
    session = Session(engine)

    # Calculate the date one year from the last date in data set
    last_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query the most active station for the temperature observations within the last year
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    
    # Query temperature observations for the most active station for the previous year
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station[0]).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Create a list of dictionaries containing date and temperature observations
    tobs_list = []
    for date, tobs in tobs_results:
        tobs_dict = {"date": date, "tobs": tobs}
        tobs_list.append(tobs_dict)
    
    # Close session
    session.close()

    # Return a JSON list of temperature observations
    return jsonify(tobs_list)   

# Query a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
# For a specified start date and end date, calculate TMIN,TAVG and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):

    # Create Session
    session = Session(engine)
    # Query the minimum, average, and maximum temperature for dates greater than or equal to the start date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Create a dictionary to store the temperature statistics
    temperature_stats_dict = {
        "start_date": start,
        "end_date": None,
        "tmin": temperature_stats[0][0],
        "tavg": temperature_stats[0][1],
        "tmax": temperature_stats[0][2]
    }

    # Close session
    session.close()

    # Return the temperature statistics as JSON
    return jsonify(temperature_stats_dict)

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    # Create Session
    session = Session(engine)
    # Query the minimum, average, and maximum temperature for the specified date range
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary to store the temperature statistics
    temperature_stats_dict = {
        "start_date": start,
        "end_date": end,
        "tmin": temperature_stats[0][0],
        "tavg": temperature_stats[0][1],
        "tmax": temperature_stats[0][2]
    }

    # Close session
    session.close()
    # Return the temperature statistics as JSON
    return jsonify(temperature_stats_dict)

app.run(host='0.0.0.0', port=105) 