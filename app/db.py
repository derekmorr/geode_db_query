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
    continent_ocean: Optional[str]):
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

    features_subquery = features_query.subquery("features")

    final_query = select(
        func.json_agg(
            cast(func.ST_AsGeoJSON(features_subquery), JSON)
        )
    ) 

    rs = db.execute(final_query).all()
    return rs


def load_event_hapstats(db: Session, event_id: str):
#    return db.query(EventMetadata, SampleMetadata, Datasets, StacksRuns, PopulationsSumStatsSummaryAllPositions)\
#         .select_from(EventMetadata)\
#         .join(SampleMetadata)\
#         .join(Datasets)\
#         .join(StacksRuns, StacksRuns.stacks_run_name == Datasets.r80)\
#         .join(PopulationsSumStatsSummaryAllPositions)\
#         .where(EventMetadata.event_id == event_id)\
#         .all()

    rs = db.execute(
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

    return rs.fetchall()
