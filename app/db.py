from typing import Any, Dict, List

import psycopg
from psycopg.adapt import Loader
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from models import *


class NumericFloatLoader(Loader):
    """Decode PG numeric data into a Python float."""
    def load(self, data):
        return float(data)


def load_events(db: Session, min_lng: float, min_lat: float, max_lng: float, max_lat: float):
    """Load all events in a bounding box"""

    location_params = {
        "min_lng": min_lng, 
        "min_lat": min_lat, 
        "max_lng": max_lng,
        "max_lat": max_lat 
    }

    rs = db.execute(
        text(
            """
            SELECT json_agg(ST_AsGeoJSON(t.*)::json) AS features
            FROM (
                SELECT 
                    event_id, continent_ocean, coordinate_uncertainty_in_meters,
                    country, day_collected,
                    environmental_medium, expedition_code, georeference_protocol,
                    habitat, land_owner, locality, maximum_depth_in_meters,
                    maximum_elevation_in_meters, microhabitat,
                    minimum_depth_in_meters, minimum_elevation_in_meters,
                    month_collected, permit_information, principal_investigator,
                    sampling_protocol, state_province, year_collected,
                    geom
                FROM event_metadata 
                WHERE event_metadata.geom && ST_MakeEnvelope(:min_lng, :min_lat, :max_lng, :max_lat, 4326)
            ) AS t
            """),
        location_params
    )

    return rs.fetchall()

# def load_events2(db: Session, phylum: Optional[str], habitat: Optional[str]) -> List[Any]:
#     stmt = ???
#     return db.query(stmt).all()

# xxx: tighten return type
def load_event_hapstats(db: Session, event_id: str):
#    return db.query(EventMetadata, SampleMetadata, Datasets, StacksRuns, PopulationsSumStatsSummaryAllPositions)\
#         .select_from(EventMetadata)\
#         .join(SampleMetadata)\
#         .join(Datasets)\
#         .join(StacksRuns, StacksRuns.stacks_run_name == Datasets.r80)\
#         .join(PopulationsSumStatsSummaryAllPositions)\
#         .where(EventMetadata.event_id == event_id)\
#         .all()

    rs = db.execute(``
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
