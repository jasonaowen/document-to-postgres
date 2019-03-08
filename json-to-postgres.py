#!/usr/bin/env python

# Copyright (C) 2016 Jason Owen <jason.a.owen@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A small script to load line-delimited JSON data into a column in a table in a
PostgreSQL database.
"""

import argparse
import fileinput
import json
import psycopg2
from psycopg2.extras import Json


def parse_args():
    parser = argparse.ArgumentParser(
        description='Load streaming JSON data into a PostgreSQL database.'
    )
    parser.add_argument('user')
    parser.add_argument('dbname')
    parser.add_argument('table')
    parser.add_argument('column')
    parser.add_argument('filename', nargs='*', default='-')

    return parser.parse_args()


def load_line_delimited_json_data(user, dbname, table, column, filenames):
    conn = psycopg2.connect("dbname={} user={}".format(dbname, user))
    cur = conn.cursor()
    insert_statement = "INSERT INTO {} ({}) VALUES (%s)".format(table, column)

    for line in fileinput.input(filenames):
        try:
            parsed_line = json.loads(line)
            cur.execute(insert_statement, [Json(parsed_line)])
        except ValueError as e:
            e.args += (fileinput.filename(),)
            raise

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    args = parse_args()
    print("Database: {}, user: {}, table: {}, column: {}".format(
        args.dbname,
        args.user,
        args.table,
        args.column,
    ))

    load_line_delimited_json_data(
        args.user,
        args.dbname,
        args.table,
        args.column,
        args.filename
    )
