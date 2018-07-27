
'''
analyze_hetero.py

Created by Hamza Khan on 2018-07-24

A script to analyze the performance of the tool, hetero
'''

import argparse
import csv
import os
import re
import math
from collections import defaultdict

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())



class analyze_hetero(object):

    BED_HEADERS = ['vcfchr','vcfstart','vcfend','kmerid','kmerstart','kmerend']

    READBED_HEADERS = ['vcfchr','vcfstart','vcfend','readid','readstart','readend']
   
    READ_BARCODE = ['ID','barcode']
 
    read_barcode_dict = {}
    num_snps_per_barcode = {}
    
    def __init__(self, bedfile, kmerbed, readbarcode, graph):
        self.bedfile = bedfile
        self.kmerbed = kmerbed
        self.readbarcode = readbarcode
        self.graph = graph


    def read_barcode(self):
        """
        Reads a VCF file and makes a dictionary 

        Args: None
        Returns:None

        read_barcode()->None
        """  
        in_file = csv.DictReader(open(self.readbarcode, 'r'), skipinitialspace=True,
                               delimiter=' ', fieldnames=self.READ_BARCODE)        
 
        for row in in_file:
           self.read_barcode_dict[row['ID']] = row['barcode']         


    @staticmethod
    def find_common_snps_in_barcodes(read_bed_snp_dict):
        #print read_bed_snp_dict
        common_snps_dict = defaultdict(dict)
        for snp in read_bed_snp_dict:
            barcode_list = read_bed_snp_dict[snp]
            #print barcode_list
            for i in xrange(0, len(barcode_list)):
                for j in xrange(0, len(barcode_list)):
                    print "i =", i ,"  " ,barcode_list[i], " j = ", j, " ", barcode_list[j], "\n"
                    if barcode_list[j] in common_snps_dict[barcode_list[i]] and barcode_list[i]!=barcode_list[j]:
                        common_snps_dict[barcode_list[i]][barcode_list[j]]+=1
                    if barcode_list[j] not in common_snps_dict[barcode_list[i]] and barcode_list[i]!=barcode_list[j]:
                        common_snps_dict[barcode_list[i]][barcode_list[j]]=1
        ''' 
        for key1 in common_snps_dict:
            for key2 in common_snps_dict[key1]:
               print "Barcode ", key1, "," , key2, ",", common_snps_dict[key1][key2], "\n"                
        '''


    def read_bed(self):
        """
        Reads a bed file and makes a dictionary 

        Args: None
        Returns:None

        read_bed()->None
        """
        read_bed_snp_dict = defaultdict(list)
        read_bed_indel_dict = defaultdict(list)
        barcode_count_per_snp = {}     
        barcode_count_per_indel = {}


        in_bed = csv.DictReader(open(self.bedfile, 'r'), skipinitialspace=True,
                               dialect=csv, fieldnames=self.READBED_HEADERS)
        next(in_bed)
        
        for row in in_bed:
            read_id = re.sub(r'(/.)', '', row['readid'])      
            if(int(row['vcfend'])-int(row['vcfstart'])==1):    
                read_bed_snp_dict[row['vcfchr']+row['vcfstart']].append(self.read_barcode_dict[read_id])
            else:
                read_bed_indel_dict[row['vcfchr']+row['vcfstart']].append(self.read_barcode_dict[read_id])

        for key in read_bed_snp_dict:
            read_bed_snp_dict[key] = list(set(read_bed_snp_dict[key]))
            if(len(read_bed_snp_dict[key])) in barcode_count_per_snp:
                barcode_count_per_snp[len(read_bed_snp_dict[key])]+=1
            else:
                barcode_count_per_snp[len(read_bed_snp_dict[key])]=1            
           
        for key in read_bed_indel_dict:
            read_bed_indel_dict[key] = list(set(read_bed_indel_dict[key]))
            if(len(read_bed_indel_dict[key])) in barcode_count_per_indel:
                barcode_count_per_indel[len(read_bed_indel_dict[key])]+=1
            else:
                barcode_count_per_indel[len(read_bed_indel_dict[key])]=1
 
        self.find_common_snps_in_barcodes(read_bed_snp_dict)


    def read_kmer_bed(self):
        """
        Reads a kmer bed file, makes a dictionary,
        computes kmers per SNP and indels per SNP,
        writes output filed 

        Args: None
        Returns:None

        read_bed()->file,file
        """
        kmer_bed_snp_dict = defaultdict(list)
        kmer_bed_indel_dict = defaultdict(list)   
        kmer_count_per_snp = {}     
        kmer_count_per_indel = {}

        in_bed = csv.DictReader(open(self.kmerbed, 'r'), skipinitialspace=True,
                               dialect=csv, fieldnames=self.BED_HEADERS)
        next(in_bed)
        for row in in_bed:
          
           if(int(row['vcfend'])-int(row['vcfstart'])==1):
               kmer_bed_snp_dict[row['vcfchr']+row['vcfstart']].append(row['kmerid'])
           else:
               kmer_bed_indel_dict[row['vcfchr']+row['vcfstart']].append(row['kmerid'])
       

        for key in kmer_bed_snp_dict:
            kmer_bed_snp_dict[key] = list(set(kmer_bed_snp_dict[key]))
            if(len(kmer_bed_snp_dict[key])) in kmer_count_per_snp:
                kmer_count_per_snp[len(kmer_bed_snp_dict[key])]+=1
            else:
                kmer_count_per_snp[len(kmer_bed_snp_dict[key])]=1

        for key in kmer_bed_indel_dict:
            kmer_bed_indel_dict[key] = list(set(kmer_bed_indel_dict[key]))
            if(len(kmer_bed_indel_dict[key])) in kmer_count_per_indel:
                kmer_count_per_indel[len(kmer_bed_indel_dict[key])]+=1
            else:
                kmer_count_per_indel[len(kmer_bed_indel_dict[key])]=1

        with open('kmer_count_per_snp.csv', 'wb') as f: 
            f.write('kmer_per_snp,count\n')
            for k, v in kmer_count_per_snp.items():
                f.write(str(k) + ','+ str(v) + '\n')
     
       
        with open('kmer_count_per_indel.csv', 'wb') as f:
            f.write('kmer_per_indel,count\n')
            for k, v in kmer_count_per_indel.items():
                f.write(str(k) + ','+ str(v) + '\n')
   


    def read_graph(self):
        """
        Reads a DOT graph file and makes a graph object 

        Args: None
        Returns:graph object

        read_graph()->obj
        """
        graph = Graph()
        #graph = defaultdict(list)
        with open(self.graph) as g:
            for line in g:
                if(line.startswith('Graph')):
                    continue
                if("--" in line):
                    #print "Edge ", line
                    temp = line.strip().split("--")
                    vertexA = temp[0]
                    vertexB = temp[1].split("[")[0]
                    weight = re.findall("\d+\.\d+", temp[1].split("[")[1])[0]
                    graph.addEdge(vertexA, vertexB,cost=weight)                                   
        for v in graph:
            for w in v.getConnections():
                print("( %s , %s )" % (v.getId(), w.getId()))                     

 
def _parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description = 'Analyze hetero output using alignment and VCF files')

    #Positional arguments
    parser.add_argument('-i', '--HeteroGraph',
                       default = 'None', required = True,
                       help = 'Graph file from hetero')

    parser.add_argument('-b', '--readbarcodefile',
                       default = 'None', required=True,
                       help = 'Read barcode file')

    parser.add_argument('-r', '--readbed',
                       default = 'None', required = True,
                       help = 'Read BED file intersecting with vcf') 
 
    parser.add_argument('-k', '--kmerbed',
                       default = 'None', required = True,
                       help = 'Putative heterozygous kmers BED file intersecting with vcf') 

    args = parser.parse_args()
    return args

def main():
   
    args = _parse_args()
    obj = analyze_hetero(args.readbed, args.kmerbed, args.readbarcodefile, args.HeteroGraph)
    obj.read_barcode()
    obj.read_bed()
    obj.read_kmer_bed()
    #obj.read_graph()

if __name__=='__main__':
    main()
