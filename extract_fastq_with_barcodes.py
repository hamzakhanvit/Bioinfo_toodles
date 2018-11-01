'''
Given a file of barcodes, 
extract all fastq sequences having that barcode
'''

from Bio import SeqIO
import argparse
from collections import defaultdict

class extract_fq():

    def __init__(self, inputfile, barcodefile):
        self.inputfile = inputfile
        self.barcodefile = barcodefile   


    def write_fastq_from_records(self, records_to_write, out):
        '''
        Given a list of fastq records, write a fastq file
        '''
        SeqIO.write(records_to_write, out, "fastq")


    def read_fastq(self, barcodes):
        '''
        Reads the input FASTQ file 
                                 
        Input: filename                              
        Returns -> None
        '''
        fastqs = defaultdict(list)
        records_to_write=[]

        with open(self.inputfile, "rU") as handle:
           for record in SeqIO.parse(handle, "fastq"):
               if len(record.description.split())>1:
                   barcode = record.description.split()[1] 
               else:
                   continue
               if barcode in barcodes:
                   records_to_write.append(record)               
        return records_to_write               
    
    
    def read_barcode(self):
        '''
        Read the barcode file and make a dictionary
    
        Input: Filename
        Returns -> dict
        ''' 
        barcodes = set() 
        with open (self.barcodefile, 'r') as bc:
            for line in bc:
               line = line.rstrip()
               barcodes.add(line)
        return barcodes



def parse_args():
    """Parse command line arguments"""
    
    parser = argparse.ArgumentParser(
             description = 'Given a file of barcodes, extract all fastq sequences having that barcode')

    parser.add_argument('-f', '--fastq', 
                       default = None, required = True,
                       help = "FASTQ file")

    parser.add_argument('-b', '--barcode',
                       default = None, required = True,
                       help = "Barcode file")

    args = parser.parse_args()
    return args



def main():

    args = parse_args()
    obj = extract_fq(args.fastq, args.barcode)
    out = args.barcode[:-7] + "fastq"
    barcodes = obj.read_barcode()
    print "Finished reading barcodes"
    records_to_write = obj.read_fastq(barcodes)
    print "Made a list of records to write"
    obj.write_fastq_from_records(records_to_write, out)
    print "Wrote fastq file. END"


if __name__=='__main__':
    main()
