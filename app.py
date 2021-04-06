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
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def percip_page():
    print('Server request received for percipitation')

    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    percip = list(np.ravel(results))
    return jsonify(percip)


if __name__ == "__main__":
    app.run(debug=True)


