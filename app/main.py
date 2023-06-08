#!/usr/bin/env python3

import os
from typing import Any, Dict, List

from db import unique_phylum, unique_class, unique_order, unique_family, unique_genus, unique_species, unique_environmental_medium, unique_establishment_means, year_range, load_events, load_event_hapstats, load_event_variant_stats
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
def events(
    min_lng: float | None = None, 
    min_lat: float | None = None,
    max_lat: float | None = None, 
    max_lng: float | None = None,
    phylum: str | None = None,
    taxonomic_class: str | None = None,
    taxonomic_order: str | None = None,
    family: str | None = None,
    genus: str | None = None, 
    species: str | None = None,
    habitat: str | None = None,
    country: str | None = None,
    continent_ocean: str | None = None,
    environmental_medium: str | None = None,
    establishment_means: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    db: Session = Depends(get_db)) -> JSONResponse:
    """Query the events_metdata table to load events."""
    
    features = load_events(
        db, 
        min_lng, min_lat, max_lng, max_lat, 
        phylum, taxonomic_class, taxonomic_order, family, genus, species, 
        habitat, country, continent_ocean,
        environmental_medium,
        establishment_means,
        min_year, max_year
    )
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
    return(hapstats)


@app.get("/events/{event_id}/variant_stats")
def event_hapstats(event_id: str, db: Session = Depends(get_db)):
    hapstats = load_event_variant_stats(db, event_id)
    hapstats = [h._asdict() for h in hapstats]
    return(hapstats)


@app.get("/phylum")
def get_phyla(db: Session = Depends(get_db)):
    """Get unique phyla in the database."""
    return unique_phylum(db)

@app.get("/taxonomic_class")
def get_class(db: Session = Depends(get_db)):
    """Get unique taxonomic classes in the database."""
    return unique_class(db)

@app.get("/taxonomic_order")
def get_order(db: Session = Depends(get_db)):
    """Get unique taxonomic orders in the database."""
    return unique_order(db)

@app.get("/family")
def get_family(db: Session = Depends(get_db)):
    """Get unique taxonomic families in the database."""
    return unique_family(db)

@app.get("/genus")
def get_genus(db: Session = Depends(get_db)):
    """Get unique genera in the database."""
    return unique_genus(db)

@app.get("/species")
def get_species(db: Session = Depends(get_db)):
    """Get unique species in the database."""
    return unique_species(db)

@app.get("/environmental_medium")
def get_environmental_medium(db: Session = Depends(get_db)):
    """Get unique environmental media in the database."""
    return unique_environmental_medium(db)

@app.get("/establishment_means")
def get_establishment_means(db: Session = Depends(get_db)):
    """Get unique establishment means in the database."""
    return unique_establishment_means(db)

@app.get("/years")
def get_years(db: Session = Depends(get_db)):
    """Return the min/max collection years in the database."""
    return year_range(db)