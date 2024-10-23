class Graph:
    def __init__(self, n=0, m=0):
        '''Constructs a graph with n vertices numbered from 0 to n and no edges
        '''
        self.__n = n
        self.__m = m
        self.__in_edges = {}
        self.__out_edges = {}
        self.__cost = {}
        for i in range(n):
            self.__in_edges[i] = set()
            self.__out_edges[i] = set()

    def add_vertex(self, x):
        '''Inserts the vertex into the graph.py.
        Precondition: x is not already a vertex.
        '''
        self.__in_edges[x] = set()
        self.__out_edges[x] = set()
        self.__n += 1

    def remove_vertex(self, x):
        for vertex in self.parse_nout(x):
            self.remove_edge(x, vertex)
            self.__m -= 1
        for vertex in self.parse_nin(x):
            self.remove_edge(vertex, x)
            self.__m -= 1
        self.__in_edges.pop(x)
        self.__out_edges.pop(x)
        self.__n -= 1

    def add_edge(self, x, y, c):
        '''Adds an edge from vertex x to vertex y and returns True.
            If the edge already exists, nothing happens and the function returns False.
            Precondition: x and y are valid vertices of the graph.py.
        '''
        if y in self.__out_edges[x]:
            return False
        self.__out_edges[x].add(y)
        self.__in_edges[y].add(x)
        self.__cost[(x, y)] = c
        self.__m += 1
        return True

    def remove_edge(self, x, y):
        if y not in self.__out_edges[x]:
            return False
        self.__out_edges[x].remove(y)
        self.__in_edges[y].remove(x)
        self.__cost.pop((x, y))
        self.__m -= 1

    def is_edge(self, x, y):
        '''Returns True if there is an edge from x to y in the graph.py, and False otherwise.
            Precondition: x and y are valid vertices of the graph.py.
        '''
        return y in self.__out_edges[x]

    def parse_nout(self, x):
        '''Returns something iterable that contains all the outbound neighbors of vertex x
            Precondition: x is a valid vertex of the graph.py.
        '''
        return set(self.__out_edges[x])

    def parse_nin(self, x):
        '''Returns something iterable that contains all the inbound neighbors of vertex x
            Precondition: x is a valid vertex of the graph.py.
        '''
        return set(self.__in_edges[x])

    def parse_vertices(self):
        '''Return something iterable that contains all the vertices of the graph.py
        '''
        return set(self.__in_edges.keys())

    def get_in_degree(self, x):
        return len(self.__in_edges[x])

    def get_out_degree(self, x):
        return len(self.__out_edges[x])

    def get_cost(self, x, y):
        return self.__cost[(x, y)]

    def set_cost(self, x, y, c):
        self.__cost[(x, y)] = c

    def is_vertex(self, x):
        return x in self.__out_edges.keys() or x in self.__in_edges.keys()

    def get_number_of_vertices(self):
        return self.__n

    def get_number_of_edges(self):
        return self.__m

    def get_in_edges(self):
        return self.__in_edges

    def get_out_edges(self):
        return self.__out_edges
