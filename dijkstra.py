#!/usr/bin/env python

import timeit
import pyspark
import sys, os

import math
import heapq

from grid import Grid

inputUri='gs://dataproc-ed3c3d29-fb10-47bb-aca7-dcc358c68973-us-central1/input/map.txt'
outputUri='gs://dataproc-ed3c3d29-fb10-47bb-aca7-dcc358c68973-us-central1/output'

def parseRDD(line):
  parsedLine = list(line)
  return parsedLine

sc = pyspark.SparkContext()

grid = []

lines = sc.textFile(inputUri, 6)
words = lines.flatMap(parseRDD)
wordsMap = lines.map(parseRDD).collect()

grid = Grid([len(wordsMap), len(wordsMap[0])])
    
sharedGrid = sc.broadcast(grid)

def buildCpd(cell):
  localGrid = sharedGrid.value
  start_time = timeit.default_timer()
  localGrid.dijkstra(localGrid.mGrid[cell.pos[0]][cell.pos[1]])
  re = localGrid.compress(localGrid.mGrid[cell.pos[0]][cell.pos[1]])
  id = cell.pos[0]*localGrid.dims[1]+cell.pos[1]
  elapsed = timeit.default_timer() - start_time
  return (cell.pos[0], cell.pos[1], id, len(re), elapsed)

rdda = sc.parallelize(grid.mGrid, 14)
rddb = rdda.flatMap(lambda row: row)
rddc = rddb.map(buildCpd)
rddc.saveAsTextFile(outputUri+'/debug')
