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

    genre_group = parser.add_mutually_exclusive_group()
    genre_group.add_argument('--genres', dest='genres', nargs='+', type=int, help='List of genres to select from') 
    genre_group.add_argument('--arcade', action='store_true', help='Select from all genres that are arcade games')
    genre_group.add_argument('--adventure', action='store_true', help='Select from all generes that are adventure games')
    genre_group.add_argument('--misc', action='store_true', help='Select from games not flagged as either adventure or arcade')
    genre_group.add_argument('--all', action='store_true', help='Select from all games')

    year_group = parser.add_mutually_exclusive_group()
    year_group.add_argument('--years', dest='years', nargs='+', type=int, help='List of years to select from')
    year_group.add_argument('--1980s', dest='the80s', action='store_true', help='Select entries from the 1980s')
    year_group.add_argument('--1990s', dest='the90s', action='store_true', help='Select entries from the 1990s')
    year_group.add_argument('--modern', dest='modern', action='store_true', help='Selectr entries from the 2000s and onwards')

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
        fetch_string = "SELECT entries.title, entries.id, releases.release_seq, releases.release_year, releases.release_month, releases.release_day FROM entries JOIN releases ON entries.id = releases.entry_id "

        where_clauses = list()
            
        # Pick genre (if defined)
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
            where_clauses.append("entries.genretype_id IN (" + ",".join(map(str, genres)) + ")")

        # Select years (if defined)
        if args.years:
            where_clauses.append("releases.release_year IN (" + ",".join(map(str, args.years)) + ")")


        if args.the80s:
            where_clauses.append("releases.release_year >= 1980 AND releases.release_year <= 1989")
        if args.the90s:
            where_clauses.append("releases.release_year >= 1990 AND releases.release_year <= 1999")
        if args.modern:
            where_clauses.append("releases.release_year >= 1990")

        # Add where clause (if defined)
        if where_clauses:
            fetch_string += "WHERE "
            fetch_string += " AND ".join(where_clauses)
            fetch_string += " "

        fetch_string += "ORDER BY RANDOM() LIMIT 1;"

        # print(fetch_string)
        res = cur.execute(fetch_string)

        # Fetch data and print title
        title, entry_id, seq, year, month, day = res.fetchall()[0]
        print(f"Title: '{title}'")

        # Now display date of pblication
        print("Release date: ", end='')
        if year is None:
            released = "UNKNOWN"
        else:
            if month is None:
                month = "??"
            if day is None:
                day = "??"
            released = f"{day:2}/{month:2}/{year}"
        print(released)

        # Now print publisher
        publisher_select = f"SELECT label_id FROM publishers WHERE entry_id = {entry_id} AND release_seq = {seq}"
        res = cur.execute(publisher_select)
        publishers = res.fetchall()
        if not publishers:
            print("Unkown publisher")
        else:
            for label_id, in publishers:
                labels_select = f"SELECT name FROM labels WHERE id = {label_id};"
                res = cur.execute(labels_select)
                labels = res.fetchall()
                for name, in labels:
                    print(name)

    con.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())
