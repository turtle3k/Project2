import os

import pandas as pd
import numpy as np

# import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/femadata.sqlite"
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

@app.route("/api/disasters/", methods=['GET'])
def disasters():
    # x = Base.classes.nmbr_events
    luState = request.args.get('state')

    print(db.session.query(Nmbr_Events.STATE).all())
    sel = [Nmbr_Events.STATE, Nmbr_Events.NMBR_EVENTS]
    # session = Session(engine)
    if not luState: # - an empty param luState will evaluate to True
        results = db.session.query(*sel).all()  #.order_by(Nmbr_Events.STATE.desc()).all()
    else:
        # The must be a state to match on.
        results = db.session.query(*sel).filter(Nmbr_Events.STATE == luState).all()


    # session.close()

    print(results)

    all_results = []
    for s, e in results:
        results_dict = {}
        results_dict["state"] = s
        results_dict["number_events"] = e
        all_results.append(results_dict)
    
    return jsonify(all_results)


   

@app.route("/pieinfo" , methods=['GET'])
def pieinfo():
    #SELECT  EVENT_TYPE, count(EVENT_TYPE) as NBR_EVENT FROM all_events
    #GROUP BY EVENT_TYPE;

    # Get the passed in state
    luState = request.args.get("state")

    sel = [
        All_Events.EVENT_TYPE
    ]
    
    if not luState: # evaluates to true if luState is empty
        print('pieinfo: Is Empty')
        ttleventcounts = db.session.query(*sel, func.count(All_Events.EVENT_TYPE)).group_by(All_Events.EVENT_TYPE).all()
    else:
        print('pieinfo: NOT Empty')
        ttleventcounts = db.session.query(*sel, func.count(All_Events.EVENT_TYPE)).filter(All_Events.STATE == luState).group_by(All_Events.EVENT_TYPE).all()



    print(ttleventcounts)
    pieinfo = []
    for e, c in ttleventcounts:
        pie_dict = {}
        pie_dict["EVENT_TYPE"] = e
        pie_dict["NBR_EVENT"] = c
        pieinfo.append(pie_dict)
    
    return jsonify(pieinfo)

@app.route("/lineinfo", methods=['GET'])
def lineinfo():
    #SELECT YEAR, EVENT_TYPE, (SUM(DEATHS_DIRECT) + sum(DEATHS_INDIRECT)) as DEATHS  FROM all_events
    #GROUP BY  YEAR, EVENT_TYPE;

    
    luState = request.args.get('state')


    sel = [
        All_Events.YEAR,
        All_Events.EVENT_TYPE
    ]

    if not luState: # - an empty param luState will evaluate to True
        deathinfo = db.session.query(*sel, (func.sum(All_Events.DEATHS_DIRECT) + func.sum(All_Events.DEATHS_INDIRECT)).label("DEATHS")).group_by(All_Events.YEAR, All_Events.EVENT_TYPE)
    else:
        deathinfo = db.session.query(*sel, (func.sum(All_Events.DEATHS_DIRECT) + func.sum(All_Events.DEATHS_INDIRECT)).label("DEATHS")).filter(All_Events.STATE == luState).group_by(All_Events.YEAR, All_Events.EVENT_TYPE)

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
