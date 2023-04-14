from typing import Any, Dict, List

import psycopg
from psycopg.adapt import Loader
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


class NumericFloatLoader(Loader):
    """Decode PG numeric data into a Python float."""
    def load(self, data):
        return float(data)


def load_events(pool: ConnectionPool, min_lng: float, min_lat: float, max_lng: float, max_lat: float) -> List[Dict[str, Any]]:
    with pool.connection() as conn:
        conn.adapters.register_loader("numeric", NumericFloatLoader)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT 
                  event_id, continent_ocean, coordinate_uncertainty_in_meters,
                  country, day_collected, decimal_latitude, decimal_longitude,
                  environmental_medium, expedition_code, georeference_protocol,
                  habitat, land_owner, locality, maximum_depth_in_meters,
                  maximum_elevation_in_meters, microhabitat,
                  minimum_depth_in_meters, minimum_elevation_in_meters,
                  month_collected, permit_information, principal_investigator,
                  sampling_protocol, state_province, year_collected,
                  ST_AsGeoJSON(geom) AS geom
                FROM event_metadata 
                WHERE event_metadata.geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                """,
               (min_lng, min_lat, max_lng, max_lat)
            )

            results = cur.fetchall()
            print(f"load_events found {len(results)} results")
            return results

def load_events_gj(pool: ConnectionPool, min_lng: float, min_lat: float, max_lng: float, max_lat: float) -> List[Dict[str, Any]]:
    with pool.connection() as conn:
        conn.adapters.register_loader("numeric", NumericFloatLoader)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT json_build_object(
                  'type', 'FeatureCollection',
                  'features', json_agg(ST_AsGeoJSON(t.*)::json)
                ) AS result
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
                  WHERE event_metadata.geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                  LIMIT 2
                ) AS t
                """,
               (min_lng, min_lat, max_lng, max_lat)
            )

            results = cur.fetchone()
            print(results)
            return results

def load_event_hapstats(pool: ConnectionPool, event_id: str) -> List[Dict[str, Any]]:
    with pool.connection() as conn:
        conn.adapters.register_loader("numeric", NumericFloatLoader)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *
                FROM event_metadata 
                JOIN sample_metadata USING (event_id)
                JOIN datasets USING (dataset_name)
                JOIN stacks_runs ON stacks_runs.stacks_run_name = datasets.r80
                JOIN populations_sumstats_summary_all_positions USING (stacks_run_id)
                WHERE event_metadata.event_id = %s
                """,
                (event_id,)
            )
            results = cur.fetchall()
            return results


