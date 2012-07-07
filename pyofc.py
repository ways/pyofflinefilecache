#!/usr/bin/env python
# -*- coding: UTF-8; -*-

__version__ = '0.1'
__url__ = 'https://github.com/ways/pyofflinefilecache'
__license__ = 'GPL License'

import os, time, datetime, codecs


class OfflineFileCache:
  ''' A class storing data as files for later retreval based on timestamp.
      First line of cache file contains timestamp. Rest is text data. '''

  def __init__(self, cachedir, cachetime, fetchfunction, fetcharg = False, verbose = False):
    self.fetchfunction = fetchfunction
    self.fetcharg = fetcharg
    self.cachetime = cachetime
    self.cachedir = cachedir
    self.verbose = verbose

    if not os.path.exists(self.cachedir):
      try:
        os.mkdir(self.cachedir, 0700)
      except FileError as e:
        print "Error writing to dir ", self.cachedir, e


  def set(self, id, data):
    id = self.escape_string(id)
    #print data.read()
    try:
      #with codecs.open(self.cachedir + id, 'w', encoding='utf-8') as f:
      with codecs.open(self.cachedir + id, 'w') as f:
        f.write(str(time.time()) + "\n" + data )
    except IOError as e:
      print "OfflineFileCache: Error opening file " + self.cachedir + id
      #return False

  def status(self, id):
    id = self.escape_string(id)
    try:
      with codecs.open(self.cachedir + id, 'r') as f:
        firstline = f.readline()
        filetime = float(firstline)
    except IOError as e:
      if self.verbose:
        print "Error reading file " + self.cachedir + id + str(e)
      return False
    except ValueError as e:
      if self.verbose:
        print "Error converting time from " + str(firstline)
        return False

    if self.verbose:
      print "Time from file: " + str(datetime.datetime.fromtimestamp(filetime))

    if filetime > (time.time() - self.cachetime):
      if self.verbose:
        print "File is fresh, remaining " + str((filetime + self.cachetime) - time.time())
      return True
    else:
      if self.verbose:
        print "File is sour, over time: " + str(time.time() - filetime)
      return False


  def get(self, id):
    id = self.unescape_string(id)
    if self.status(id):
      #with codecs.open(self.cachedir + id, 'r', encoding='utf-8') as f:
      with codecs.open(self.cachedir + id, 'r') as f:
        filetime = f.readline()
        if self.verbose:
          print "Filetime ", filetime
          print "Returning cached data for", id
        return f.read(), True
    else:
      if self.verbose:
        print "Resetting contents of file"
      data = self.fetchfunction(self.fetcharg)

      self.set(id, data)

      if self.verbose:
        print "Returning fresh data for", id
        #print data
      return data, False


    def escape_string(str):
      if len(str) > 20:
        str = str[:20]
      str = str.strip()\
      .replace('..','')\
      .replace('~','£')\
      .replace('/','_')

      return newstr

    def unescape_string(str):
      str = \
      .replace('£','~')\
      .replace('_','/')

      return newstr



if __name__ == "__main__":
  #Example data:
  cachedir="/tmp/pyyrlib-cache/"
  cachetime=1200

  def fetchdata(id = "0000"):
    return "It's sunny at " + id

  #Example usage:
  ofc = OfflineFileCache (cachedir, cachetime, fetchdata, "0459", True)
  data, fromcache = ofc.get('0459')
  print "data: " + str(data)
