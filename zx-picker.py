#!/usr/bin/python3

import sys
import argparse
import sqlite3

def main() -> int:
    """ Main entrypoint """
    parser = argparse.ArgumentParser(description='Utility for randomly picking games from the ZXDB.')
    parser.add_argument('file', metavar='FILE', type=str, nargs='?', default='ZXDB_sqlite.db', help='Override ZXDB file to use (in SQLite format)')
    parser.add_argument('--list-genres', dest='list_genres', action=argparse.BooleanOptionalAction, help='Lists all available genres along with their IDs')
    parser.set_defaults(list_genres=False)
    args = parser.parse_args()

    con = sqlite3.connect(args.file)
    cur = con.cursor()

    if args.list_genres:
        res = cur.execute("SELECT * FROM genretypes;")
        print(res.fetchall())
    else:
        res = cur.execute("SELECT title FROM entries ORDER BY RANDOM() LIMIT 1;")
        print(res.fetchall()[0][0])

    con.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())
