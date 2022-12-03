import random
import pandas as pd
from algorithms import DFS, BFS, Uniform, AStar, Greedy, IDS
from utils import Graph, Result

graph = Graph()


def graph_search_test():
    algorithms = [DFS, BFS, Uniform, Greedy, AStar]
    points = [(random.choice(graph.nodes),
               random.choice(graph.nodes))
              for _ in range(100)]

    data_frame = [func(graph, start, end).data
                  for func in algorithms
                  for start, end in points]

    df = pd.DataFrame(data_frame)
    df.to_csv('graph_search_test.csv')


def tree_like_search_test():
    """
    tree-like search will trap into a circle and never terminate,
    so, only test iterative_deepening_search for 5 random samples,
    because iterative_deepening_search is just too slow
    """
    points = [(random.choice(graph.nodes), random.choice(graph.nodes))
              for _ in range(5)]

    data_frame = [func(graph, start, end).data
                  for func in [BFS, IDS]
                  for start, end in points]

    df = pd.DataFrame(data_frame)
    avg_time1 = df['memo cost(number of nodes)'][:5].mean()
    avg_time2 = df['memo cost(number of nodes)'][5:].mean()
    print(avg_time1, avg_time2)
    df.to_csv('tree_like_search_test.csv')


if __name__ == '__main__':
    graph_search_test()
    # tree_like_search_test()
