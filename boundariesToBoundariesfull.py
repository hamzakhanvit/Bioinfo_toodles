'''
Coverts boundary file from this format -
ce10_refGene_NR_070240=chrI:7741936-8394405,30,96

to this format -
NR_052806,1,43


'''

import csv
import re
csvfile = open('/projects/btl/hkhan/HSapiens/bloom/k30_new/k30_new_mrna/boundariesfull.csv', 'wb')
w = csv.writer(csvfile, delimiter=',')
csv = open('/projects/btl/hkhan/HSapiens/bloom/k30_new/k30_new_mrna/boundaries.csv')
count=0
counta = 0
countb = 0
for row in csv:
   count+=1
   a = row.split(',')
   if(len(a)==3):
     #print a[0]
     identifier = a[0].split("|")
     b = identifier[3].split(".") 
     print b[0]
     w.writerow([b[0], int(a[1]), int(a[2])])


