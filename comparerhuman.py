

from collections import defaultdict
d1 = defaultdict(list)
import csv
csvfile = open('/home/hkhan/Downloads/ref_GRCh38.p2_top_level.short_gff.csv')
for row in csvfile:
   a = row.split(',')
   if(len(a)==4):
       key = a[0].rstrip()
       val = int(a[3].rstrip())
       d1[key].append(val)
print d1


d2 = defaultdict(list)
boundaryfile = open('/projects/btl/hkhan/HSapiens/bloom/k30_new/k30_new_mrna/boundariesfull.csv')
for row in boundaryfile:
   a = row.split(',')
   if(len(a)==3):
       key = a[0].rstrip()
       val = int(a[2].rstrip()) - int(a[1].rstrip())
       d2[key].append(val)


writefile = open('/projects/btl/hkhan/HSapiens/bloom/k30_new/k30_new_mrna/TPFP', 'wb')
w = csv.writer(writefile, delimiter=',')
w.writerow(['Identifier','expected_matches','obtained_matches'])


checkfile = open('/projects/btl/hkhan/HSapiens/bloom/k30_new/k30_new_mrna/TPFP_check', 'a')

check=0;
for k in d1:
    count=0
    if k in d2:
      print k
      unique_d2k = set(d2[k])
      d1[k].pop(0)
      print d1[k], unique_d2k
      print "\nOut of ",
      len_d1k = len(d1[k]);
      if((len_d1k)<len(d2[k])):
           check = check+1;
           checkfile.write(str(k))
           checkfile.write(str(d1[k]))
           checkfile.write(str(unique_d2k))
      print len_d1k
      for a in (d1[k]):
         temp=[0]
         #print range(int(a-4),int(a+4),1)
         for b in unique_d2k:
             print "A is ", a
             print range(int(a-4),int(a+5),1)
             if(b in range(int(a-4),int(a+5),1)):
               dup_flag=0
               for z in temp:
                   #for q in range(int(z-4),int(z+4),1):
                     if(b in range(int(z-6),int(z+6),1)):
                       dup_flag = 1
                       break
               if(dup_flag==0):
                 count+=1
                 print "Yes"
             dup_flag=0
             temp.append(b)
      print "only ",count," matches found\n"
      w.writerow([str(k),int(len_d1k),int(count)])

print check;
