#!/usr/bin/env python3

import os
from typing import Any, Dict, List

from db import load_events, load_event_hapstats
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg import OperationalError
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = URL.create(
    "postgresql+psycopg",
    username=os.environ['PGUSER'],
    password=os.environ['PGPASS'],
    host=os.environ['PGHOST'],
    database=os.environ['PGDATABASE']
)

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    try:
        if engine.raw_connection().is_valid:
            return {'status': 'OK'}
        else:
            HTTPException(status_code=500, detail="Error connecting to database")
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error connecting to database")

    

@app.get("/events")
def events(min_lng: float, min_lat: float, max_lat: float, max_lng: float,  db: Session = Depends(get_db)) -> JSONResponse:
    """Query the events_metdata table to load events."""
    features = load_events(db, min_lng, min_lat, max_lng, max_lat)
    features = features[0][0]
    response = {
        'type': 'FeatureCollection',
        'features': features
    }

    return JSONResponse(content=jsonable_encoder(response))


@app.get("/events/{event_id}/hapstats")
def event_hapstats(event_id: str, db: Session = Depends(get_db)):
    hapstats = load_event_hapstats(db, event_id)
    hapstats = [h._asdict() for h in hapstats]

    print(hapstats)
    return(hapstats)