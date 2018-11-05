from collections import defaultdict


def dfs(g, root):
    q = []
    q.append(root)
    visited=set()
    while len(q)!=0:
         node = q.pop()
         if node not in visited:
             visited.add(node)
             print "Node = ", node  
	     for child in g[node]:
	         print child
                 q.append(child)

def cc(g):
    q = []
    c = defaultdict(set)
    visited = set()
    count=0
    gcopy = g.copy()
    for root in g:
        if root not in visited:
            count+=1
            c[count].add(root)
            q.append(root)           
            while len(q)!=0:
                node = q.pop()
                if node not in visited:
                    visited.add(node)
                    for child in gcopy[node]:
                        q.append(child)
                        c[count].add(child)
        
    return c   



def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))


def main():

    g = defaultdict(list)

    #Make a graph
    g['A'] = set(['B','C'])
    g['B'] = set(['D','E', 'A'])
    g['C'] = set(['F','G', 'A'])

    #Simple DFS
    dfs(g,'A')

    #Add more stuff to the graph to get 
    #more than one connected components
    g['P'] = set(['Q', 'R'])
    g['Q'] = set(['S', 'T', 'P'])
    g['R'] = set(['U', 'V', 'P']) 

    
    #Find connected components
    cc(g)

    #Join nodes A and B
    g['B'] = set(['D','E', 'A', 'C'])

    graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}

    print cc(graph)

    #Find paths from A to F
    print list(dfs_paths(graph, 'A', 'F'))


    

if __name__=='__main__':
    main()
