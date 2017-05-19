#!/usr/bin/env python

import sys,pip,getopt,csv,time       
import random
from random import randint 
random.seed(100)

__title__ = 'haploid_generator'
__version__ = '1.0'
__description__ = "Generating haploids from a given single sequence\
 FASTA file by introducing SNPs once in every 200 basepairs."
__author__ = 'Hamza Khan'
__license__ = 'NULL'
__author_email__ = "hamza.khan@alumni.ubc.ca"

epi = "By %s, %s <%s>\n\n" % (__author__,
__license__,
__author_email__)
__doc__ = "\n***********************************************\
************************************\
\n %s v%s - %s \n**********************************\
***********************************************\
**\n%s" % (__title__,
__version__,
__description__,
epi)

def install(package):
    pip.main(['install', package])


try:
    from Bio import SeqIO
except ImportError:
    print ('BioPython is not installed, installing it now!')
    install('biopython')


def replace_str_index(text,index=0,replacement=''):
    '''
    Given a string, index and a replacement character,
    the function replaces the character at the given index
    (str, int)->(str)
    '''
    return '%s%s%s'%(text[:index],replacement,text[index+1:])


def chopseq(record, length):
    ''' 
    Introduces SNPs in a given sequence at given length and
    writes haplotypes A and B to two different FASTA files
    '''
    header = "HapB"
    hapB=""
    id = record.id
    seq = record.seq.tostring()
    for i in range(0, len(seq), length): 
         sequence = seq[i:i+length]
         #print ("sequence = ", sequence)

         if(len(seq)-i>=100):
             random_index = (randint(0,length-1))
             #print ("random_index =", random_index)

             ri_char = sequence[random_index]
             #print("ri_char =", ri_char)

             if (ri_char == 'A'):
                 re_char = random.choice('TGC')
                 re_sequence = replace_str_index(sequence,random_index,re_char)
                 header = header + ":" + str(i+random_index+1) + "_" + ri_char +  "_" + re_char           
                 hapB = hapB + re_sequence

             if (ri_char == 'T'):
                 re_char = random.choice('AGC')
                 re_sequence = replace_str_index(sequence,random_index,re_char)
                 header = header + ":" + str(i+random_index+1) + "_" + ri_char +  "_" + re_char
                 hapB = hapB + re_sequence

             if (ri_char == 'G'):
                 re_char = random.choice('ATC')
                 re_sequence = replace_str_index(sequence,random_index,re_char)
                 header = header + ":" + str(i+random_index+1) + "_" + ri_char +  "_" + re_char
                 hapB = hapB + re_sequence

             if (ri_char == 'C'):
                 re_char = random.choice('TGA')
                 re_sequence = replace_str_index(sequence,random_index,re_char)
                 header = header + ":" + str(i+random_index+1) + "_" + ri_char +  "_" + re_char
                 hapB = hapB + re_sequence
 
         else:
             
             hapB = hapB + sequence
          
    hapA_out = open ("HapA.fa", 'w')
    hapB_out = open ("HapB.fa", 'w')
    hapA_out.write(">" + id + "\n" + seq)
    hapB_out.write(">" + header + "\n" + hapB) 


def generate_haplo(inputfile,length):
    '''
    Reads the input FASTA file and calls 
    chopseq function
                                 
    Input: filename                              
    Returns -> 1 (if successful)
    '''
    
    with open(inputfile, "rU") as handle:
       for record in SeqIO.parse(handle, "fasta"):
           chopseq(record, length)
    
    return 1


def usage():
    print("\nUsage: python generate_haplotypes.py\
 -i <inputfile> -l <100> \n")
    sys.exit(2)


def main(argv):
    
   #Checking if no input has been provided 
   if(len(argv)==0):
        print('\nERROR!:No input provided\n')
        usage()

   
   #Try and Catch block for handling input errors
   try:
      opts, args = getopt.getopt(argv,"h:i:l:",["help=","ifile=", "length="])
      
   except getopt.GetoptError:
      print(__doc__)
      usage()

   #Check whether the mandatory files are given as inputs  
   short_opts = [i[0] for i in opts]
   if(('-i') not in short_opts):
       print ("ERROR: Missing inputs. Please provide -i .")
       usage()
   
   if(('-l') not in short_opts):
       print ("ERROR: Missing inputs. Please provide -l .")
       usage()
   
   #Reading user inputs
   for opt, arg in opts:
      if opt == '-h':
         print(__doc__)
         usage()

      elif opt in ("-i", "--ifile"):
         inputfile = arg

      elif opt in ("-l", "--length"):
         length = int(arg)
                
   print(__doc__,'Input file is %s\n' \
 %( inputfile))
   print( '----------------------------------------\nRunning Script\n--------------\
--------------------------\n')
   
   #Variable to record time 
   start_time = time.time() 

   success = generate_haplo(inputfile, length)  
    
   if(success):
       print ('Done! Time elapsed: %.4f seconds' % (time.time() - start_time))


if __name__ == "__main__":
    main(sys.argv[1:])
