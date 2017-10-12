from graphviz import Source
import networkx as nx
import argparse, datetime
import sys, getopt
import networkx.drawing.nx_agraph as a

__title__ = 'Extract-graph.py'
__version__ = '1.0.0'
__description__ = "Given a graph DOT file, a node and a degree, it outputs a \
subgraph with the node and all nodes/edges at the given degree to the node."
__author__ = 'Hamza Khan'
__license__ = 'GPL license'
__author_email__ = "hamza.khan@alumni.ubc.ca"
epi = "Licence: %s by %s <%s>\n\n" % (__license__,
__author__,
__author_email__)
__doc__ = "***************************************************************\
          \n %s v%s - %s \n************************************************\
***************" % (__title__,
__version__,
__description__)

subgraph=[]


def graph_to_dot(G, outputfile):
    global subgraph
    #print(subgraph)
    g=G.subgraph(subgraph)
    #print "Final subgraph edges=", g.edges()
    nx.drawing.nx_agraph.write_dot(g,outputfile)

def outedges(G,nodename, degree):
    global subgraph
    if(degree==0):
       return
    else:
        #print "degree=", degree
        #print "subgraph = ", subgraph
        print G.out_edges(nodename)
        subgraph.extend(G.out_edges(nodename))
        #print "subgraph = ", subgraph
        degree-=1
        for item in G.out_edges(nodename):
              #print "item=", item
              outedges(G,item[1], degree)


def inedges(G,nodename, degree):
    global subgraph
    if(degree==0):
       return
    else:
        #print "degree=", degree
        print G.in_edges(nodename)
        #print "subgraph = ", subgraph
        subgraph.extend(G.in_edges(nodename))
        degree-=1
        for item in G.in_edges(nodename):
              #print "item=", item
              inedges(G,item[0], degree)



def read_dotfile(inputfile, nodename):
    G = a.read_dot(inputfile)
    return G


def usage():

    print(__doc__)
    print(epi)
    print ("python extract-graph.py -i <graph-dot-file> -n <node-name> -d <degree to be extracted> -o <graph-outputfile>")


def main(argv):
   
   ts = datetime.datetime.now()
   if(len(argv)==0):
        print ('\nERROR!:No input provided\n\nUsage: python extract-graph.py -i <graph-dot-file> -n <node-name> -d <degree to be extracted> -o <graph-outputfile>')
        sys.exit(2)
   inputfile = ''
   outputfile = 'outputgraph.dot'
   nodename=''
   degree=''
   global subgraph
   try:
      opts, args = getopt.getopt(argv,"hi:o:n:d:",["ifile=","ofile=","nodename=", "degree="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-n", "--nodename"):
         nodename = arg
      elif opt in ("-d", "--degree"):
         degree = int(arg)
   
   if(inputfile=='' or nodename=='' or degree==''):  
      print "\n\n ERROR: Missing one or more arguments. All arguments are necessary.\n"
      usage()
      sys.exit(2)
  

   print 'Graph Input file is: ', inputfile
   print 'Graph-output file is: ', outputfile
   print 'Node is: ', nodename
   print 'Degree is: ', degree
   G=read_dotfile(inputfile, nodename)
   print "\nOutedges are: \n" 
   outedges(G, nodename, degree)
   print "\nInedges are: \n"
   inedges(G,nodename, degree)
   subgraph = list(set([item for subtuple in subgraph for item in subtuple]))
   graph_to_dot(G, outputfile)

   tf = datetime.datetime.now()
   print "\n Time required - ",tf-ts

  
if __name__ == "__main__":
   main(sys.argv[1:])
