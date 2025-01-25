"""Save logs to SQLite Database."""

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from psycopg.types.json import Jsonb

from .db_log import DBLog
from .exceptions import DBSaveError


@dataclass
class SQLiteLog(DBLog):
    connection_info: Path = Path.cwd() / "log.sqlite"

    def save_log(self) -> int:
        try:
            with sqlite3.connect(self.connection_info) as conn:
                cur =  conn.cursor()
                for log_timestamp, log_info in self.logs.items():
                    cur.execute(
                        """
                        insert into logs (entry, program, pc_name, level, message, details)
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
