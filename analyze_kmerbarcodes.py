
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
import community
import matplotlib.pyplot as plt

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
        
    '''
    def merge_sets(self):
        """
        Given a dictionary of kmers and barcodes, 
        makes sets that can be clubbed together
        """
        barcode_dict = {'BX:Z:CAAG-1': {'BX:Z:TGAG-1': 10, 'BX:Z:CAAT-1': 38}, 'BX:Z:TACC-1': {'BX:Z:GTAG-1': 41, 'BX:Z:ATTC-1': 41, 'BX:Z:CGAA-1': 41, 'BX:Z:AGGG-1': 41}, 'BX:Z:CAAT-1': {'BX:Z:GATA-1': 39, 'BX:Z:AGCC-1': 39, 'BX:Z:CAGG-1': 41, 'BX:Z:TACG-1': 41}, 'BX:Z:AGCA-1': {'BX:Z:TGAC-1': 39, 'BX:Z:ACGT-1': 41}}
        clusters = []
        #clusters_member = defaultdict(list)
        #setdict = defaultdict(set)
        barcode_cluster_dict = {}
        for barcodeA in self.barcode_dict:
            barcodeA_sets = []
            if barcode A in barcode_cluster_dict:
            


            else:
                for barcodeB in self.barcode_dict[barcodeA]:
                    if barcodeB in barcode_cluster_dict:
                    
                    else:
                            
            
            for s in xrange(0,len(clusters)): 
                if (barcodeA in clusters[s]):
                    barcodeA_sets.append(s)
                
    '''                         

    def debug(self):
        """
        Debugging graph formation and finding connected components
        """
        G = nx.Graph()
        f_comp = ()
        s_comp = ()
        flag = 0
        unadded_nodes = set()
        for barcodeA in self.barcode_dict:
            for barcodeB in self.barcode_dict[barcodeA]:
                    print barcodeA, " ", barcodeB
                    G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])
                    cc = sorted(nx.connected_components(G), key = len, reverse=True)
                    lens = []
                    for x in cc:
                         lens.append(len(x))
                    print "Number of components = ", len(lens), ", First 5 compenents size = ", lens[:5]
                    if(len(cc)>1 and len(cc[0])-len(cc[1])<(len(cc[0])/2) and flag == 0):
                        flag = 1
                    if(flag == 1 and len(cc)>1):
                        f_comp = cc[0]
                        s_comp = cc[1]
                        if(len(f_comp) > (len(s_comp)*5)):
                            print "Removing edge = ", barcodeA, " ", barcodeB
                            #print "First component size = ", len(cc[0]),"Second component = ", len(cc[1])
                            G.remove_edge(barcodeA,barcodeB)
                    if(flag == 1 and len(cc)==1): 
                        G.remove_edge(barcodeA,barcodeB)        
                        print "Removing Edge = ", barcodeA, " ", barcodeB 

       
        G = nx.Graph()
        for barcodeA in self.barcode_dict:
            for barcodeB in self.barcode_dict[barcodeA]:
                    #print barcodeA, " ", barcodeB
                    G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])
        
        #Print graph degree
        for node in G.nodes():
            print "Node ", node, " has degree = ", G.degree(node)

        #Print graph edge weights
        edges_to_remove=[]
        for edge in G.edges():
            print "edge ", edge, " has edge weight = ", G[edge[0]][edge[1]]['weight']
            if (G[edge[0]][edge[1]]['weight'] < 36  or G[edge[0]][edge[1]]['weight'] > 43):
                edges_to_remove.append(edge[:2])

        for edge in edges_to_remove:
            G.remove_edge(*edge)

        for node in G.nodes():
            print "After Node ", node, " has degree = ", G.degree(node)
        

        
        

    def merge_sets(self):
        """
        Given a dictionary of kmers and barcodes, 
        makes sets that can be clubbed together
        """
        G = nx.Graph()
        f_comp = ()
        s_comp = ()
        flag = 0
        unadded_nodes = set()
        for barcodeA in self.barcode_dict:
            for barcodeB in self.barcode_dict[barcodeA]:
                if(len(f_comp)>10000 and len(s_comp)>10000):
                    flag=1 
                if(flag==0): 
                    G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])
                    cc = sorted(nx.connected_components(G), key = len, reverse=True)
                    #lens = []
                    #for x in cc:
                    #     lens.append(len(x))
                    #print "Number of components = ", len(lens), ", First 5 compenents size = ", lens[:5]
                    if(len(cc)>1):
                        f_comp = cc[0]
                        s_comp = cc[1]
                        if(len(f_comp) > (len(s_comp)*5)):
                            #print barcodeA, " ", barcodeB
                            #print "First component size = ", len(cc[0]),"Second component = ", len(cc[1])
                            G.remove_edge(barcodeA,barcodeB)
                else:      
                    if ((barcodeA not in f_comp and barcodeB not in s_comp)):
                        #G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])
                        unadded_nodes.add((barcodeA,barcodeB))            

                    if ((barcodeA in f_comp and barcodeB not in s_comp) or (barcodeB in f_comp and barcodeA not in s_comp)):
                        G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])    

        cc = sorted(nx.connected_components(G), key = len, reverse=True) 
        f_comp = cc[0]
        s_comp = cc[1]
        print "Pre First component size = ", len(cc[0]),"Second component = ", len(cc[1]), "Third component = ", len(cc[2])   
        for barcodeA, barcodeB in unadded_nodes:
            if ((barcodeA in f_comp and barcodeB not in s_comp) or (barcodeB in f_comp and barcodeA not in s_comp)):
                G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])  
                          
        nx.drawing.nx_agraph.write_dot(G,'file_test.dot')
    


    def make_graph(self):
        """
        Given a dictionary, creates a networkx graph
        """
        G = nx.Graph()
        print "len(self.barcode_dict) = ", len(self.barcode_dict)
        for barcodeA in self.barcode_dict:
            for barcodeB in self.barcode_dict[barcodeA]:
                G.add_edge(barcodeA,barcodeB,weight=self.barcode_dict[barcodeA][barcodeB])
                cc = sorted(nx.connected_components(G), key = len, reverse=True)
                if(len(cc)>1): 
                    if(len(cc[0]) > (len(cc[1])*5)):
                        #print barcodeA, " ", barcodeB
                        #print "First component size = ", len(cc[0]),"Second component = ", len(cc[1])
                        G.remove_edge(barcodeA,barcodeB)
                        #cc = sorted(nx.connected_components(G), key = len, reverse=True)
                        #print "After removing -> First component size = ", len(cc[0]),\
                        #      "Second component = ", len(cc[1]), "Third component = ", len(cc[2]),\
                        #      "Fourth component = ", len(cc[3])

        nx.drawing.nx_agraph.write_dot(G,'file_rough.dot')      
 
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
            if G.degree(node)<5:
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
    #obj.make_graph()
    obj.debug()
    obj.merge_sets()

if __name__=='__main__':
    main()
