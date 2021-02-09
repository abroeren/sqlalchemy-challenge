import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > "2016-08-23").all()
    precipitation_list = [results]
    session.close()
    
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name, Station.station, Station.elevation).all()
    session.close()

    station_list = []
    for result in results:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['elevation'] = result[2]
        station_list.append(row)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temperatures = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == USC00519281).filter(Measurement.date > 8-23-2016).all()
    session.close()
    return jsonify(temperatures)
    
## Ran out of time.

if __name__ == '__main__':
    app.run(debug=True)