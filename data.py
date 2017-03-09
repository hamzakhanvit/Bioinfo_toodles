#!/usr/bin/env python
"""
DATA.PY
Author: Hamza Khan

This script generates a data file for a heatmap.

Inputs: 
1) 021717_v3_edges_links_for_contact_map.csv


Output: A formatted csv file 
[Default: out.csv]
"""

import sys,getopt,time
from collections import defaultdict
     
__title__ = 'data.py'
__version__ = 'v0.0'
__description__ = "A script that generates a data file for a heatmap"
__author__ = 'Hamza Khan'
__comment__ = ''
__author_email__ = "hamza.khan1@ucalgary.ca"
epi = "By %s. %s <%s>\n\n" % (__author__,
__comment__,
__author_email__)
__doc__ = "\n***********************************************\
************************************\
\n %s v%s - %s \n**********************************\
***********************************************\
**\n%s" % (__title__,
__version__,
__description__,
epi)


def file_to_dict(fname, out):
   '''
    Reads input file, orders the nodes by cluster
    and length and writes the ordered list in the 
    output file
    
    Input: csv input and output filenames 
    
    Returns: 1 if successfull
   '''     

   #Declaring two dictionaries
   clust_dict = defaultdict(list)  
   len_dict = defaultdict(list)
   link_dict = defaultdict(list)
   cov_dict = defaultdict(list)
   
   #Opening input and output files for reading and writing
   fh = open(fname, 'r')
   fo = open(out, 'w')
   
   for line in fh:
       
       line=(line.strip()).split(',')
       
       #Skipping the first line in the csv file
       if(line[0]=='edge'):
           continue
       
       '''
       #Extra varibles for future use
       edge=line[0]
       name_n1=line[3]
       med_cov_n1=line[6]
       pct_cov_n1=line[7]
       name_n2=line[10]
       med_cov_n2=line[13]
       pct_cov_n2=line[14]
       '''
       #Storing the required info in variables
       nlinks=line[1]
       n1=line[2]
       length_n1=line[4]
       cluster_n1=line[8]
       n2=line[9]
       length_n2=line[11]
       cluster_n2=line[15]
       avg_cov_n1=line[5]
       avg_cov_n2=line[12]

       #Storing cluster_ids as keys and nodes as values
       clust_dict[cluster_n1].append(n1)
       clust_dict[cluster_n2].append(n2)          
       
       #Storing node_ids as keys and length of nodes as values
       len_dict[n1] = int(length_n1)
       len_dict[n2] = int(length_n2)

       #Storing node_ids as keys and coverage as values
       cov_dict[n1] = float(avg_cov_n1)
       cov_dict[n2] = float(avg_cov_n2) 
       
       l = []
       l.append(n2)
       l.append(nlinks)
       link_dict[n1].append(l)
       
       l=[]
       l.append(n1)
       l.append(nlinks)
       link_dict[n2].append(l)
   
   #print(link_dict)
      
   clusters=[]
   #Making set of nodes unique for a cluster
   for key in clust_dict:
       clusters.append(key)
       clust_dict[key]=list(set(clust_dict[key]))
       
   #Making the clusters list unique and sorted
   #I have assumed that cluster 1 is the biggest and cluster 8 the smallest    
   clusters=list(set(clusters))
   clusters.sort()

   #Ordering and writing nodes to the output file
   ordered_list=[]
   fo.write('n1, n2, nlinks\n')
   for item in clusters:
       clust_dict[item] = sorted(clust_dict[item],  key=len_dict.get)
       for a in clust_dict[item]:           
           ordered_list.append(a)
   
   '''
   #Code snippet to check no. of nodes in each cluster
   i=0    
   #print("\n\n")    
   for key in clust_dict:  
         i+=len(clust_dict[key])
         print(key,len(clust_dict[key])) 
   #print("i=",i)
   ''' 

   for item in ordered_list:
       if item in link_dict:
           for connection in link_dict[item]:
               #print (connection)
               #print(item)
               s = (str(item) + ',' + connection[0] + ',' + connection[1] + '\n')
               #print(s)
               fo.write(s)
   fo.close()
       
   fo = open('out2.csv', 'w')  
   fo.write('ordering,nlength,coverage\n')   
   for item in ordered_list:
        fo.write("%s,%d,%f\n" % (item, len_dict[item], cov_dict[item]))
   fo.close()     
    
   return 1


def usage():
    print("Usage: python data.py -i <input_csv_file> -o\
<output_filename [Default: out.csv]> \n")
    sys.exit(2) #Exit the program


def main(argv):
    
   #Checking if no input has been provided 
   if(len(argv)==0):
        print('\nERROR!:No input provided\n')
        usage()
        
   #Default output filename
   output_filename = 'out.csv'
   
   #Try and Catch block for handling input errors
   try:
      opts, args = getopt.getopt(argv,"h:i:o:",["help=","ifile=","ofile="])
      
   except getopt.GetoptError:
      print(__doc__)
      usage()
     
   #Check whether the mandatory files are given as inputs  
   short_opts = [i[0] for i in opts]
   if(('-i') not in short_opts):
       print ("ERROR: Missing input. Please provide -i")
       usage()

   #Reading user inputs
   for opt, arg in opts:
       
      if opt == '-h':
         print(__doc__)
         usage()
         sys.exit()

      elif opt in ("-i", "--ifile"):
         fname = arg

      elif opt in ("-o", "--ofile"):
         output_filename = arg
         
   print(__doc__,'Input file is \n%s\n\n Output file is %s' %( fname, output_filename))
   print( '----------------------------------------\nRunning Script\n--------------\
--------------------------\n')
   
   #Variable to record time 
   start_time = time.time()
 
   #Calling function and storing the returned dicts 
   success = file_to_dict(fname, output_filename)
   
   #Checking if everything ran successfully
   if(success):
       print ('Done! Time elapsed: %.4f seconds' % (time.time() - start_time))


if __name__ == "__main__":
    
   #Call main function with the input arguments 
   main(sys.argv[1:])
