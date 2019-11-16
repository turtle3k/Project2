import os

import pandas as pd
import numpy as np

# import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/femadata.sqlite"
db = SQLAlchemy(app)
# engine = create_engine("sqlite:///data/femadata.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
# Base.prepare(db.engine, reflect=True)
Base.prepare(db.engine, reflect=True)

# Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples
All_Events = Base.classes.all_events
Event_Deaths = Base.classes.events_deaths
Nmbr_Events = Base.classes.nmbr_events
State_Abbrv = Base.classes.state_abbrv
# print(Nmbr_Events)
# print(db.session.query(Nmbr_Events.STATE).all())

@app.route("/")
def index():
    print("This should print in the console")
    """Return the homepage."""
    return render_template("index.html")

@app.route("/api/disasters")
def disasters():
    x = Base.classes.nmbr_events
    print(db.session.query(Nmbr_Events.STATE).all())
    sel = [Nmbr_Events.STATE, Nmbr_Events.NMBR_EVENTS]
    # session = Session(engine)
    results = db.session.query(*sel).all()  #.order_by(Nmbr_Events.STATE.desc()).all()
    # session.close()

    print(results)

    all_results = []
    for s, e in results:
        results_dict = {}
        results_dict["state"] = s
        results_dict["number_events"] = e
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
    # stmt = db.session.query(Nmbr_Events).statement
    # df = pd.read_sql_query(stmt, db.session.bind)

    # state_data = df.loc[df[STATE] = state,] [STATE, "YEAR", "EVENT_TYPE"]]

    # state_data.sort_values(by=STATE, ascending=False, inplace=True)

    # state = {
    #     "state": state_data.STATE.tolist(),
    #     "year": state_data.YEAR.values.tolist(),
    #     "event_type": state_data.EVENT_TYPE.tolist(),
    # }
    # print(state)
    # return jsonify(state)

    sel = [
        All_Events.STATE,
        All_Events.YEAR,
        All_Events.EVENT_TYPE,
        All_Events.DEATHS_DIRECT,
        All_Events.DEATHS_INDIRECT
    ]

    results = db.session.query(*sel).filter(All_Events.STATE == state).all()

    state_events = {}
    for result in results:
        state_events["STATE"] = result[0]
        state_events["YEAR"] = result[1]
        state_events["EVENT_TYPE"] = result[2]
        state_events["DEATHS_DIRECT"] = result[3]
        state_events["DEATHS_INDIRECT"] = result[4]

    print(state_events)
    return jsonify(state_events)
   

@app.route("/pieinfo")
def pieinfo():
    #SELECT  EVENT_TYPE, count(EVENT_TYPE) as NBR_EVENT FROM all_events
    #GROUP BY EVENT_TYPE;
    sel = [
        All_Events.EVENT_TYPE
    ]
    # session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()
    # ttlfloods = db.session.query(*sel, func.count(All_Events.EVENT_TYPE)).group_by(All_Events.EVENT_TYPE).all()
    ttleventcounts = db.session.query(*sel, func.count(All_Events.EVENT_TYPE)).group_by(All_Events.EVENT_TYPE).all()
    # ttltornados = db.session.query(*sel).filter(All_Events.EVENT_TYPE == "Tornado").all().count(All_Events.EVENT_TYPE)
    # ttlwildfires = db.session.query(*sel).filter(All_Events.EVENT_TYPE == "Wildfire").all().count(All_Events.EVENT_TYPE)

    # pieinfo = {
        # "EVENT_TYPE": ttleventcounts[0],
        # "tornados": ttltornados,
        # "wildfires": ttlwildfires,
    # }
    print(ttleventcounts)
    pieinfo = []
    for e, c in ttleventcounts:
        pie_dict = {}
        pie_dict["EVENT_TYPE"] = e
        pie_dict["NBR_EVENT"] = c
        pieinfo.append(pie_dict)
    
    return jsonify(pieinfo)

@app.route("/lineinfo")
def lineinfo():
    #SELECT YEAR, EVENT_TYPE, (SUM(DEATHS_DIRECT) + sum(DEATHS_INDIRECT)) as DEATHS  FROM all_events
    #GROUP BY  YEAR, EVENT_TYPE;
    sel = [
        All_Events.YEAR,
        All_Events.EVENT_TYPE
    ]
    deathinfo = db.session.query(*sel, (func.sum(All_Events.DEATHS_DIRECT) + func.sum(All_Events.DEATHS_INDIRECT)).label("DEATHS")).group_by(All_Events.YEAR, All_Events.EVENT_TYPE)
    print(deathinfo)

    lineinfo = []
    for year, t, d in deathinfo:
        deaths_dict = {}
        deaths_dict["YEAR"] = year
        deaths_dict["EVENT_TYPE"] = t
        deaths_dict["DEATHS"] = d
        lineinfo.append(deaths_dict)

    # return jsonify(lineinfo)
    return jsonify(lineinfo)

if __name__ == "__main__":
    app.run(debug=True)
