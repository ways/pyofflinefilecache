#!/usr/bin/env python

import os, time, datetime

#offline disk cache
cachedir="/tmp/pyyrlib-cache/"
cachetime=60

def fetchdata(id = "0000"):
  return "It's sunny at " + id


class OfflineFileCache:
  ''' A class storing data as files for later retreval based on timestamp.
      First line of cache file contains timestamp. Rest is text data. '''

  def __init__(self, cachedir, cachetime, fetchfunction, verbose = False):
    self.fetchfunction = fetchfunction
    self.cachetime = cachetime
    self.cachedir = cachedir
    self.verbose = verbose

    if not os.path.exists(cachedir):
      try:
        os.mkdir(cachedir, 0700)
      except FileError as e:
        print "Error writing to dir ", cachedir, e


  def set(self, id, data):
    try:
      with open(cachedir + id, 'w') as f:
        f.write(str(time.time()) + "\n" + data)
    except IOError as e:
      print "OfflineFileCache: Error opening file " + cachedir + id
      return False


  def status(self, id):
    try:
      with open(cachedir + id, 'r') as f:
        filetime = float(f.readline())
    except IOError as e:
      if self.verbose:
        print "Error reading file " + cachedir + id
      return False

    if self.verbose:
      print "Time from file: " + str(datetime.datetime.fromtimestamp(filetime))

    if filetime > (time.time() - cachetime):
      if self.verbose:
        print "File is fresh, remaining " + str((filetime + cachetime) - time.time())
      return True
    else:
      if self.verbose:
        print "File is sour, over time: " + str(time.time() - filetime)
      return False

  def get(self, id):
    if self.status(id):
      with open(cachedir + id, 'r') as f:
        filetime = f.readline()
        return f.read()
    else:
      if self.verbose:
        print "Reset contents of file"
      data = self.fetchfunction()
      if not self.set(id, data):
        return False

      return data

print "Now:"
print datetime.datetime.fromtimestamp(time.time())
ofc = OfflineFileCache (cachedir, cachetime, fetchdata)
print ofc.get('0458')
