import os
import sys
import src
import src.analyzer as analyzer
from src.reader_file import FileReader
from termcolor import colored
from src.db import SQLiteDatabase

MUSICS_FOLDER_PATH = "mp3/"

if __name__ == '__main__':
  db = SQLiteDatabase()

  for filename in os.listdir(MUSICS_FOLDER_PATH):
    if filename.endswith(".mp3"):
      reader = FileReader(MUSICS_FOLDER_PATH + filename)
      audio = reader.parse_audio()

      song = db.get_song_by_filehash(audio['file_hash'])
      song_id = db.add_song(filename, audio['file_hash'])

      print colored("Analyzing music: %s","green") % filename 
      
      if song:
        hash_count = db.get_song_hashes_count(song_id)

        if hash_count > 0:
          msg = 'Warning: This song has already exists (%d hashes), skip' % hash_count
          print colored(msg, 'yellow')

          continue

      hashes = set()
      channel_amount = len(audio['channels'])

      for channeln, channel in enumerate(audio['channels']):
        channel_hashes = analyzer.fingerprint(channel, Fs=audio['Fs'])
        channel_hashes = set(channel_hashes)

        msg = 'Channel %d saved %d hashes'
        print colored(msg, attrs=['dark']) % (
           channeln, len(channel_hashes)
        )

        hashes |= channel_hashes

      values = []
      for hash, offset in hashes:
        values.append((song_id, hash, offset))

      db.store_fingerprints(values)

  print colored('Done',"green")
