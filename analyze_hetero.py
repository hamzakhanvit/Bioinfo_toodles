
'''
analyze_hetero.py

Created by Hamza Khan on 2018-07-24

A script to analyze the performance of the tool, hetero
'''

import argparse
import csv
import os
import vcf
import re
import math
from collections import defaultdict
from simplesam import Reader, Writer



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
    
    def __init__(self, samfile, vcfile, graph):
        self.samfile = samfile
        self.vcfile = vcfile
        self.graph = graph

    def read_vcf(self):
        """
        Reads a VCF file and makes a dictionary 

        Args: None
        Returns:dictionary of vcf records

        read_vcf()->dict
        """  
        vcf_reader = vcf.Reader(open(self.vcfile))
        #for record in vcf_reader:
        #    print record   

    def read_sam(self):
        """
        Reads a SAM file and makes a dictionary 

        Args: None
        Returns:dictionary of SAM records

        read_sam()->dict
        """
        in_sam = Reader(open(self.samfile, 'r'))
        #for record in in_sam:
        #    print record.qname

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
    obj.read_vcf()
    obj.read_graph()

if __name__=='__main__':
    main()
