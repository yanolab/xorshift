#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from multiprocessing import Pool, cpu_count

def worker(num):
  #filename = "/dev/null"
  filename = "1G.dat." + str(num)
  start = time.time()
  os.system('./xorshift %s 1024 %d' % (filename, 1024 * 1024))
  end = time.time()
  print end, "%s, %d Mbps" % (filename, 1.0/(end-start)*8)

with open("write.pid", "w") as f:
  f.write(str(os.getpid()))

pool = Pool()
s = time.time()
pool.map(worker, xrange(80))
e = time.time() - s
print 80 / e * 8, "Mbps"

