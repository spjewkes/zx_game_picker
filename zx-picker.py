#!/usr/bin/python3

import sys
import argparse
import sqlite3

def main() -> int:
    """ Main entrypoint """
    parser = argparse.ArgumentParser(description='Utility for randomly picking games from the ZXDB.')
    parser.add_argument('file', metavar='FILE', type=str, help='The ZXDB file to use (in SQLite format)')

    args = parser.parse_args()

    con = sqlite3.connect(args.file)

    cur = con.cursor()

    res = cur.execute("SELECT title FROM entries ORDER BY RANDOM() LIMIT 1;")

    print(res.fetchall()[0][0])

    con.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())
