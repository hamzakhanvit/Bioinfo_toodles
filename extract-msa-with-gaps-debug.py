from __future__ import division
import argparse, datetime, numpy as np
import sys, getopt, csv, re
from collections import Counter

__title__ = 'Extract-msa-with-gaps.py'
__version__ = '1.0.0'
__description__ = "Given a SPOA MSA file, the program computes heterozygozity"
__author__ = 'Hamza Khan'
__license__ = 'None'
__author_email__ = "hamza.khan@alumni.ubc.ca"
epi = "Licence: %s by %s <%s>\n\n" % (__license__,
__author__,
__author_email__)
__doc__ = "***************************************************************\
          \n %s v%s - %s \n************************************************\
***************" % (__title__,
__version__,
__description__)


def read_msa_compute_zygosity(inputfile, outputfile, percent, coverage):

  out=open(outputfile,'wb')
  df=open(("depth"+outputfile), 'wb')
  depth_ratio={}
  with open(inputfile) as fh:
    for i in xrange(1):
        fh.next()
    l=0
    lines=[]
    for line in fh:
      if line.startswith("digraph"):break
      else:
          #print line
          lines.append(list(line.rstrip()))
    a = np.array(lines)
    print "a=", a      
    print "a.shape=", a.shape,"a.ndim=" ,a.ndim   

    # Loop through each row and find the start and end coordinate of 
    # of each sequence
    row_indices={}
    for x in range(a.shape[0]):
        row = ''.join(a[x,:])
        #print "Row is = ", row
        start=re.search("\w", row).start()
        end=a.shape[1]-(re.search("\w", row[::-1]).start())-1
        row_indices[x]=(start,end)
        #print "row_indices are", row_indices[x]
    #print "row_indice dict is", row_indices
    
    # Loop on each column to get the most frequent element and its count
    true_columns={}
    homozygous_count=0
    for j in range(a.shape[1]):
        true_column=[]
        for i in range(a.shape[0]):
            if(row_indices[i][0]<=j and row_indices[i][1]>=j):
               true_column.append(a[i,j])
        true_columns[j]=(len(true_column), true_column.count('-'), true_column)
    print "true_columns = ", true_columns

    for j in range(a.shape[1]):
        count = Counter(a[:, j])
        print "Count=", count
        if '-' in count:
           print "GAP Present"
           print "No of Gaps = ", count['-']
           print "Gap ratio=",(int(count['-'])/(a.shape[0]))
           gaps = int(count.pop('-'))
        print "Counter elements=", list(count.elements())
        print "count.most_common(1)=", count.most_common(1)
        print "count.most_common(1)[0]=", count.most_common(1)[0]

        if(len(count)==1):
           homozygous_count=homozygous_count+1
        
        #Write depth for each homozygous datapoint
        if(len(count)==1) and ((true_columns[j][1]/true_columns[j][0])<(percent/100)):
            d =  "1," + str(true_columns[j][0]) + "\n"
            print "Homozygous found"
            print "d=", d
            df.write(d) 
        

        if(len(count)==2) and ((true_columns[j][1]/true_columns[j][0])<(percent/100)):
            vals = [float(count[item]) for item in count]           
            print "VALS=", vals
            x= str(round(max(vals)/(min(vals)+max(vals)),2)) + "\n"
        #if(count.most_common(1)[0][0]!='-' and (int(count['-'])/(a.shape[0]))<0.1  and count.most_common(1)[0][1]>=((a.shape[0])/4)):
            #x = str(round((count.most_common(1)[0][1])/(a.shape[0]),2)) + "\n"
            print "Ratio=", x
            #Added another check for coverage greater than the estimated average coverage
            if(int(vals[0])+int(vals[1])>=coverage):
               print "Considered"
               out.write(x)
            print "Gap less than 10%"
            print count.most_common(1)

            #Write depth for each ratio
            print "Homozygous found"
            print "d=", d
            d = str(round(max(vals)/(min(vals)+max(vals)),2)) + "," + str(true_columns[j][0]) + "\n"
            df.write(d)
                  
    print "Number of homozygous sites = ", homozygous_count        
       
            
def dict_to_csv(wt_frac_dict):
   ''' 
   Writes a dictionary to a csv file
   (dict->file)
   ''' 
   with open(outputfile, 'wb') as csv_file:
       writer = csv.writer(csv_file)
       for key, value in wt_frac_dict.items():
          writer.writerow([key, value])


def usage():

    print(__doc__)
    print(epi)
    print ("python extract-msa.py -i <msa-file> -o <outputfile> -p <Gap percentage> -c <estimated coverage>")


def main(argv):
   
   ts = datetime.datetime.now()
   if(len(argv)==0):
        print ('\nERROR!:No input provided\n\nUsage: python extract-msa.py -i <msa-file> -o <outputfile> -p <Gap percentage> -c <estimated coverage>')
        sys.exit(2)
   inputfile = ''
   outputfile = "output_msa.csv"
   percent=10
   coverage=0
   try:
      opts, args = getopt.getopt(argv,"hi:o:p:c:",["ifile=","ofile=","percent=","coverage="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-p", "--percent"):
         percent = int(arg)
      elif opt in ("-c", "--coverage"):
         coverage = int(arg)


   
   if(inputfile==''):  
      print "\n\n ERROR: Missing input argument. MSA file is required.\n"
      usage()
      sys.exit(2)
  

   print 'MSA inputfile is: ', inputfile
   print 'Output file is: ', outputfile
   print 'Allowed Gap percentage is: ', percent
   read_msa_compute_zygosity(inputfile, outputfile, percent, coverage)

   tf = datetime.datetime.now()
   print "\n Time required - ",tf-ts

  
if __name__ == "__main__":
   main(sys.argv[1:])
