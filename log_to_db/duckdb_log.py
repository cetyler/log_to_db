"""Save logs to SQLite Database."""

from dataclasses import dataclass
from pathlib import Path

import duckdb
from psycopg.types.json import Jsonb

from .db_log import DBLog
from .exceptions import DBSaveError


@dataclass
class DuckDBLog(DBLog):
    connection_info: Path = Path.cwd() / "log.duckdb"

    def save_log(self) -> int:
        try:
            with duckdb.connect(f"{self.connection_info}") as conn:
                with conn.cursor() as cur:
                    for log_timestamp, log_info in self.logs.items():
                        cur.execute(
                            """
                            insert into logs (entry, program, pc_name, level, message, details)
                            values (?, ?, ?, ?, ?, ?)
                            """,
                            (
                                str(log_timestamp),
                                log_info["program_name"],
                                log_info["pc_name"],
                                log_info["level"],
                                log_info["message"],
                                log_info["details"],
                            ),
                        )
                    conn.commit()
                    code = 0
                    self.logs = dict()

        except Exception as err:
            raise DBSaveError(f"Can't write to Database. {err}")
            code = -1

        return code
