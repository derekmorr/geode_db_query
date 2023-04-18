#!/usr/bin/env python3

from typing import List

from db import load_events, load_event_hapstats
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    features = load_events(pool, min_lng, min_lat, max_lng, max_lat)
    response = {
        'type': 'FeatureCollection',
        'features': features['features']
    }

    return JSONResponse(content=jsonable_encoder(response))

@app.get("/events/{event_id}/hapstats")
def event_hapstats(event_id: str):
    hapstats = load_event_hapstats(pool, event_id)
    return(hapstats)
