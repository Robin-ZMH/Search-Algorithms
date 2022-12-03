import random
import pandas as pd
from algorithms import DFS, BFS, Uniform, AStar, Greedy, IDS
from utils import Graph, Result

graph = Graph()


def first_quest():
    points = [(0, 1894), (4, 3115), (18, 9186), (25, 15061), (33, 21040)]
    data_frame = [AStar(graph, start, end).data
                  for start, end in points]

    df = pd.DataFrame(data_frame)
    df.to_csv('results/question1.csv')


def second_quest():
    algorithms = [DFS, BFS, Uniform, Greedy, AStar]
    points = [(random.choice(graph.nodes),
               random.choice(graph.nodes))
              for _ in range(1000)]

    data_frame = [func(graph, start, end).data
                  for func in algorithms
                  for start, end in points]

    df = pd.DataFrame(data_frame)
    df.to_csv('results/question2.csv')


def third_quest():
    raise NotImplementedError(
        "We solve the Question3 by visualizing, "
        "and the result can be found at 'results/Q2&3 Figure.twbx' ")


def forth_quest():
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
    df.to_csv('results/question4.csv')


if __name__ == '__main__':
    first_quest()
    second_quest()
    forth_quest()
