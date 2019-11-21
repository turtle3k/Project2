# FEMA Database

File Name: femadata.sqlite

location: data

path: data/femadata.sqlite



####  https://www.ncdc.noaa.gov/stormevents/ 



Files downloaded from FTP.

NOAA Storm Events Database

1. The occurrence of storms and other significant weather phenomena having sufficient intensity to cause loss of life, injuries, significant property damage, and/or disruption to commerce;
2. Rare, unusual, weather phenomena that generate media attention, such as snow flurries in South Florida or the San Diego coastal area; and
3. Other significant meteorological events, such as record maximum or minimum temperatures or precipitation that occur in connection with another event.

Files are by year.  FIle names are this convention  ex: StormEvents_details-ftp_v1.0_d1995_c20190920.csv



## all_events table

This table is filtered for just the events we want; Flood, Wildfire, Tornado.  This is all events from 2000 - 2018.

Number of records: 74, 246



## events_deaths table

This table is the filtered data of events.  It is events with deaths.

Number of records: 942

## nmbr_events

This is a table of the events we are concerned with and the number of times each event occured in the dataset.







# Create Scripts

```sql
CREATE TABLE all_events (
        PKEY INTEGER NOT NULL, index BIGINT, 
        EPISODE_ID BIGINT, 
        EVENT_ID BIGINT, 
        STATE TEXT, 
        STATE_FIPS FLOAT, 
        YEAR BIGINT, 
        EVENT_TYPE TEXT, 
        INJURIES_DIRECT BIGINT, 
        INJURIES_INDIRECT BIGINT, 
        DEATHS_DIRECT BIGINT, 
        DEATHS_INDIRECT BIGINT, 
        DAMAGE_PROPERTY TEXT, 
        DAMAGE_CROPS TEXT, 
        TOR_F_SCALE TEXT, 
        STATE_ABBRV TEXT, 
        PRIMARY KEY (PKEY"	INTEGE"));

CREATE TABLE events_deaths (
        PKEY INTEGER NOT NULL, 
        index BIGINT, 
        EPISODE_ID BIGINT, 
        EVENT_ID BIGINT, 
        STATE TEXT, 
        STATE_FIPS FLOAT, 
        YEAR BIGINT, 
        EVENT_TYPE TEXT, 
        INJURIES_DIRECT BIGINT, 
        INJURIES_INDIRECT BIGINT, 
        DEATHS_DIRECT BIGINT, 
        DEATHS_INDIRECT BIGINT, 
        DAMAGE_PROPERTY TEXT, 
        DAMAGE_CROPS TEXT, 
        TOR_F_SCALE TEXT, 
        STATE_ABBRV TEXT, PRIMARY KEY (PKEY"	INTEGE"));
        
CREATE TABLE nmbr_events (
        PKEY INTEGER NOT NULL, index BIGINT, 
        STATE TEXT, 
        NMBR_EVENTS BIGINT, 
        STATE_ABBRV TEXT, 
        PRIMARY KEY (PKEY"	INTEGE"));
        
        
CREATE TABLE state_abbrv (
        PKEY INTEGER NOT NULL, 
        index BIGINT, 
        STATE_CAPS TEXT, 
        STATE_TITLE TEXT, 
        STATE_ABBRV TEXT, 
        STATE_APSTYLE TEXT, 
        PRIMARY KEY (PKEY"	INTEGE"));
```



