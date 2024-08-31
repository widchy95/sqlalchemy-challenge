# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform a query to retrieve the last 12 months of precipitation data
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Perform a query to retrieve all stations
    results = session.query(Station.station, Station.name).all()
    
    # Convert the query results to a list of dictionaries
    stations_list = [{"station": station, "name": name} for station, name in results]
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Perform a query to retrieve the last 12 months of temperature observation data for the most active station
    most_active_station_id = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a list of dictionaries
    tobs_list = [{"date": date, "temperature": tobs} for date, tobs in temperature_data]
    
    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)
