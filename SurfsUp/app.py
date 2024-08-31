# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create an instance of Flask
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation Data</a><br/>"
        f"<a href='/api/v1.0/stations'>Station List</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observations</a><br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Retrieve the most recent date and calculate the date one year ago
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Query for precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert to dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query for all stations
    results = session.query(Station.station, Station.name).all()
    
    # Convert to list of dictionaries
    stations_list = [{"station": station, "name": name} for station, name in results]
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most active station
    most_active_station_id = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    # Retrieve the most recent date and calculate the date one year ago
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Query for temperature data
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert to list of dictionaries
    tobs_list = [{"date": date, "temperature": tobs} for date, tobs in temperature_data]
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    # Query for temperature statistics from the start date
    results = session.query(func.min(Measurement.tobs), 
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    
    # Convert results to dictionary
    stats = [{"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}]
    
    return jsonify(stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Query for temperature statistics between start and end dates
    results = session.query(func.min(Measurement.tobs), 
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end).all()
    
    # Convert results to dictionary
    stats = [{"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}]
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
