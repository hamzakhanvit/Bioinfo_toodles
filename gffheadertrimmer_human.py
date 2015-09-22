hand = open("/home/hkhan/Downloads/ref_GRCh38.p2_top_level.short_gff", "rU")
import csv
import re
csvfile = open('/home/hkhan/Downloads/ref_GRCh38.p2_top_level.short_gff.csv', 'wb')
w = csv.writer(csvfile, delimiter=',')
reader = csv.reader(hand)
for row in reader:
    #b = int(row[0].find(";gbkey"))
    #a = int(row[0].find("NM_"))
    #print row[0][40:55]
    #print row[0][a:b]
    m = re.search('(Genbank:)(.*?)(\;){1}', row[1])
    if m:    
        st = m.group(0)
        st = st[8:]
        st = st[:-3]
        print st
        w.writerow([st, row[2], row[3], row[4]])
