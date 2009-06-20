from graph_utils import FloydWarshall
from graph_utils import Neighborhood as Ngb
from graph_utils import HAlgorithm as HA
import math
import time
import random

class SimulatedAnnealing(object):

    def __init__(self, graph, terminals, percent=0.01, stop=40):
        """
        Percent and stop are used to determine when the execution can stop.
        It works as follow:
            After 'stop' iterations with difference of 'percent'% between them,
            the optimal solution found is returned. This avoid we stay much time
            turning around a solution without significant results.
        For small instances, one may want set 'percent' to 0.
        """
        self.graph = graph
        self.terminals = terminals
        self.optimal = None
        self.percent = percent
        self.stop = stop

    def get_min_steiner_tree(self, t_0=1, alfa=0.95, l1=20, l2=200):
        """
        Get the minimum steiner tree.
        Options:
            t_0: the initial temperature to start with
            alfa: the cooling rate
            l1: how many coolings to do
            l2: how many iterations over the same temperature
        """
        random.seed()
        fw = FloydWarshall(self.graph)
        current = HA(self.graph, self.terminals, fw).get_steiner_tree()
        self.optimal = current
        count = 0
        k = None
        t = t_0

        print 'Initial solution: %d' %current.get_cost()
        for i in xrange(l1):
            for j in xrange(l2):
                new_cur = Ngb.get(self.graph, current, fw)

                delta = new_cur.get_cost() - current.get_cost()
                # Nothing to do
                if delta == 0:
                    continue

                # In the beginning, k is such that every state is possible
                if k is None:
                    k = -(delta/(math.log(0.9999) * t))

                if delta < 0.0:
                    current = new_cur
                    if current.get_cost() < self.optimal.get_cost():
                        print 'New optimal solution: %d' \
                        %current.get_cost()
                        self.optimal = current
                else:
                    try:
                        if random.random() < math.exp(-(delta/(k * t))):
                            current = new_cur
                    except OverflowError:
                        return self.optimal

                # Stop after some time without significant good results
                if abs(delta) < self.percent * current.get_cost():
                    count += 1
                    if count >= self.stop:
                        print 'Stopping because little difference'
                        return self.optimal
                else:
                    count = 0
            t *= alfa
        return self.optimal
