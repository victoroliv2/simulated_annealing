#!/usr/bin/env python

"""stein.py
Stein : a Steiner Tree problem solver

Usage:
./stein.py [--help] [--draw <filename>] [<instance>]

    --help (-h) : print this message
    --draw (-d) : draw the solution found. It needs of 'gvgen' and 'pygraphviz'
                  modules installed
    <instance>  : a graph description file. If no one is given, the program will
                  generate a random one.
"""

import sys
import getopt
import time
from simulannealing import SimulatedAnnealing as SimulAnn
import graph as Graph
from graph_utils import GraphGen

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def read_from_file(filename):
    g = Graph.Graph()
    try:
        f = open(filename, 'r')
    # Commented because python 2.5 doesnt understand it
    except IOError: #as (errno, strerror):
        print "I/O error({0}): {1}"#.format(errno, strerror)
        return (None, None)
    num_nodes = int(f.readline().split()[1])
    num_edges = int(f.readline().split()[1])

    print 'Read %d nodes and %d edges' %(num_nodes, num_edges)
    nodes = {}
    for i in xrange(num_nodes):
        nodes[i] = Graph.Node(i + 1)
        g.add_node(nodes[i])
    for i in xrange(num_edges):
        u, v, w = f.readline().split()[1:]
        g.add_edge(Graph.Edge(nodes[int(u)-1], nodes[int(v)-1], float(w)))

    # Read a empty line
    f.readline()

    num_term = int(f.readline().split()[1])
    terminals = [nodes[int(f.readline().split()[1])-1] for i in
            xrange(num_term)]
    f.close()

    return (g, terminals)

def print_tree(tree, arg):
    if not isinstance(arg, str):
        arg = 'Randomly generated instance'
    print 'Solucao: %s' %arg
    print 'Valor: %f' %tree.get_cost()
    print 'Arestas usadas: %d' %len(tree.get_edges())
    for e in tree.get_edges():
        print '%s %s' %(str(e.u.label), str(e.v.label))

def process(arg, draw=False, filename=None):
    if arg is None:
        graph, terminals = GraphGen.generate(steiner=True)
    else:
        graph, terminals = read_from_file(arg)

    steiner = SimulAnn(graph, terminals).get_min_steiner_tree()
    if draw is True:
        steiner.draw(filename)
    print_tree(steiner, arg)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        draw=False
        filename=None
        try:
            opts, args = getopt.getopt(argv[1:], "h:d", ["help", "draw="])
        except getopt.error, msg:
            raise Usage(msg)
        # Process options
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 0
            elif o in ("-d", "--draw"):
                draw = True
                filename = a
        # Process arguments
        map(lambda arg: process(arg, draw, filename), args)
        if args == []:
            process(None)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
