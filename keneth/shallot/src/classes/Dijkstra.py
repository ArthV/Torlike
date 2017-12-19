
class Graph:
    # A function to find the  node with minimum dist value, from the set of vertices still in queue
    def minDistance(self, dist, queue):
        # IInitialize min value and min_index as -1
        minimum = float("Inf")
        min_index = -1
        # Find from the dist array, min value which is till in queue
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index
# print shortst path from src

    def printPath(self, parent, j):
        if parent[j] == -1:  # define base:If j is source
            jj = j + 1
            print("R%d" % jj),
            return
        self.printPath(parent, parent[j])
        jj = j + 1
        print("R%d" % jj),

    def printSolution(self, dist, parent):
        src = 0
        print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)):
            print("\nR%d --> R%d \t\t%d \t\t\t\t\t" %
                  (src + 1, i + 1, dist[i])),
            self.printPath(parent, i)

    '''This function implements Dijkstra's single source shortest path
        algorithm for a graph represented using adjacency matrix
        representation'''

    def dijkstra(self, graph, src):

        row = len(graph)
        col = len(graph[0])
        dist = [float("Inf")] * row  # initializan

        # store shortest path tree
        parent = [-1] * row

        dist[src] = 0  # Distance of source from itself is always 0

        # Add all vertices in queue
        queue = []
        for i in range(row):
            queue.append(i)

        # shortest path for all vertices
        while queue:

            # min dis vertex from vertices
            u = self.minDistance(dist, queue)

            queue.remove(u)

            # Update dis value
            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

        self.printSolution(dist, parent)

    @staticmethod
    def random_dijkstra(self, topology):
        self.generate_graph(topology)

    def generate_graph(self, topology):
        """ Genereate the graph to apply dijskstra """
        relays = dict()
        for key, value in topology.items():
            if 'relay' in value['name']:
                relays.update(value)
        size = len(relays)
        Graph = [[0 for x in range(size)] for y in range(size)]


g = Graph()
store = []
from random import randint
for i in range(11):
    # assigning randomized cost between 1 and 16 to each link
    store.append(randint(1, 16))
    # print([store])


c1 = store[0]  # C1 to C11 are the costs
c2 = store[1]
c3 = store[2]
c4 = store[3]
c5 = store[4]
c6 = store[5]
c7 = store[6]
c8 = store[7]
c9 = store[8]
c10 = store[9]
c11 = store[10]
graph = [
    [0, c1, 0, 0, 0, 0, 0, 0],  # alice
    [c1, 0, 0, 0, c2, c3, c4, 0],  # R2
    [0, 0, 0, c5, c6, 0, c7, 0],  # R3
    [0, 0, c5, 0, c8, c9, 0, c10],  # R4
    [0, c2, c6, c8, 0, 0, c11, 0],  # R5
    [0, c3, 0, c9, 0, 0, 0, 0],  # R6
    [0, c4, c7, 0, c11, 0, 0, 0],  # R7
    [0, 0, 0, c10, 0, 0, 0, 0]  # Bob
]


# Print the solution
g.dijkstra(graph, 0)
