# db_logging

Be able to log to a database.

## Features

- Can log to the following databases:
  - PostgreSQL
  - SQLite
  - DuckDB

## Quickstart

### Install

```
> pip install db_logging
```

### Setup

The database will need to be created ahead of time.
The table structure will need to be:

```
create schema if not exists programs;

drop table if exists programs.logs;
drop table if exists programs.log_levels;

create table programs.logs (
     entry timestamptz not null default now()
    ,program text not null
    ,pc_name text not null
    ,level int not null
    ,message text not null
    ,details jsonb null
);

create table programs.log_levels (
     level int not null
    ,name text not null
);

-- Insert log_level data
insert into programs.log_levels (level, name) values
 (10, 'debug')
,(20, 'info')
,(30, 'warning')
,(40, 'error')
,(50, 'critical');
```

This is using PostgreSQL as the example database with `programs` as the schema.
However, the log table name will need to be `logs`.
**Note** `log_level` table is not required but this makes it easier to build queries.
SQLite would be similar but the schema won't be included.

### Example Usage

To use in a program for example:

```
from db_logging.postgres_log import PostgresLog

db_logger = PostgresLog(
    save_level="debug",
    pc_name="test_pc",
    program_name="test_program",
    program_timezone="America/Chicago",
    connection_info="postgres://user:password@youhost:5432/log_database",
    schema="log_location",
)

db_logger.info(
    message="Starting program.",
    details=dict(
        test_data="This is a test.",
    )
)

db_code = db_logger.save_log()
```

To use SQLite instead, replace `connection_info` to the file location of the SQLite database file.
