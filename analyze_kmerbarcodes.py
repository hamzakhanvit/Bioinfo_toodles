
'''
analyze_hetero.py

Created by Hamza Khan on 2018-07-24

A script to analyze common kmers between 10x barcodes
'''

import argparse
import csv
import os
import re
import math
import pprint
from collections import defaultdict
import networkx as nx

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



class analyze_kmerbarcode(object):
   
 
    barcode_dict = defaultdict(dict)
    
    def __init__(self, kmerbarcode):
        self.kmerbarcode = kmerbarcode

    def read_barcodefile(self):
        """
        Reads a tsv file and makes a dictionary 

        Args: None
        Returns:dictionary of reads(key) and barcodes(value)

        read_barcode()->dict
        """  
             
        with open(self.kmerbarcode, 'r') as in_file:
            for line in in_file:
                if line.startswith("kmer"):
                    continue
                line = list(set(line.strip().split("\t")[1:]))
                #print line
                for a in line:
                    for b in line:
                        if(a!=b and b not in self.barcode_dict[a]): 
                             self.barcode_dict[a][b] = 1
                             continue
                        if(a!=b and b in self.barcode_dict[a]):
                             self.barcode_dict[a][b] += 1
            #pprint.pprint(dict(self.barcode_dict), width=1)
        
   
 
    def make_graph(self):
        """
        Given a dictionary, creates a networkx graph
        """
        G = nx.Graph()
        for barcodeA in self.barcode_dict:
            for barcodeB in self.barcode_dict[barcodeA]:
                G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])
                cc = sorted(nx.connected_components(G), key = len, reverse=True)
                #print barcodeA, " ", barcodeB
                #print "First component size = ", len(cc[0]),
                if(len(cc)>1): 
                    #print "Second component = ", len(cc[1])  
                    if(len(cc[0]) > (len(cc[1])*5)):
                        print barcodeA, " ", barcodeB
                        print "First component size = ", len(cc[0]),"Second component = ", len(cc[1])
                        G.remove_edge(barcodeA,barcodeB)
                        cc = sorted(nx.connected_components(G), key = len, reverse=True)
                        print "After removing -> First component size = ", len(cc[0]),\
                              "Second component = ", len(cc[1]), "Third component = ", len(cc[2]),\
                              "Fourth component = ", len(cc[3])
 
        #Remove edges with less than kmer length +-5 edge weight
        k_len = [41]
        for i in range(0,4):k_len.append(k_len[-1]*2)
        for e in G.edges(data=True):
            if(any(e[2]['weight'] < k+5 and e[2]['weight'] > k-5 for k in k_len))==False:
            #if(e[2]['weight'] < 35):
                G.remove_edge(e[0],e[1]) 
        nx.drawing.nx_agraph.write_dot(G,'file.dot')

        #Remove nodes with less than 5 degree
        nodes_to_remove=[]
        for node in G.nodes():
            if G.degree(node)<8:
                nodes_to_remove.append(node)  

        for node in nodes_to_remove: 
            G.remove_node(node)

        #Print top three connected components
        cc = sorted(nx.connected_components(G), key = len, reverse=True)
        print "First component = ", cc[0]
        print "Second component = ", cc[1]


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
        description = 'Analyze kmers common between barcodes')

    #Positional arguments

    parser.add_argument('-b', '--kmerbarcodefile',
                       default = 'None', required=True,
                       help = 'kmer barcode file')

    args = parser.parse_args()
    return args

def main():
    '''Parse arguments'''
    args = _parse_args()
    obj = analyze_kmerbarcode(args.kmerbarcodefile)
    obj.read_barcodefile()
    obj.make_graph()

if __name__=='__main__':
    main()
