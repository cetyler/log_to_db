# log_to_db

Be able to log to a database.
Currently, it is known to work with Windows 10/11 and Ubuntu 24.04.
This does not mean it wouldn't work with other operating systems (ex. MacOS,
other Linux distributions, etc.) just that I haven't tested it yet.

## Features

- Can log to the following databases:
  - PostgreSQL
  - SQLite
  - DuckDB

## Quickstart

### Install

```
> pip install log_to_db
```

### Setup

The database will need to be created ahead of time.
The table structure will need to be:

```
create schema if not exists programs;

drop table if exists log_location.logs;
drop table if exists log_location.log_levels;

create table log_location.logs (
     entry timestamptz not null default now()
    ,program text not null
    ,pc_name text not null
    ,level int not null
    ,message text not null
    ,details jsonb null
);

create table log_location.log_levels (
     level int not null
    ,name text not null
);

-- Insert log_level data
insert into log_location.log_levels (level, name) values
 (10, 'debug')
,(20, 'info')
,(30, 'warning')
,(40, 'error')
,(50, 'critical');
```

This is using PostgreSQL as the example database with `log_location` as the schema.
However, the log table name will need to be `logs`.
**Note** `log_level` table is not required but this makes it easier to build queries.
SQLite and DuckDB would be similar but the schema won't be included.

### Example Usage

To use in a program for example:

```
from log_to_db.postgres_log import PostgresLog

db_logger = PostgresLog(
    save_level="debug",
    pc_name="test_pc",
    program_name="test_program",
    program_timezone="America/Chicago",
    connection_info="postgres://user:password@yourhost:5432/log_database",
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

To use SQLite or DuckDB instead, replace `connection_info` to the file location
of the SQLite database file.
For either of these databases, it will be either `SQLiteLog` from `sqlite_log`
or `DuckDBLog` from `duckdb_log`.
**Note** file-based databases currently don't have a custom schema.

## Usage

For the most part, the API is similar for each supported database.
There is a base class `DBLog` in `db_log.py` which has the following inputs:

- save_level (required)
  - A string value that should match one of the log levels:
    - debug
    - info
    - warning
    - error
    - critical
- pc_name (required)
  - The name of the computer that is the given program is running on.
  - This will help later on when reviewing logs, especially if there are
    multiple computers logging.
- program_name (required)
  - The name of the program which similar to `pc_name` will help when reviewing
    the logs later on.
- logs (optional, but shouldn't change)
  - Will default as an empty `dict()`.
    This is not something you will need to modify.
- program_timezone (optional and should change unless you are in the USA
  Central Timezone)
  - The program's timezone.
  - Defaults to "America/Chicago".

The available methods are:

- load_log_levels()
  - This is required to run first prior to doing any logging.
  - This creates a `dict()` matching the log level to it's name (ex. debug = 10).
- get_log_level(level_name)
  - This will return the integer that matches a given log level
    (ex. return 10 for debug).
- get_error_codes(code)
  - Depending on the error integer code, will return the corresponding text
    (ex. 0 will return "Successful.").
- log(level, message, details)
  - Your program should not need to call this method and use the methods below.
  - The level is the log level string (ex. debug).
  - The message is a string value of whatever message is required.
  - The details is a `dict()` to add any further details that would help.
  - This method will then determine if it should be logged or not.
    - For example, if the minimum log level is debug, then all log levels will
      be recorded.
      However, if the minimum log level is warning, then info and debug will
      **not** be recorded.
  - This method appends a given log to `logs` dictionary.
- debug(message,details)
  - This will call `log()` to log as debug.
  - Debug is just for development/debugging purposes.
  - Message is a string value of whatever message is required.
  - Details is a `dict()` to add any further details that would help.
    - If no details are, then provide an empty `dict()`.
- info(message,details)
  - This will call `log()` to log as info.
  - This is confirmation that things are working as expected.
  - Message is a string value of whatever message is required.
  - Details is a `dict()` to add any further details that would help.
    - If no details are, then provide an empty `dict()`.
- warning(message,details)
  - This will call `log()` to log as warning.
  - This is an indication that something could be wrong or unexpected but
    the software is still working as expected.
  - Message is a string value of whatever message is required.
  - Details is a `dict()` to add any further details that would help.
    - If no details are, then provide an empty `dict()`.
- error(message,details)
  - This will call `log()` to log as error.
  - This is a more serious problem and the software was unable to perform some
    function.
  - Message is a string value of whatever message is required.
  - Details is a `dict()` to add any further details that would help.
    - If no details are, then provide an empty `dict()`.
- critical(message,details)
  - This will call `log()` to log as critical.
  - This is a serious error and the program itself may be unable to continue.
  - Message is a string value of whatever message is required.
  - Details is a `dict()` to add any further details that would help.
    - If no details are, then provide an empty `dict()`.

You will notice that debug, info, warning, error and critical follow the same
pattern as Python's
[logging module](https://docs.python.org/3/library/logging.html#module-logging)
which was done on purpose.

Each database class have these same methods.

### DuckDB

`DuckDBLog(DBLog)` class is located in `duckdb_log.py`.
There is an additional input from `DBLog()`:

- connection_info (optional but you will probably want to change)
  - Defaults to `log.duckdb` in the current directory.
  - It expects to get a `Path` object from `pathlib`.

There is an additional method:

- `save_log()`
  - This will attempt to save the logs `dict()`.
  - After a successful save, it will clear logs `dict()`.

### PostgreSQL

`PostgresLog(DBLog)` class is located in `postgres_log.py`.
There is an additional input from `DBLog()`:

- connection_info (optional but you will want to change)
  - Defaults to localhost with port of 5432 to `raw_test_data` database with
    username and userpassword as the user and password.

There is an additional method:

- `save_log()`
  - This will attempt to save the logs `dict()`.
  - After a successful save, it will clear logs `dict()`.

### SQLite

`SQLiteLog(DBLog)` class is located in `sqlite_log.py`.
There is an additional input from `DBLog()`:

- connection_info (optional but you will probably want to change)
  - Defaults to `log.sqlite` in the current directory.
  - It expects to get a `Path` object from `pathlib`.

There is an additional method:

- `save_log()`
  - This will attempt to save the logs `dict()`.
  - After a successful save, it will clear logs `dict()`.

## Development

I would suggest using [uv](https://docs.astral.sh/uv/) but you can use standard
Python/pip.
If using `uv` (this will create the virtual environment and install the packages):

``bash
$ uv sync
$ uv sync --dev
``
Using `pip` and `venv`:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

In order to run all the tests, you will need to install
[PostgreSQL](https://www.postgresql.org/).
There is a `env_sample` which you should copy and rename to `.env`.
Put in the required information to connect to your PostgreSQL database.
**Note** the PostgreSQL database does not need to be on your development
machine.
