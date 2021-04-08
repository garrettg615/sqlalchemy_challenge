# create a web page to display the weather data

# import libraries
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
from flask import Flask, jsonify

##########################
# Data Base Setup
##########################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def homepage():
    print('Server request received for Homepage...')
    return("Welcome to the Definitive API for the weather in Hawaii!!<br/>"
        "Below are the available roots you can visit:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/2017-08-07<br/>"
        "/api/v1.0/2017-08-07/2017-08-17<br/>"
    )

@app.route("/api/v1.0/precipitation")
def percip_page():
    print('Server request received for percipitation')

    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    percip = dict(results)
    return jsonify(percip)

@app.route("/api/v1.0/stations")
def station_page():
    print('Server request received for percipitation')

    session = Session(engine)

    results = session.query(Station.station, Station.name).all()
    session.close()

    station_dict = dict(results)

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def temp_obs_page():
    print('Server request received for percipitation')

    session = Session(engine)

    results = session.query(Measurement.station,func.count(Measurement.id)).group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).all()
    
    most_active = results[1][0]

    station_name = session.query(Station.station,Station.name).filter(Station.station==Measurement.station).\
        filter(Measurement.station==most_active).all()
    stat_name = list(station_name)
        

    tobs_active = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station==most_active).\
        filter(Measurement.date.between('2016-08-19','2017-08-18')).all()

    session.close()

    temp_obs = dict(tobs_active)

    if most_active is True:
        return f'THE MOST ACTIVE WEATHER STATION IS {stat_name[0][1]}<br/>STATION ID: {stat_name[0][0]}<br/><br/>'
    
    return jsonify(temp_obs)

@app.route('/api/v1.0/<start>')
def get_start_date(start):
    session = Session(engine)

    query1 = session.query(Measurement.date,func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    query2 = session.query(Measurement.date,func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    query3 = session.query(Measurement.date,func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    temp_min = dict(query1)
    temp_avg = dict(query2)
    temp_max = dict(query3)

    return jsonify(temp_min,temp_avg,temp_max)

@app.route('/api/v1.0/<start>/<end>')
def get_dates(start,end):
    session = Session(engine)

    query1 = session.query(Measurement.date,func.min(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    query2 = session.query(Measurement.date,func.avg(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    query3 = session.query(Measurement.date,func.max(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()

    session.close()

    temp_min = dict(query1)
    temp_avg = dict(query2)
    temp_max = dict(query3)

    return jsonify(temp_min,temp_avg,temp_max)



if __name__ == "__main__":
    app.run(debug=True)


