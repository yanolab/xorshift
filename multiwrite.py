#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from functools import partial
from multiprocessing import Pool, cpu_count

def humansize(bytesize, unit=1024):
  labeltable = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  for label in labeltable:
    bytesize /= unit
    if bytesize < unit:
      return "%.1f %s" % (bytesize, label)

  raise ValueError('number too large')

def worker(dirname, blocksize, writecount, filecount):
  filename = os.path.join(dirname, str(filecount))
  os.system('./xorshift %s %d %d' % (filename, blocksize, writecount))

def workerrunner(args):
  worker(*args)

if __name__ == '__main__':
  if len(sys.argv) != 5:
    print "python write.py OUTDIR TOTAL_FILE_COUNT BLOCK_SIZE WRITE_COUNT"
    sys.exit(1)

  dirname = sys.argv[1]
  filecount, blocksize, writecount = map(int, sys.argv[2:5])

  with open("write.pid", "w") as f:
    f.write(str(os.getpid()))

  pool = Pool(cpu_count() * 2)

  if sys.version_info[0] and sys.version_info[1] >= 7 or sys.version_info[0] >= 3:
    workerrunner = partial(worker, sys.argv[1], blocksize, writecount)
    start = time.time()
    pool.map(workerrunner, xrange(filecount))
    end = time.time()
  else:
    start = time.time()
    pool.map(workerrunner, zip([dirname]*filecount, [blocksize]*filecount, [writecount]*filecount, xrange(filecount)))
    end = time.time()


  print end, "%s" % humansize(filecount * blocksize * writecount / (end-start))

  if os.path.exists("write.pid"):
    os.remove("write.pid")

