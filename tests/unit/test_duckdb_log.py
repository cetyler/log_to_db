import pytest
from log_to_db.duckdb_log import DuckDBLog
import duckdb

@pytest.fixture()
def duckdb_log(tmp_path):
    folder_path = tmp_path
    duckdb_path = folder_path / "log.duckdb"
    con = duckdb.connect(f"{duckdb_path}")
    con.execute(
        """
        create table logs
        (
            entry   timestamptz not null default now(),
            program text        not null,
            pc_name text        not null,
            level   int         not null,
            message text        not null,
            details json
        );
        """
    )
    con.execute(
        """
        create table log_levels (
             level int not null
            ,name text not null
        );
        """
    )

    db = DuckDBLog(
        save_level="debug",
        pc_name="test_pc",
        program_name="test_program",
        connection_info=duckdb_path,
    )
    db.load_log_levels()

    yield db


def test_save_log(duckdb_log):
    con = duckdb.connect(f"{duckdb_log.connection_info}")

    assert con.sql("select count(*) from logs").fetchall()[0][0] == 0

    duckdb_log.log(level="info",message="test_message",details=dict(more_info="1st one"))
    duckdb_log.save_log()

    assert con.sql("select count(*) from logs").fetchall()[0][0] == 1

    duckdb_log.log(level="info", message="test_message", details=dict(more_info="2nd one"))
    duckdb_log.save_log()

    assert con.sql("select count(*) from logs").fetchall()[0][0] == 2
