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
    parser.add_argument('--genres', dest='genres', nargs='+', type=int, help='List of genres to select from') 
    args = parser.parse_args()

    con = sqlite3.connect(args.file)
    cur = con.cursor()

    if args.list_genres:
        res = cur.execute("SELECT * FROM genretypes;")
        print("ID   Genre")
        print("---- --------------------------------------------------")
        for _id, _genre in res.fetchall():
            print(f"{_id:<4} {_genre:<50}")
    else:
        fetch_string = "SELECT title FROM entries "
        if args.genres:
            fetch_string += "WHERE "

        if args.genres:
            fetch_string += "genretype_id IN (" + ",".join(map(str, args.genres)) + ") "

        fetch_string += "ORDER BY RANDOM() LIMIT 1;"

        # print(fetch_string)
        res = cur.execute(fetch_string)
        # print(res.fetchall())
        title, = res.fetchall()[0]
        print(f"Title: {title}")

    con.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())
