#!/usr/bin/python
'''
analyze_hetero.py

Created by Hamza Khan on 2018-07-24

A script to analyze the performance of the tool, hetero
'''

import argparse
import csv
import os
from simplesam import Reader, Writer

class analyze_hetero(object):
    
    def __init__(self, samfile, vcf, graph):
        self.samfile = samfile
        self.vcf = vcf
        self.graph = graph

    def read_vcf(self):
        """
        Reads a VCF file and makes a dictionary 

        Args: None
        Returns:dictionary of vcf records

        read_vcf()->dict
        """
        pass   

    def read_sam(self):
        """
        Reads a SAM file and makes a dictionary 

        Args: None
        Returns:dictionary of SAM records

        read_sam()->dict
        """
        in_file = open(self.samfile, 'r')
        in_sam = Reader(in_file)
        for record in in_sam:
            print record.qname

    def read_graph(self):
        """
        Reads a DOT graph file and makes a graph object 

        Args: None
        Returns:graph object

        read_graph()->obj
        """
        pass 



def _parse_args():

    #Parse command line arguments
    parser = argparse.ArgumentParser(
        description = 'Analyze hetero output using alignment and VCF files')

    #Positional arguments
    parser.add_argument('-i', '--HeteroGraph',
                       default = 'None', required = True,
                       help = 'Graph file from hetero')

    parser.add_argument('-v', '--vcf',
                       default = 'None', required=True,
                       help = 'VCF file')

    parser.add_argument('-s', '--samfile',
                       default = 'None', required = True,
                       help = 'Reads to reference alignment file(SAM)') 

    args = parser.parse_args()
    return args

def main():
    '''Parse arguments'''
    args = _parse_args()
    obj = analyze_hetero(args.samfile, args.vcf, args.HeteroGraph)
    obj.read_sam()


if __name__=='__main__':
    main()
