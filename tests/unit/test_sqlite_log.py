import pytest
from log_to_db.sqlite_log import SQLiteLog
import sqlite3

@pytest.fixture()
def sqlite_log(tmp_path):
    folder_path = tmp_path
    sqlite_path = folder_path / "log.sqlite"
    con = sqlite3.connect(f"{sqlite_path}")
    con.execute(
        """
        create table logs
        (
            entry   text not null,
            program text        not null,
            pc_name text        not null,
            level   int         not null,
            message text        not null,
            details text
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

    db = SQLiteLog(
        save_level="debug",
        pc_name="test_pc",
        program_name="test_program",
        connection_info=sqlite_path,
    )
    db.load_log_levels()

    yield db


def test_save_log(sqlite_log):
    con = sqlite3.connect(f"{sqlite_log.connection_info}")

    assert con.execute("select count(*) from logs;").fetchall()[0][0] == 0

    sqlite_log.log(level="info", message="test_message", details=dict(more_info="1st one"))
    sqlite_log.save_log()

    assert con.execute("select count(*) from logs;").fetchall()[0][0] == 1

    sqlite_log.log(level="info", message="test_message", details=dict(more_info="2nd one"))
    sqlite_log.save_log()

    assert con.execute("select count(*) from logs;").fetchall()[0][0] == 2
