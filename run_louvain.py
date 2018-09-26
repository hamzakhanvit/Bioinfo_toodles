
'''
run_louvain.py

Created by Hamza Khan on 2018-09-25

A script to test the Networkx Louvain algorithm implementation
'''

import argparse
from collections import defaultdict
import networkx as nx
import community
import matplotlib.pyplot as plt



class louvain(object):
    
    def __init__(self, G):
        self.G = G


    def run_louvain(self, G):
        """
        Given a graph object runs the Louvain algorithm  

        Args: None
        Returns:print nodes and their assigned clusters

        louvain()->None
        """               
        #first compute the best partition
        partition = community.best_partition(G)
        for x in partition:
             print x, partition[x]

        print "FINISHED"

        #drawing
        '''
        size = float(len(set(partition.values())))
        pos = nx.spring_layout(G)
        count = 0.
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))

        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()
        plt.savefig('louvain_output.png')

        '''

    def read_graph(self):
        """
        Reads a DOT graph file and makes a graph object 

        Args: None
        Returns:graph object

        read_graph()->obj
        """
        graph = nx.drawing.nx_agraph.read_dot(self.G)
        self.run_louvain(graph)


def _parse_args():

    #Parse command line arguments
    parser = argparse.ArgumentParser(
        description = 'Run networkx Louvain algorithm')

    #Positional arguments

    parser.add_argument('-g', '--graphdotfile',
                       default = 'None', required=True,
                       help = 'Graph DOT file')

    args = parser.parse_args()
    return args


def main():
    '''Parse arguments'''
    args = _parse_args()
    obj = louvain(args.graphdotfile)
    obj.read_graph()
   

if __name__=='__main__':
    main()
