#!/usr/env python

from graph_utils import GraphGen, HAlgorithm, FloydWarshall
from graph import Graph, Node, Edge, SteinerTree
from random import choice

# Testing the H algorithm with a known instance
g = Graph()
nodes = []
for i in range(9):
    nodes.append(Node(i+1))
    g.add_node(nodes[i])
g.add_edge(Edge(nodes[0], nodes[1], 10))
g.add_edge(Edge(nodes[0], nodes[8], 1))
g.add_edge(Edge(nodes[1], nodes[5], 1))
g.add_edge(Edge(nodes[1], nodes[2], 8))
g.add_edge(Edge(nodes[2], nodes[3], 9))
g.add_edge(Edge(nodes[2], nodes[4], 2))
g.add_edge(Edge(nodes[3], nodes[4], 2))
g.add_edge(Edge(nodes[4], nodes[5], 1))
g.add_edge(Edge(nodes[4], nodes[8], 1))
g.add_edge(Edge(nodes[5], nodes[6], 1))
g.add_edge(Edge(nodes[6], nodes[7], 0.5))
g.add_edge(Edge(nodes[7], nodes[8], 0.5))

terminals = [nodes[0], nodes[1], nodes[2], nodes[3]]
ha = HAlgorithm(g, terminals, FloydWarshall(g))
tree = ha.get_steiner_tree()
print 'The HAlgorithm answer'
for e in tree.get_edges():
    print e
print '\n'

g = SteinerTree()
nodes = []
for i in range(10):
    nodes.append(Node(i+1))
    g.add_node(nodes[i])
g.add_edge(Edge(nodes[0],nodes[1], 1))
g.add_edge(Edge(nodes[1],nodes[2], 1))
g.add_edge(Edge(nodes[2],nodes[3], 1))
g.add_edge(Edge(nodes[1],nodes[4], 1))
g.add_edge(Edge(nodes[4],nodes[5], 1))
g.add_edge(Edge(nodes[1],nodes[6], 1))
g.add_edge(Edge(nodes[6],nodes[7], 1))
g.add_edge(Edge(nodes[6],nodes[8], 1))
g.add_edge(Edge(nodes[8],nodes[9], 1))
g.add_terminal(nodes[0])
g.add_terminal(nodes[5])
print 'Generated SteinerTree:'
print g
g.del_useless_edges()
print 'After deleting all useless:'
print g
print '\n'

g = GraphGen.generate(5)
#Graph.draw(g, 'minhaImagem.png')

print 'Printing the random generated graph'
for e in g.get_edges():
    print e,
print '\n'

print 'The minimum spanning tree: '
mst = g.get_mst_kruskal()
for e in mst:
    print e,
print '\n'

print "The minimum path of all-pairs: "
fw = FloydWarshall(g)
n = g.get_nodes()
print [ n.label for n in fw.get_min_path(choice(n), choice(n)) ]
