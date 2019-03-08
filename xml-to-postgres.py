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
A small script to load individual XML documents (one per file) into a column in
a table in a PostgreSQL database.
"""

import argparse
import psycopg2


def parse_args():
    parser = argparse.ArgumentParser(
        description='''
            Load one or more XML documents into a PostgreSQL database. The
            target database table must have one xml column (specified via the
            `column` argument), and any other columns in the table must have
            default values.
        ''',
        epilog='''
            See also the PostgreSQL table creation syntax
            (https://www.postgresql.org/docs/current/sql-createtable.html) and
            the PostgreSQL xml data type
            (https://www.postgresql.org/docs/current/datatype-xml.html).
        ''',
    )
    parser.add_argument('user', help='user to connect to the database as')
    parser.add_argument('dbname', help='database to connect to')
    parser.add_argument('table', help='table to insert into')
    parser.add_argument('column', help=('''column to insert into; the data type
        of the column must be xml'''))
    parser.add_argument('filename', nargs='*', default='-', help='''Filenames of
        XML files to load''')

    return parser.parse_args()


def load_xml_documents(user, dbname, table, column, filenames):
    conn = psycopg2.connect("dbname={} user={}".format(args.dbname, args.user))
    cur = conn.cursor()
    insert_statement = (
        "INSERT INTO {} ({}) VALUES (XMLPARSE (DOCUMENT %s))".format(
            args.table,
            args.column
        )
    )

    for filename in filenames:
        with open(filename) as xml_file:
            xml = xml_file.read()
            cur.execute(insert_statement, [xml])

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

    load_xml_documents(
        args.user,
        args.dbname,
        args.table,
        args.column,
        args.filename
    )
