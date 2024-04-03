# ZX Game Picker

This is a simple Python script that randomly selects an entry from the ZXDB.

## Examples

Select any entry randomly from the ZXDB:
```
zx-picker.py
```

Select any arcade game published in the 1980s:
```
zx-picker.py --arcade --1980s
```

Select any adventure game published in 1989 or 1990
```
zx-picker.py --adventure --years 1989 1990
```

List all genres available:
```
zx-picker.py --list-genres 
```

Select any casual word game:
```
zx-picker.py --genre 32
```

## Requirements

This project does not contain the ZXDB. This will need to be downloaded from [ZXDB GitHub Project](https://github.com/zxdb/ZXDB). As this Python program requires an SQLite3 database the conversion script will need to be run and the resultant SQL script can then be used to generate the database.

By default this program expects to find the database (named 'ZXDB_sqlite.db') in the same directory as the script. Alternatively the database file can be passed into the program.

