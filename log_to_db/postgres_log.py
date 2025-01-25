"""Save logs to PostgreSQL Database."""

from dataclasses import dataclass

import psycopg
from psycopg.types.json import Jsonb

from .db_log import DBLog
from .exceptions import DBSaveError


@dataclass
class PostgresLog(DBLog):
    connection_info: str = (
        "postgres://username:userpassword@localhost:5432/raw_test_data"
    )
    schema: str = "programs"

    def save_log(self) -> int:
        try:
            with psycopg.connect(self.connection_info) as conn:
                with conn.cursor() as cur:
                    for log_timestamp, log_info in self.logs.items():
                        cur.execute(
                            f"""
                            insert into {self.schema}.logs (entry, program, pc_name, level, message, details)
                            values (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                str(log_timestamp),
                                log_info["program_name"],
                                log_info["pc_name"],
                                log_info["level"],
                                log_info["message"],
                                Jsonb(log_info["details"]),
                            ),
                        )
                    conn.commit()
                    code = 0
                    self.logs = dict()

        except Exception as err:
            raise DBSaveError(f"Can't write to Database. {err}")
            code = -1

        return code
