import os
import sys
import src
import src.analyzer as analyzer
import argparse

from argparse import RawTextHelpFormatter
from itertools import izip_longest
from termcolor import colored
from src.config import get_config
from src.listener import Listener
from src.db import SQLiteDatabase

if __name__ == '__main__':
  db = SQLiteDatabase()

  parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
  parser.add_argument('-s', '--seconds', nargs='?')
  args = parser.parse_args()

  if not args.seconds:
    print colored("Warning: You don't set any second. It's 10 by default", "yellow")
    args.seconds = "10"

  seconds = int(args.seconds)

  chunksize = 2**12
  channels = 2

  record_forever = False

  listener = Listener()

  listener.start_recording(seconds=seconds,
    chunksize=chunksize,
    channels=channels)

  while True:
    bufferSize = int(listener.rate / listener.chunksize * seconds)
    print colored("Listening....","green")

    for i in range(0, bufferSize):
      nums = listener.process_recording()

    if not record_forever: break

  listener.stop_recording()

  print colored('Okey, enough', attrs=['dark'])

  def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in izip_longest(fillvalue=fillvalue, *args))

  data = listener.get_recorded_data()

  msg = 'Took %d samples'
  print colored(msg, attrs=['dark']) % len(data[0])

  Fs = analyzer.DEFAULT_FS
  channel_amount = len(data)

  result = set()
  matches = []

  def find_matches(samples, Fs=analyzer.DEFAULT_FS):
    hashes = analyzer.fingerprint(samples, Fs=Fs)
    return return_matches(hashes)

  def return_matches(hashes):
    mapper = {}
    for hash, offset in hashes:
      mapper[hash.upper()] = offset
    values = mapper.keys()

    for split_values in grouper(values, 1000):
      query = """
        SELECT upper(hash), song_fk, offset
        FROM fingerprints
        WHERE upper(hash) IN (%s)
      """
      query = query % ', '.join('?' * len(split_values))

      x = db.executeAll(query, split_values)
      matches_found = len(x)

      if matches_found > 0:
        msg = 'I found %d hash in db'
        print colored(msg, 'green') % (
          matches_found
        )

      for hash, sid, offset in x:
        yield (sid, offset - mapper[hash])

  for channeln, channel in enumerate(data):
    matches.extend(find_matches(channel))

  def align_matches(matches):
    diff_counter = {}
    largest = 0
    largest_count = 0
    song_id = -1

    for tup in matches:
      sid, diff = tup

      if diff not in diff_counter:
        diff_counter[diff] = {}

      if sid not in diff_counter[diff]:
        diff_counter[diff][sid] = 0

      diff_counter[diff][sid] += 1

      if diff_counter[diff][sid] > largest_count:
        largest = diff
        largest_count = diff_counter[diff][sid]
        song_id = sid

    songM = db.get_song_by_id(song_id)

    nseconds = round(float(largest) / analyzer.DEFAULT_FS *
                     analyzer.DEFAULT_WINDOW_SIZE *
                     analyzer.DEFAULT_OVERLAP_RATIO, 5)

    return {
        "SONG_ID" : song_id,
        "SONG_NAME" : songM[1],
        "CONFIDENCE" : largest_count,
        "OFFSET" : int(largest),
        "OFFSET_SECS" : nseconds
    }

  total_matches_found = len(matches)

  if total_matches_found > 0:
    msg = 'Totally found %d hash'
    print colored(msg, 'green') % total_matches_found

    song = align_matches(matches)

    msg = ' => song: %s (id=%d)\n'
    msg += '    offset: %d (%d secs)\n'

    print colored(msg, 'green') % (
      song['SONG_NAME'], song['SONG_ID'],
      song['OFFSET'], song['OFFSET_SECS']
    )
  else:
    msg = 'Not anything matching'
    print colored(msg, 'red')
