from utils import DistinctHeap, Queue, Graph, timer
from algorithms.base import General_Graph_Search, depth_limited_search


@timer
def depthFirstSearch(graph: Graph, start: int, end: int):
    graph.set_problem(start=start, end=end, heuristic=False)  # initialize the search problem
    stack = list()  # initialize a LIFO stack as the frontier
    return General_Graph_Search(graph, frontiers=stack)


@timer
def breadthFirstSearch(graph: Graph, start: int, end: int):
    graph.set_problem(start=start, end=end, heuristic=False)  # initialize the search problem
    queue = Queue()  # initialize a FIFO queue as the frontier
    return General_Graph_Search(graph, frontiers=queue)


@timer
def uniformCostSearch(graph: Graph, start: int, end: int):
    graph.set_problem(start=start, end=end, heuristic=False)
    '''
    frontier for uniformCostSearch is a distinct priority queue,
    where key is item[0][-1]: the last node in a path to make sure that
    there is only one optimal path to reach that node,
    if two paths has the same destiny, optimal one will be preserved
    different paths in the queue are sorted by it's total cost(item[1])
    '''
    priority_queue = DistinctHeap(key=lambda item: item[0][-1], cmp=lambda item: item[1])
    return General_Graph_Search(graph, frontiers=priority_queue)


@timer
def greedySearch(graph: Graph, start: int, end: int):
    graph.set_problem(start=start, end=end, heuristic=True)
    '''
    frontier for greedySearch is a distinct priority queue,
    where key is item[0][-1]: the last node in a path to make sure that
                              there is only one optimal path to reach that node,

    and different paths in the queue are sorted by it's heuristic value (item[2])
    '''
    priority_queue = DistinctHeap(key=lambda item: item[0][-1], cmp=lambda item: item[2])
    return General_Graph_Search(graph, frontiers=priority_queue)


@timer
def aStarSearch(graph: Graph, start: int, end: int):
    graph.set_problem(start=start, end=end, heuristic=True)
    '''
    frontier for aStarSearch is a distinct priority queue,
    where key is item[0][-1]: the last node in a path to make sure that
                              there is only one optimal path to reach that node,

    and different paths in the queue are sorted by sum of total cost and heuristic value
    '''
    priority_queue = DistinctHeap(key=lambda item: item[0][-1], cmp=lambda item: item[1] + item[2])
    return General_Graph_Search(graph, frontiers=priority_queue)


@timer
def iterative_deepening_search(graph: Graph, start: int, end: int):
    graph.set_problem(start=start, end=end)
    stack = list()
    for iters in range(int(1e9)):
        res = depth_limited_search(graph, stack, iters)
        if res.prune is False:
            return res
        iters += 1


DFS = depthFirstSearch
BFS = breadthFirstSearch
Uniform = uniformCostSearch
Greedy = greedySearch
AStar = aStarSearch
IDS = iterative_deepening_search

if __name__ == '__main__':
    graph = Graph()
    algorithms = [DFS, BFS, Uniform, Greedy, AStar]
    res_lst = [func(graph, 0, 1894) for func in algorithms]

    for res in res_lst:
        print(res)
        print(f'length of path: {len(res.path)}, total cost: {res.cost}, '
              f'memo cost: {res.expanded_nodes}, time cost: {res.time}')
