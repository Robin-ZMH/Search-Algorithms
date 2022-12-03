import pandas as pd
import numpy as np
import os


class Graph:
    NODES_FILE = "CaliforniaRoadNetwork_Nodes.csv"
    EDGES_FILE = "CaliforniaRoadNetwork_Edges.csv"

    def __init__(self):
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        nodes_file = os.path.join(file_dir, self.NODES_FILE)
        edges_file = os.path.join(file_dir, self.EDGES_FILE)

        nodes_df = pd.read_csv(nodes_file)
        edges_df = pd.read_csv(edges_file)

        self.__edges = edges_df.values
        self.__graph = self.__graph_maker()

        # store the position of every node
        self.__nodes = {int(node_id): (longitude, latitude)
                        for node_id, longitude, latitude in nodes_df.values}

        self.__start = None
        self.__end = None
        self.__heuristic = False

    def __graph_maker(self):
        """
        convert all edges into a graph data structure,
        where the graph is a dict like this:
        {node: all successors of the node}
        """
        graph = dict()
        for _, start, end in self.__edges:
            # since edges are bi-directional,
            # both of start and end should be the key of the dict
            graph[start] = graph.get(start, [])
            graph[start].append(end)
            graph[end] = graph.get(end, [])
            graph[end].append(start)
        return graph

    def __euclidean_distance(self, node1, node2):
        pos1, pos2 = self.position(node1), self.position(node2)  # get positions of two nodes
        vector = [x1 - x2 for x1, x2 in zip(pos1, pos2)]  # compute the vector
        vector = np.array(vector)
        return np.linalg.norm(vector)

    @property
    def nodes(self):
        return list(self.__nodes.keys())

    def successors(self, node):
        return self.__graph[node]

    def position(self, node):
        # nodes = {1, (20.1, 0.0)}
        return self.__nodes[node]

    # initialize the search problem
    def set_problem(self, start, end, heuristic=False):
        self.__start = start
        self.__end = end
        self.__heuristic = heuristic

    def get_initial_state(self):
        return self.__start

    def is_goal(self, node):
        return node == self.__end

    def distance(self, *nodes):
        """
        compute the total distance of the path(list of nodes)
        """
        # make both (n1, n2...) and ([n1, n2...]) are correct
        if len(nodes) == 1 and isinstance(nodes[0], list):
            nodes = nodes[0]

        # 错位拼接:[1, 2, 3]
        # zip([0, 1, ... ,n-1], [1, 2, ... , n]) -> [(0, 1), (1, 2), ... , (n-1, n)]
        distances = [self.__euclidean_distance(node1, node2)
                     for node1, node2 in zip(nodes[:-1], nodes[1:])]

        res = sum(distances)
        return res

    def heuristic(self, node):
        if self.__heuristic is False:
            return 0
        # best heuristic for this problem we have explored out so far
        # is euclidean distance between the current node and the end
        return self.distance(node, self.__end)

    @staticmethod
    def has_circle(path):
        # check if there is a circle in the path by check if there are repeated nodes,
        # just compare the length of set(path) with original path.
        # Because if there are repeated nodes in a path,
        # then the repeated nodes must have run a circle to get back
        return len(set(path)) < len(path)


if __name__ == '__main__':
    import random
    graph = Graph()
    points = [random.choice(graph.nodes) for _ in range(50)]
    print(graph.distance(points))
    print(graph.nodes)
    print('=' * 50)
    graph.set_problem(0, 21040, True)
    print(graph.heuristic(1894))
