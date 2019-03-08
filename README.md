# document-to-postgres

Load JSON or XML documents into PostgreSQL.

These Python scripts depend on the [psycopg2](http://initd.org/psycopg/)
library to talk to PostgreSQL, which in turn depends on having
[libpq](https://www.postgresql.org/docs/current/libpq.html) installed. This
library is packaged in Debian as
[python-psycopg2](https://packages.debian.org/stretch/python-psycopg2) (for
Python 2) or
[python3-psycopg2](https://packages.debian.org/stretch/python3-psycopg2) (for
Python 3), and is packaged on PyPI as
[psycopg2](https://pypi.org/project/psycopg2/).

PostgreSQL introduced the XML data type in version 8.3, the JSON data type in
9.2, and the JSONB data type in 9.4 ([release
history](https://en.wikipedia.org/wiki/PostgreSQL#Release_history)). This
script should work with all currently supported PostgreSQL versions.

## json-to-postgres

Load one or more files containing line-delimited JSON into a PostgreSQL
database.

The target database table needs to have a [JSON or JSONB
column](https://www.postgresql.org/docs/current/datatype-json.html), and can
have any number of additional columns, so long as they have default values that
meet any existing constraints.

For example:

```sql
CREATE TABLE events(
  event_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  event JSONB NOT NULL
);
```

Call the script with `--help` for more details.

## xml-to-postgres

Load one or more XML files into a PostgreSQL database.

The target database table needs to have an [xml
column](https://www.postgresql.org/docs/current/datatype-xml.html), and can
have any number of additional columns, so long as they have default values that
meet any existing constraints.

For example:

```sql
CREATE TABLE documents(
  document_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  document XML NOT NULL
);
```

Call the script with `--help` for more details.
