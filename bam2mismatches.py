from __future__ import division
import re
import sys

md_regex = re.compile("MD:Z:\S+")
rex = re.compile("[0-9]+[ACTG]+")

for line in sys.stdin:
  try:
    md_line = md_regex.findall(line)[0]
  except:
    sys.stderr.write("Can't find MD:Z: in "+line)
  elements = rex.findall(md_line)
  print len(elements)/len(line.split()[9])
