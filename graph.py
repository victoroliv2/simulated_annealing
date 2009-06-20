import graph_utils

class GraphError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Node(object):
    """ Represents a node that has a label. This label can be any object """

    def __init__(self, label):
        self.label = label

    def __str__(self):
        return "".join(["<node ", str(self.label), ">"])

class Edge(object):
    """ Represents a weighted edge that connects two Node objects """

    def __init__(self, u, v, weight=0):
        self.u = u
        self.v = v
        self.weight = weight

    def __str__(self):
        return "".join(["<edge ", str(self.u), ", ", str(self.v),
            str(self.weight), ">"])

class Graph(object):
    """ Represent undirected graphs built of nodes and edges """

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def __str__(self):
        slist = [str(i) for i in self.get_edges()]
        slist.append(" >")
        return '<graph ' + "".join(slist)

    def __iter__(self):
        """ Iterate over the nodes: 'for i in Graph' """
        return self.nodes.iterkeys()

    def __len__(self):
        """ The number of nodes """
        return len(self.nodes)

    def __contains__(self, node):
        """ Return whether the graph contains the node or not """
        try:
            return node in self.nodes
        except TypeError:
            return False

    def __getitem__(self, node):
        """ Return the node's neighbors """
        try:
            return self.nodes[node]
        except KeyError:
            return []

    def copy (self):
        """ Return a shallow copy of the graph """
        g = Graph()
        map(lambda e: g.add_edge(e), self.get_nodes())
        return g

    def get_nodes(self):
        """ Give the graph nodes list """
        return self.nodes.keys()

    def neighbors(self, node):
        """ Equal to Graph[node], here just for convenience """
        return self[node]

    def get_edges(self):
        """ Give the graph edges. Because the graph is undirected, (u, v) is
        the same as (v, u) and is returned once """
        return {}.fromkeys(self.edges.values()).keys()

    def get_node(self, label):
        """ Return the node given its label """
        try:
            return [i for i in self.nodes if i.label == label][0]
        except IndexError:
            return None

    def get_edge(self, u, v):
        """ Return the edge given the nodes it connects """
        try:
            return self.edges[(u, v)]
        except KeyError:
            return None

    def has_edge(self, u, v):
        """ Return whether an edge between u and v exists or not """
        return self.edges.has_key((u, v)) and self.edges.has_key((v, u))

    def add_node(self, node):
        """ Add the node """
        if node not in self.nodes:
            self.nodes[node] = []
            return True
        return False

    def add_edge(self, edge):
        """ Add the edges to the graph. If the edge is connected to some node
        that doesnt belong to the graph, the node is added also """
        try:
            if edge.u in self.nodes[edge.v] and edge.v in self.nodes[edge.u] \
            and edge == self.edges[(edge.u, edge.v)] and \
            edge == self.edges[(edge.v, edge.u)]:
                return False
            elif edge.u in self.nodes[edge.v] and edge.v not in \
            self.nodes[edge.u]:
                return False
            elif edge.u not in self.nodes[edge.v] and edge.v in \
            self.nodes[edge.u]:
                return False
        except KeyError:
            pass
        self.add_node(edge.u)
        self.add_node(edge.v)
        self.nodes[edge.u].append(edge.v)
        self.nodes[edge.v].append(edge.u)
        self.edges[(edge.u, edge.v)] = edge
        self.edges[(edge.v, edge.u)] = edge
        return True

    def del_node(self, node):
        # Delete all edges adjacent to this node
        try:
            neighbors = self[node]
        except KeyError:
            raise GraphError('Node %s not in graph' %str(node))
        map(lambda v: self.del_edge(self.get_edge(v, node)), neighbors)
        try:
            self.nodes.pop(node)
        except KeyError:
            pass

    def del_edge(self, edge):
        """ Remove the given edge. Notice this method doesnt handle graph
        disconection and all nodes with no incident edge will be removed """
        try:
            if edge.v not in self[edge.u] or edge.u not in self[edge.v]:
                raise GraphError('Bad edge %s on the graph' %str(edge))
            self.edges.pop((edge.u, edge.v))
            self.edges.pop((edge.v, edge.u))
            self[edge.u].remove(edge.v)
            self[edge.v].remove(edge.u)
            # Delete isolated nodes
            if self.order(edge.u) == 0:
                self.nodes.pop(edge.u)
            if self.order(edge.v) == 0:
                self.nodes.pop(edge.v)
        except KeyError:
            raise GraphError('Edge not found')
        except:
            raise

    def order(self, node):
        """ Give the node order """
        return len(self[node])

    def get_mst_kruskal(self):
        """ Give the edges of the minimum spanning tree using Kruskal algorithm
        """
        edges = self.get_edges()
        edges.sort(key=lambda e: e.weight)
        forest = graph_utils.UnionFind()
        for e in edges:
            if forest[e.u] != forest[e.v]:
                yield e
                forest.union(e.u, e.v)
        del forest

    @staticmethod
    def read(filename):
        """ Read a graph object from a file """
        import pickle

        f = open(filename, 'r')
        obj = pickle.load(f)
        if type(obj) is Graph:
            return obj
        else:
            raise GraphError('wtf r u trying to read?')
        f.close()
        return obj

    def write(self, filename):
        """ Write a graph to a file """
        import pickle

        f = open(filename, 'w')
        pickle.dump(self, f)
        f.close()

    def draw(self, imagefile):
        import gvgen
        import pygraphviz as pgv

        G = gvgen.GvGen()
        n = {}
        for node in self:
            n[node] = G.newItem('%s' %node.label)
        for e in self.edges:
            edge = self.edges[e]
            ge = G.newLink(n[edge.u], n[edge.v])
            G.propertyAppend(ge, "arrowhead", "none")

        import StringIO

        fd = StringIO.StringIO()
        G.dot(fd)
        dottext = fd.getvalue()

        G = pgv.AGraph()
        G.from_string(dottext)
        G.layout()
        G.draw(imagefile)

