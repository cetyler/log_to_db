# Roadmap

The roadmap will help drive feature releases.
Major releases (ex. 1.x.x) may include breaking changes and major new features.
Minor releases (x.1.x) will be new features that does not break the API.
Bugfixes (x.x.1) or very minor features that are isolated to a particular thing.

**Note** that only future releases will be shown.

## Release 0.2.0

* Test coverage for PostgreSQL.

## Release 0.3.0

* Test coverage for SQLite.

## Release 0.4.0

* Test coverage for DuckDB.

## Release 0.5.0

* Add option to create schema and tables if they don't exists.
* Add error checking to verify that the schema and tables given if exists are
  correct.

## Release 0.6.0

* Test with Python versions 3.11, 3.12 and 3.13.

## Release 1.0.0

* Feature complete.
* Will include options to change the following:
  * Schema (but will default to `programs`).
  * Log table (but will default to `logs`).
  * Log lelvel table (but will default to `log_levels`).
