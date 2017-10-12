#!/usr/bin/env python

'''
Calculate coverage from minimap PAF file

Usage: python calc-ref-cov.py -i ecoli.e0.fq_to_reference.paf 
-s ~/simpsonlab/data/references/ecoli_k12.fasta
-q ~/simpsonlab/users/h2khan/projects/preqc-lr/dataset/wgsim/ecoli.e0.fq

'''

__title__ = 'calc-ref-cov.py'
__version__ = '1.0'
__description__ = "Calculate coverage from minimap PAF file"
__author__ = 'Hamza Khan'
__license__ = 'MIT License,'
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


try:
    from collections import defaultdict
    import sys,getopt,csv,time

except ImportError:
    print ('One of the required packages is not installed. Check pre-reqs')


def usage():
    print("\nUsage: python extract-alignments.py\
 -i <PAFfile>\n \
 -s <Subject FASTA file>\n \
 -q <Query FASTQ file>\n \
 -h --help\tHelp option\n\n")
    sys.exit(2)


def readfq(fp):
    '''
    Heng Li's fast Fastq reader
    '''
    last = None # this is a buffer keeping the last unprocessed line
    while True: # mimic closure; is it a bad idea?
        if not last: # the first record or a record following a fastq
            for l in fp: # search for the start of the next record
                if l[0] in '>@': # fasta/q header line
                    last = l[:-1] # save this line
                    break
        if not last: break
        name, seqs, last = last[1:].partition(" ")[0], [], None
        for l in fp: # read the sequence
            if l[0] in '@+>':
                last = l[:-1]
                break
            seqs.append(l[:-1])
        if not last or last[0] != '+': # this is a fasta record
            yield name, ''.join(seqs), None # yield a fasta record
            if not last: break
        else: # this is a fastq record
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp: # read the quality
                seqs.append(l[:-1])
                leng += len(l) - 1
                if leng >= len(seq): # have read enough quality
                    last = None
                    yield name, seq, ''.join(seqs); # yield a fastq record
                    break
            if last: # reach EOF before reading enough quality
                yield name, seq, None # yield a fasta record instead
                break


def read_fastAQ(fname):
    '''
    Given a filename, reads fastq/fastq file
    and return a dictionary of sequences
    (file)->(dict)
    '''
    seq_dict={}
    print "\n\nReading file ", fname
    n, slen, qlen = 0, 0, 0
    fh=open(fname, 'r')
    for name, seq, qual in readfq(fh):
        seq_dict[name]=seq
        n += 1
        slen += len(seq)
        qlen += qual and len(qual) or 0
    print "Number of seqs = %d, Total length of seqs = %d, total quality score = %.2f" % (n, slen, qlen)
    return (seq_dict)

 


def alignments_per_read(inputfile):
   '''
   Reads the PAF input file, creates a dictionary
   with queryID as keys and a list of other columns as values 
   '''
   fh=open(inputfile, 'r')
   paf_dict=defaultdict(list)
   for line in fh:
       temp = (line.strip("\n")).split()
       paf_dict[temp[0]].append(temp[1:])
   #print (paf_dict)      
   #print (paf_dict['gi|556503834|ref|NC_000913.3|_424435_434434_0:0:0_0:0:0_1/1'])
   return paf_dict


def calc_coverage(paf_dict, sub_dict, query_dict):
    '''
    Calculates coverage as per the read alignment 
    and output it to a file
    (dict, dict, dict)->(file)
    '''
    cov_dict={}

    for key in sub_dict:
        reference = [-1] * len(sub_dict[key])
        for reads in query_dict:
            start = int((reads.split("|")[4]).split("_")[1])
            end = int((reads.split("|")[4]).split("_")[2])
            #print start, end
            for i in range(start-1, end):
                 reference[i]=0  
    #print reference

    for key in paf_dict:
        for alignment in paf_dict[key]:
            start = int(alignment[6])
            end = int(alignment[7])
            for i in range(start-1, end):
                if(reference[i]!=-1):reference[i] = reference[i] + 1
   
    for reads in query_dict:
            start = int((reads.split("|")[4]).split("_")[1])
            end = int((reads.split("|")[4]).split("_")[2])
            sum = 0
            for i in range(start-1, end):
                sum = sum + reference[i]
            avg = sum/(end-start+1)
            if (avg in cov_dict):
               cov_dict[avg] += 1             
            else:
               cov_dict[avg]=1
    return (cov_dict,1)     
     


def main(argv):
    
   #Checking if no input has been provided 
   if(len(argv)==0):
        print('\nERROR!:No input provided\n')
        usage()

   
   #Try and Catch block for handling input errors
   try:
      opts, args = getopt.getopt(sys.argv[1:],'h:i:s:q:',['help=','ifile=','subject=','query=',])
      
   except getopt.GetoptError:
      print __doc__ 
      usage()

   #Check whether the mandatory files are given as inputs  
   short_opts = [i[0] for i in opts]

   if(('-i') not in short_opts and ('--ifile') not in short_opts) or (('-s') not in short_opts and \
     ('--subject') not in short_opts) or (('-q') not in short_opts and ('--query') not in short_opts):
       print ("ERROR: Missing inputs. Please provide -i .")
       usage()
   

   subject = ""
   query = ""
   
   #Reading user inputs
   for opt, arg in opts:
      if opt in ("-h", "--help"):
          print(__doc__)
          usage()
 
      elif opt in ("-i", "--ifile"):
          inputfile = arg

      elif opt in ("-s", "--subject"):
          subject = arg

      elif opt in ("-q", "--query"):
          query = arg

                
   print __doc__,"Input PAF file is %s\n" \
 % inputfile
   print "----------------------------------------\nReading input PAF file\n--------------\
--------------------------\n"
   
   #Variable to record time 
   start_time = time.time()  
   paf_dict = alignments_per_read(inputfile) 
   sub_dict = read_fastAQ(subject)
   query_dict = read_fastAQ(query)
   success=0
   coverage_dict, success = calc_coverage(paf_dict, sub_dict, query_dict)
   #print coverage_dict

   #Write coverage distribution
   out = open("cov.csv", "w")
   out.write("coverage,count\n")
   for key in coverage_dict:
      s = str(key) + "," + str(coverage_dict[key]) + "\n"
      out.write(s) 
   out.close()
    
   if(success):
       print ('Done! Time elapsed: %.4f seconds' % (time.time() - start_time))


if __name__ == "__main__":
   main(sys.argv[1:])
