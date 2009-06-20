#!/usr/bin/env python

import sys
sys.path.append("..")

import sys
import getopt
from time import time
from simulannealing import SimulatedAnnealing as SimulAnn
import graph as Graph
from graph_utils import GraphGen

# Tamanho previsto para as instancias aleatorias.
instances = [10, 50, 100, 200, 500, 700, 1000, 1500]

for i in instances:
	print '##### Tamanho da Instancia: ', i
	tempo = time()
	graph, terminals = GraphGen.generate(nodes_number=i, steiner=True)
	print 'Tempo de geracao: ', time()-tempo

	print 'Numero de terminais: ', len(terminals)
	
	tempo = time()
	steiner = SimulAnn(graph, terminals).get_min_steiner_tree()
	print 'Tempo de execucao da heuristica: ', time()-tempo

