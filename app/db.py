from typing import Any, Dict, List


from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from models import *

def load_events(
    db: Session, 
    min_lng: float, min_lat: float, max_lng: float, max_lat: float,
    phylum: Optional[str],
    taxonomic_class: Optional[str],
    taxonomic_order: Optional[str],
    family: Optional[str],
    genus: Optional[str], 
    species: Optional[str],
    habitat: Optional[str],
    country: Optional[str],
    continent_ocean: Optional[str],
    environmental_medium: Optional[str],
    establishment_means: Optional[str],
    min_year: Optional[int],
    max_year: Optional[int]):
    """Load all events in a bounding box"""

    location_params = {
        "min_lng": min_lng, 
        "min_lat": min_lat, 
        "max_lng": max_lng,
        "max_lat": max_lat 
    }

    # XXX: convert to use a spatial query
    features_query = select(EventMetadata)\
                      .join(SampleMetadata)\
                      .where(EventMetadata.decimal_latitude.between(min_lat, max_lat))\
                      .where(EventMetadata.decimal_longitude.between(min_lng, max_lng))
 
    if phylum:
        features_query = features_query.where(SampleMetadata.phylum == phylum)
    
    if taxonomic_class:
        features_query = features_query.where(SampleMetadata.taxonomic_class == taxonomic_class)

    if taxonomic_order:
        features = features_query.where(SampleMetadata.taxonomic_order == taxonomic_order)

    if family:
        features_query = features_query.where(SampleMetadata.family == family)
    
    if genus:
        features_query = features_query.where(SampleMetadata.genus == genus)

    if species:
        features_query = features_query.where(EventMetadata.species == species)
    
    if habitat:
        features_query = features_query.where(EventMetadata.habitat == habitat)

    if country:
        features_query = features_query.where(EventMetadata.country == country)

    if continent_ocean: 
        features_query = features_query.where(EventMetadata.continent_ocean == continent_ocean)

    if environmental_medium:
        features_query = features_query.where(EventMetadata.environmental_medium == environmental_medium)

    if establishment_means:
        features_query = features_query.where(SampleMetadata.establishment_means == establishment_means)

    if min_year:
        features_query = features_query.where(EventMetadata.year_collected >= min_year)

    if max_year:
        features_query = features_query.where(EventMetadata.year_collected <= max_year)

    features_subquery = features_query.subquery("features")

    final_query = select(
        func.json_agg(
            cast(func.ST_AsGeoJSON(features_subquery), JSON)
        )
    ) 

    rs = db.execute(final_query).all()
    return rs


def load_event_hapstats(db: Session, event_id: str):
    results = db.execute(
        text(
            """
            SELECT *
            FROM event_metadata 
            JOIN sample_metadata USING (event_id)
            JOIN datasets USING (dataset_name)
            JOIN stacks_runs ON stacks_runs.stacks_run_name = datasets.r80
            JOIN populations_sumstats_summary_all_positions USING (stacks_run_id)
            WHERE event_metadata.event_id = :event_id
            """
        ),
        { "event_id": event_id }
    )

    return results.fetchall()


def unique_phylum(db: Session) -> List[Optional[str]]:
    """List distinct pyhla in the database"""
    phyla = db.query(SampleMetadata.phylum)\
            .distinct()\
            .all()
    return [p[0] for p in phyla]

def unique_class(db: Session) -> List[Optional[str]]:
    """List distinct classes in the database"""
    classes = db.query(SampleMetadata.taxonomic_class)\
                .distinct()\
                .all()
    return [c[0] for c in classes]

def unique_order(db: Session) -> List[Optional[str]]:
    """List distinct orders in the database"""
    orders = db.query(SampleMetadata.taxonomic_order)\
                .distinct()\
                .all()
    return [o[0] for o in orders]

def unique_family(db: Session) -> List[Optional[str]]:
    """List distinct families in the database"""
    families = db.query(SampleMetadata.family)\
                .distinct()\
                .all()
    return [f[0] for f in families]

def unique_genus(db: Session) -> List[Optional[str]]:
    """List distinct genera in the database"""
    genera = db.query(SampleMetadata.genus)\
                .distinct()\
                .all()
    return [g[0] for g in genera]

def unique_species(db: Session) -> List[Optional[str]]:
    """List distinct species in the database"""
    species =  db.query(SampleMetadata.specific_epithet)\
                .distinct()\
                .all()
    return [s[0] for s in species]

def unique_environmental_medium(db: Session) -> List[Optional[str]]:
    """List distinct environmental media in the database."""
    media = db.query(EventMetadata.environmental_medium)\
                .distinct()\
                .all()
    return [m[0] for m in media]

def unique_establishment_means(db: Session) -> List[Optional[str]]:
    """List distinct establishment means in the database."""
    means = db.query(SampleMetadata.establishment_means)\
                .distinct()\
                .all()
    return [m[0] for m in means]

def year_range(db: Session) -> Dict[str, int]:
    """Return dictionary of min, max collection years in the database."""
    results = db.query(
        func.min(EventMetadata.year_collected),
        func.max(EventMetadata.year_collected)
    ).first()

    return { 'min_year': results[0], 'max_year': results[1] }