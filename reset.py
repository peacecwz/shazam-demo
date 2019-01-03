from src.db import SQLiteDatabase
from termcolor import colored

if __name__ == '__main__':
  db = SQLiteDatabase()

  db.query("DROP TABLE IF EXISTS songs;")
  print colored('Dropped songs table',"red");

  db.query("""
    CREATE TABLE songs (
      id  INTEGER PRIMARY KEY AUTOINCREMENT,
      name  TEXT,
      filehash  TEXT
    );
  """)
  print colored('Created songs table','green');

  db.query("DROP TABLE IF EXISTS fingerprints;")
  print colored('Removed fingerprints',"red");

  db.query("""
    CREATE TABLE `fingerprints` (
      `id`  INTEGER PRIMARY KEY AUTOINCREMENT,
      `song_fk` INTEGER,
      `hash`  TEXT,
      `offset`  INTEGER
    );
  """)
  print colored('Created Fingerprints',"green");

  print colored('Done',"green");
