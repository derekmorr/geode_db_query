#!/usr/bin/env python3

from typing import List

from db import load_events, load_event_hapstats
from fastapi import FastAPI
from psycopg_pool import ConnectionPool

app = FastAPI()

pool = ConnectionPool()

@app.on_event("startup")
def open_pool():
    if pool is not None:
        pool.open()

def close_pool():
    if pool is not None:
        pool.close()

@app.get("/events")
def events(min_lng: float, min_lat: float, max_lat: float, max_lng: float) -> List:
    """Query the events_metdata table to load events."""
    events = load_events(pool, min_lng, min_lat, max_lng, max_lat)

    # # do this? - do in parallel or avoid n+1?
    # for event in events:
    #     hapstats = load_event_hapstats(pool, event['event_id'])
    #     event['hapstats'] = hapstats

    return(events)

@app.get("/events/hapstats/{event_id}")
def event_hapstats(event_id: str):
    load_event_hapstats = load_event_hapstats(pool, event_id)
    return(load_event_hapstats)
