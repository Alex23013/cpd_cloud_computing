#!/usr/bin/env python

import pyspark
import sys

inputUri='gs://dataproc-76399b63-8b38-4f0a-b831-6e680daa45e8-us-central1/input/words.txt'
outputUri='gs://dataproc-76399b63-8b38-4f0a-b831-6e680daa45e8-us-central1/output'

sc = pyspark.SparkContext()
lines = sc.textFile(inputUri)
words = lines.flatMap(lambda line: line.split())
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda count1, count2: count1 + count2)
wordCounts.saveAsTextFile(outputUri)
