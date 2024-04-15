class Vertex:
    #Vertex objects represent stations, with edges representing connections
    def __init__(self, value):
        self.value = value
        self.edges = {}
    
    def add_edge(self, vertex, line, weight, direction):
        self.edges[vertex] = [line, weight, direction]
    


class Graph:
    def __init__(self):
        self.graph_dict = {}
    
    def add_vertex(self, vertex):
        self.graph_dict[vertex.value[0]] = vertex
    
    def add_edge(self, vertex1, vertex2, line, weight):
        #add an edge in each direction (1 = forwards, 2 = backwards)
        self.graph_dict[vertex1.value[0]].add_edge(vertex2.value[0], line, weight, 1)
        self.graph_dict[vertex2.value[0]].add_edge(vertex1.value[0], line, weight, 2)
