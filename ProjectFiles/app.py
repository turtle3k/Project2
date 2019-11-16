import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/femadata.sqlite"
# db = SQLAlchemy(app)
engine = create_engine("sqlite:///data/femadata.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
# Base.prepare(db.engine, reflect=True)
Base.prepare(engine, reflect=True)

# Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples
All_Events = Base.classes.all_events
Event_Deaths = Base.classes.events_deaths
Nmbr_Events = Base.classes.nmbr_events
State_Abbrv = Base.classes.state_abbrv


@app.route("/")
def index():
    print("This should print in the console")
    """Return the homepage."""
    return render_template("index.html")

@app.route("/api/test")
def test():
    session = Session(engine)
    results = session.query(Nmbr_Events.STATE, Nmbr_Events.NMBR_EVENTS).order_by(Nmbr_Events.STATE.desc()).all()
    session.close()

    all_results = []
    for STATE, Nmbr_Events in results:
        results_dict = {}
        results_dict["state"] = STATE
        results_dict["number_events"] = Nmbr_Events
        all_results.append(results_dict)
    
    return jsonify(all_results)

# @app.route("/names")
# def names():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])


# @app.route("/metadata/<state>")
# def state_metadata(state):
#     """Return the MetaData for a given state."""
#     sel = [
#         Nmbr_Events.STATE,
#         Nmbr_Events.NMBR_EVENTS,
#         Nmbr_Events.STATE_ABBRV,
#     ]

#     results = db.session.query(*sel).filter(Nmbr_Events.STATE == state).all()

#     # Create a dictionary entry for each row of metadata information
#     state_metadata = {}
#     for result in results:
#         state_metadata["STATE"] = result[0]
#         state_metadata["NMBR_EVENTS"] = result[1]
#         state_metadata["STATE_ABBRV"] = result[2]
        
#     print(state_metadata)
#     return jsonify(state_metadata)


# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)

@app.route("/events/<state>")
def events(state):
    sel = [
        All_Events.STATE,
        All_Events.YEAR,
        All_Events.EVENT_TYPE,
        All_Events.INJURIES_DIRECT
    ]

    results = db.session.query(*sel).filter(All_Events.STATE == state).all()

    state_events = {}
    for result in results:
        state_events["STATE"] = result[0]
        state_events["YEAR"] = result[1]
        state_events["EVENT_TYPE"] = result[2]
        state_events["INJURIES_DIRECT"] = result[3]

    print(state_events)
    return jsonify(state_events)


if __name__ == "__main__":
    app.run()