class Tree(Graph):

    def __init__(self):
        Graph.__init__(self)

    def del_node(self, node):
        """ Just leaves can be deleted """
        if self.is_leaf(node) or self.order(node) == 0:
            Graph.del_node(self, node)
        else:
            raise GraphError('Cant delete %s. Just allowed deletion of leaves.'
                    %str(node))

    def get_leaves(self):
        """ Return a iterator with all tree's leaves """
        for node in self:
            if self.is_leaf(node):
                yield node

    def is_leaf(self, node):
        return self.order(node) == 1

class SteinerTree(Tree):
    """ The SteinerTree class is a tree that must have some nodes (the
    terminal nodes) and its total cost is supposed to be minimum.

    All non terminal nodes belonging to the tree are called steiner nodes """

    def __init__(self):
        Tree.__init__(self)
        self.terminals = {}
        self.cost = 0

    def copy(self):
        st = SteinerTree()
        map(lambda e: st.add_edge(e), self.get_edges())
        map(lambda t: st.add_terminal(t), self.terminals)
        st.cost = self.cost
        return st

    def get_terminals(self):
        return self.terminals.keys()

    def add_terminal(self, node):
        if node not in self:
            self.add_node(node)
        self.terminals[node] = None

    def add_edge(self, e):
        if Tree.add_edge(self, e):
            self.cost += e.weight
            return True
        return False

    def del_terminal(self, node):
        try:
            self.terminals.pop(node)
        except KeyError:
            raise GraphError('%s is not a terminal node' %str(node))

    def del_node(self, node):
        if node not in self.terminals:
            Tree.del_node(self, node)
        else:
            raise GraphError('Deletion of terminal %s doesnt allowed'
                    %str(node))

    def del_edge(self, edge):
        Tree.del_edge(self, edge)
        self.cost -= edge.weight

    def del_useless_edges(self):
        nodes = self.get_nodes()
        nodes.sort(key=lambda o: len(self[o]))
        for node in nodes:
            if self.is_leaf(node) and node not in self.terminals:
                self.del_node(node)

    def is_terminal(self, node):
        return node in self.terminals

    def get_cost(self):
        return self.cost

    def draw(self, imagefile):
        import gvgen
        import pygraphviz as pgv

        G = gvgen.GvGen()
        G.styleAppend("terminal", "color", "red")
        G.styleAppend("terminal", "style", "filled")
        G.styleAppend("terminal", "fontcolor", "white")

        n = {}
        for node in self:
            n[node] = G.newItem('%s' %str(node.label))
            if node in self.terminals:
                G.styleApply("terminal", n[node])
        for e in self.edges:
            edge = self.edges[e]
            ge = G.newLink(n[edge.u], n[edge.v])
            G.propertyAppend(ge, "arrowhead", "none")

        import StringIO

        fd = StringIO.StringIO()
        G.dot(fd)
        dottext = fd.getvalue()

        G = pgv.AGraph()
        G.from_string(dottext)
        G.layout()
        G.draw(imagefile)
