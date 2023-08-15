from typing import Any, Dict, List


from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from models import *

def load_events(
    db: Session, 
    min_lng: Optional[float], min_lat: Optional[float], 
    max_lng: Optional[float], max_lat: Optional[float],
    phylum: Optional[str],
    taxonomic_class: Optional[List[str]],
    taxonomic_order: Optional[List[str]],
    family: Optional[List[str]],
    genus: Optional[List[str]], 
    species: Optional[List[str]],
    habitat: Optional[List[str]],
    country: Optional[List[str]],
    continent_ocean: Optional[List[str]],
    environmental_medium: Optional[List[str]],
    establishment_means: Optional[List[str]],
    min_year: Optional[int],
    max_year: Optional[int]):
    """Load all events in a bounding box"""

    features_query = select(EventMetadata, SampleMetadata).join(SampleMetadata)

    # XXX: convert to use a spatial query
    if min_lng and max_lng and min_lat and max_lat:
        features_query = features_query\
                          .where(EventMetadata.decimal_latitude.between(min_lat, max_lat))\
                          .where(EventMetadata.decimal_longitude.between(min_lng, max_lng))

    if phylum:
        features_query = features_query.where(SampleMetadata.phylum.in_(phylum))
    
    if taxonomic_class:
        features_query = features_query.where(SampleMetadata.taxonomic_class.in_(taxonomic_class))

    if taxonomic_order:
        features = features_query.where(SampleMetadata.taxonomic_order.in_(taxonomic_order))

    if family:
        features_query = features_query.where(SampleMetadata.family.in_(family))
    
    if genus:
        features_query = features_query.where(SampleMetadata.genus.in_(genus))

    if species:
        features_query = features_query.where(SampleMetadata.specific_epithet.in_(species))
    
    if habitat:
        features_query = features_query.where(EventMetadata.habitat.in_(habitat))

    if country:
        features_query = features_query.where(EventMetadata.country.in_(country))

    if continent_ocean: 
        features_query = features_query.where(EventMetadata.continent_ocean.in_(continent_ocean))

    if environmental_medium:
        features_query = features_query.where(EventMetadata.environmental_medium.in_(environmental_medium))

    if establishment_means:
        features_query = features_query.where(SampleMetadata.establishment_means.in_(establishment_means))

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


def load_event_all_stats(db: Session, event_id: str):
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

def load_event_variant_stats(db: Session, event_id: str):
    results = db.execute(
        text(
            """
            SELECT *
            FROM event_metadata 
            JOIN sample_metadata USING (event_id)
            JOIN datasets USING (dataset_name)
            JOIN stacks_runs ON stacks_runs.stacks_run_name = datasets.r80
            JOIN populations_sumstats_summary_variant_positions USING (stacks_run_id)
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

def unique_habitats(db: Session) -> List[Optional[str]]:
    """List distinct habitats in the database."""
    habitats = db.query(EventMetadata.habitat)\
                .distinct()\
                .all()
    return [h[0] for h in habitats]

def year_range(db: Session) -> Dict[str, int]:
    """Return dictionary of min, max collection years in the database."""
    results = db.query(
        func.min(EventMetadata.year_collected),
        func.max(EventMetadata.year_collected)
    ).first()

    return { 'min_year': results[0], 'max_year': results[1] }
