import graph as Graph
import random

class UnionFind(object):
    """
    This is a fast tree based data structure to work with disjoint-set. It aims
    to be O(alfa(n)), where 'alfa' is the inverse of the Ackermanns function.

    The data structure usually has 3 operation: MakeSet, Union and Find. But
    here, the MakeSet and Find operations were merged into just one special
    method
    """

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def __getitem__(self, object):
        """ Return the representant of the set that contains the object """
        # Include the object to the structure
        if object not in self.parent:
            self.parent[object] = object
            self.rank[object] = 0
            return object

        # Find the path starting from the object
        path = [object]
        root = self.parent[object]
        while root != path[-1]:
            path.append(root)
            root = self.parent[root]

        # Compress the path
        for child in path:
            self.parent[child] = root

        return root

    def union(self, x, y):
        """ Find the sets containing the objects and merge them """
        x_root = self.parent[x]
        y_root = self.parent[y]

        if self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        elif self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif x_root != y_root:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1

class FloydWarshall(object):
    """ Give the all-pairs shortest path on a graph """

    def __init__(self, graph):
        import floydwarshall as fw

        n = len(graph)

        m_adj = fw.new_doubleArray(n*n)
        dist  = fw.new_doubleArray(n*n)
        pred  = fw.new_intArray(n*n)

        nodes = graph.get_nodes()
        k = {}

        for i, v in enumerate( nodes ):
            k[v] = i

        # Adjacent matrix
        for i in xrange(n*n):
            fw.doubleArray_setitem(m_adj, i, 0)
        for e in graph.edges:
            fw.doubleArray_setitem(m_adj, k[e[0]]*n+k[e[1]],
                    graph.edges[e].weight)

        fw.floydwarshall(n, m_adj, dist, pred)

        self.dist = {}
        self.pred = {}

        for i in xrange(n*n):
            u = nodes[i/n]
            v = nodes[i%n]
            self.dist[(u,v)] = fw.doubleArray_getitem(dist, i)
            p = fw.intArray_getitem(pred, i)
            if p > -1:
                self.pred[(u,v)] = nodes[p]
            else:
                self.pred[(u,v)] = None

    def get_min_path(self, i, j):
        """ Get the minimum path between nodes i and j """
        p = self.__getpath(i, j)
        if p is None:
            return []
        else:
            return [i, ] + p + [j, ]

    def __getpath(self, i, j):
        try:
            if self.pred[(i, j)] is None:
                return None
            elif self.pred[(i, j)] == i:
                return []
            else:
                k = self.pred[(i, j)]
                return self.__getpath(i, k) + [k, ] + self.__getpath(k, j)
        except KeyError:
            return None

class Helper(object):
    """ A class that implement some methods used by other classes """

    @staticmethod
    def get_path_cost(graph, path):
        return reduce(lambda a, b: a+b, [e.weight for e in [graph.get_edge(u,
            path[i+1]) for i, u in enumerate(path[:-1])]])

    @staticmethod
    def make_tree_from_kruskal(graph, terminals):
        st = Graph.SteinerTree()
        st.terminals = {}.fromkeys(terminals)
        for e in graph.get_mst_kruskal():
            st.add_edge(e)

        return st

class HAlgorithm(object):
    """
    This algorithm is used to find a Steiner tree of a given graph. Its
    approximation is Dh/Dmin <= 2 * (1 - 1/l), where l is the number of leaves
    in the minimal Steiner tree.

    Input: an undirected weighted graph G=(V, E, d), a list of terminal nodes
    S conteined or equal to V and a FloydWarshall instance with all the minimum
    path on the graph.

    Output: a SteinerTree object for G and S
    """

    def __init__(self, graph, terminals, floydwarshall):
        self.graph = graph
        self.terminals = terminals
        self.min_path = floydwarshall.get_min_path

    def get_steiner_tree(self):
        # Create the complete graph with terminal nodes
        complete = self.__complete_terminal_graph()
        # Get a graph changing the edges of the complete graph by minimum paths
        subst = self.__subst_shortest_paths(complete)
        del complete
        # Get the minimum spanning tree
        mst = Helper.make_tree_from_kruskal(subst, self.terminals)
        del subst
        mst.del_useless_edges()

        return mst

    def __complete_terminal_graph(self):
        g = Graph.Graph()
        for i in self.terminals:
            for j in [j for j in self.terminals if j != i]:
                cost = Helper.get_path_cost(self.graph, self.min_path(i, j))
                g.add_edge(Graph.Edge(i, j, cost))
        return g

    def __subst_shortest_paths(self, g):
        tree = Graph.Tree()
        for e in g.get_mst_kruskal():
            path = self.min_path(e.u, e.v)
            for i, u in enumerate(path[:-1]):
                edge = self.graph.get_edge(u, path[i+1])
                tree.add_edge(edge)
        return tree

class Neighborhood(object):
    random.seed()

    @staticmethod
    def get(graph, tree, fw):
        """
        Given a Graph, a SteinerTree and FloydWarshall, returns a neighborhood
        for the graph.

        What it does:
            * Remove an arbitrary edge 'e' of the tree T
            * Replace that edge by a minimum path between the two left subtreesof T - e
            * Remove unnecessary nodes and edges such all non terminal nodes
            * have degree at least two
        """

        t = tree.copy()
        edge = random.choice(t.get_edges())
        t.del_edge(edge)
        # Add the nodes just in case some of them was deleted because it was
        # isolated
        t.add_node(edge.u)
        t.add_node(edge.v)

        # Find the minimum path that connects the two subtress
        cost_min = t.get_cost()
        path_min = None
        for u in Neighborhood._get_subtree_from_root(t, edge.u):
            for v in Neighborhood._get_subtree_from_root(t, edge.v):
                if u == edge.u and v == edge.v:
                    continue
                path = fw.get_min_path(u, v)
                cost = Helper.get_path_cost(graph, path)
                if cost < cost_min:
                    path_min = path
                    cost_min = cost

        # Add the path in the tree
        for i, u in enumerate(path_min[:-1]):
            e = graph.get_edge(u, path_min[i+1])
            t.add_edge(e)

        # Remove all unnecessary nodes and edges
        st = Helper.make_tree_from_kruskal(t, t.terminals)
        st.del_useless_edges()

        return st

    @staticmethod
    def _get_subtree_from_root(tree, root):
        dic = {}
        Neighborhood._get(tree, root, dic)
        return dic.keys()

    @staticmethod
    def _get(tree, root, dic):
        if root is None:
            return
        dic[root] = 1
        for i in tree[root]:
            if not i in dic or dic[i] != 1:
                Neighborhood._get(tree, i, dic)

class GraphGen(object):
    """ Generate a complete undirected graph """
    _MAX_NODES = 1000
    _MAX_WEIGHT = 10000
    random.seed()

    @staticmethod
    def generate(nodes_number=random.randint(5, _MAX_NODES), steiner=False):
        if nodes_number > GraphGen._MAX_NODES:
            raise Graph.GraphError('Unsupported number of nodes %d' %nodes_number)
            return None
        else:
            graph = Graph.Graph()
            terminals = []

            # Create ndoes from 1 to nodes_number
            for i in xrange(1, nodes_number + 1):
                node = Graph.Node(i)
                graph.add_node(node)

                # Link with other nodes
                for j in graph:
                    if node != j:
                        w = random.randint(1, GraphGen._MAX_WEIGHT)
                        graph.add_edge(Graph.Edge(node, j, w))
            if steiner is True:
                return (graph, random.sample(graph.get_nodes(),
                        random.randint(2, len(graph)-1)))
            else:
                return graph
