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
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--genres', dest='genres', nargs='+', type=int, help='List of genres to select from') 
    group.add_argument('--arcade', action='store_true', help='Select from all genres that are arcade games')
    group.add_argument('--adventure', action='store_true', help='Select from all generes that are adventure games')
    group.add_argument('--misc', action='store_true', help='Select from games not flagged as either adventure or arcade')
    group.add_argument('--all', action='store_true', help='Select from all games')
    args = parser.parse_args()

    genre_enabled = args.genres or args.arcade or args.adventure or args.misc or args.all

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
        if genre_enabled:
            fetch_string += "WHERE "

        genres = list()
        if args.genres:
            genres.extend(args.genres)
        if args.adventure or args.all:
            genres.extend([1, 2, 4, 5, 6])
        if args.arcade or args.all:
            genres.extend([7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        if args.misc or args.all:
            genres.extend([27, 28, 29, 31, 32, 17, 18, 19, 30, 20, 21, 26])

        if genre_enabled:
            fetch_string += "genretype_id IN (" + ",".join(map(str, genres)) + ") "

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
