"""Test PostgreSQL Logging

This will require having PostgreSQL install on your development machine.
This will read a .env file to get the login credentials.
There is an env_sample that you can to modify for your credentials.
"""

import psycopg
import pytest
from dotenv import load_dotenv
import os
from log_to_db.postgres_log import PostgresLog
import duckdb
import socket

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_DATABASE")

connection_info = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def is_postgres_available():
    """Check if Postgres is available"""
    status = False
    timeout = 2
    try:
        with socket.create_connection((db_host, int(db_port)),timeout=timeout):
            status = True
    except OSError:
        status = False

    return status

@pytest.fixture()
def postgres_log():
    with psycopg.connect(connection_info) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """create schema if not exists log_to_db;"""
            )
            cur.execute(
                """drop table if exists log_to_db.logs;"""
            )
            cur.execute(
                """create table log_to_db.logs (
                     entry timestamptz not null default now()
                    ,program text not null
                    ,pc_name text not null
                    ,level int not null
                    ,message text not null
                    ,details jsonb null
                );"""
            )
            cur.execute(
                """create table log_to_db.log_levels (
                     level int not null
                    ,name text not null
                );"""
            )
            cur.execute(
                """insert into log_to_db.log_levels (level, name) values
                     (10, 'debug')
                    ,(20, 'info')
                    ,(30, 'warning')
                    ,(40, 'error')
                    ,(50, 'critical');"""
            )

    db = PostgresLog(
        save_level="debug",
        pc_name="test_pc",
        program_name="test_program",
        connection_info=connection_info,
        schema="log_to_db",
    )
    db.load_log_levels()
    yield db
    with psycopg.connect(connection_info) as conn:
        with conn.cursor() as cur:
            cur.execute("""drop table if exists log_to_db.logs;""")
            cur.execute("""drop table log_to_db.log_levels;""")

@pytest.mark.skipif(not is_postgres_available(), reason="PostgreSQL server not available")
def test_save_log(postgres_log: PostgresLog):
    con = duckdb.connect()
    con.execute("""install postgres;""")
    con.execute("""load postgres;""")
    con.execute(
        f"""attach '{postgres_log.connection_info}' as db (type postgres, read_only);"""
    )

    assert con.sql("select count(*) from db.log_to_db.logs;").fetchone()[0] == 0

    postgres_log.log(level="info",message="test_message",details=dict(more_info="1st one"))
    postgres_log.save_log()

    assert con.sql("select count(*) from db.log_to_db.logs;").fetchone()[0] == 1

    postgres_log.log(level="info", message="test_message", details=dict(more_info="2nd one"))
    postgres_log.save_log()

    assert con.sql("select count(*) from db.log_to_db.logs;").fetchone()[0] == 2
