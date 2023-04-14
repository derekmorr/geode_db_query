from dataclasses import dataclass
import os
from typing import Optional

@dataclass(frozen=True)
class DBConfig:
    host: str
    port: int
    db: str
    user: str
    password: str

    def to_url(self) -> str:
        """Return a postgres connection URL"""
        return f"postgresql://{self.user}:{self.password}"


def load_db_config_from_environ() -> Optional[DBConfig]:
    """
    Try to load the database configuration
    using environment variables. If they are not
    set, return None.
    """
    keys = ['PGHOST', 'PGDATABASE', 'PGUSER', 'PGPASSWORD']
    if not all(key in os.environ for key in keys):
        missing_keys = [key for key in keys if not key in os.environ]
        print("Missing environment variables for", ", ".join(missing_keys))
        return None
    
    return DBConfig(
        host = os.environ['PGHOST'],
        port = int(os.environ.get('PGPORT', '5432')),
        db = os.environ['PGDATABASE'],
        user = os.environ['PGUSER'],
        password = os.environ['PGPASSWORD']
    )