from utils import Graph, Result, Container


def General_Graph_Search(graph: Graph, frontiers: Container) -> Result:
    """
    General graph search algorithm that can be transformed to [DFS, BFS, Uniform, AStar, Greedy]
    by utilizing the polymorphism of the Container object

    :param graph: A Graph object to collect all information about the search problem

    :param frontiers: A Container object to store the tuples: (path, cost, heuristic_value),
                    container should implement: append, pop and __len__

    :return: If solution exists,return a Result object that stores the
            final path, cost, memory used and time cost of the problem,
            otherwise return an empty Result object(except time consumption)
    """

    start = graph.get_initial_state()
    frontiers.append(([start], 0, graph.heuristic(start)))
    visited = set()  # stores the nodes that have been popped from the frontiers
    expanded = 1  # max number of nodes between frontiers and visited

    while frontiers:
        path, cost, _ = frontiers.pop()
        cur_node = path[-1]

        if graph.is_goal(cur_node):
            return Result(path=path, cost=cost, expanded_nodes=expanded)

        if cur_node in visited:
            continue
        visited.add(cur_node)

        successors = graph.successors(cur_node)
        for next_node in successors:
            if next_node in visited:
                continue

            new_cost = cost + graph.distance(cur_node, next_node)
            new_path = [*path, next_node]  # copy the path and append the next_node into new_path
            new_h_val = graph.heuristic(next_node)

            frontiers.append((new_path, new_cost, new_h_val))
            expanded = max(expanded, len(frontiers), len(visited))

    return Result()


def tree_like_search(graph: Graph, frontiers):
    start = graph.get_initial_state()
    if graph.is_goal(start):
        return Result(path=[start], cost=0, expanded_nodes=0)
    frontiers.append([start, ])
    expanded = 1  # number of the expanded nodes
    while frontiers:
        path = frontiers.pop()
        cur_node = path[-1]

        successors = graph.successors(cur_node)
        for next_node in successors:
            new_path = [*path, next_node]

            if graph.is_goal(next_node):
                cost = graph.distance(new_path)
                return Result(path=new_path, cost=cost, expanded_nodes=expanded)

            if graph.has_circle(new_path):
                continue

            frontiers.append(new_path)
            expanded = max(expanded, len(frontiers))

    return Result()


def depth_limited_search(graph: Graph, frontiers, max_iter) -> Result:
    start = graph.get_initial_state()
    if graph.is_goal(start):
        return Result(path=[start], cost=0, expanded_nodes=0)
    frontiers.append([start, ])
    expanded = 1  # number of the expanded nodes
    res = Result()
    while frontiers:
        path = frontiers.pop()
        cur_node = path[-1]

        if len(path) > max_iter:
            res.prune = True
            continue

        successors = graph.successors(cur_node)
        for next_node in successors:
            new_path = [*path, next_node]

            if graph.is_goal(next_node):
                cost = graph.distance(new_path)
                res = Result(path=new_path, cost=cost, expanded_nodes=expanded)
                return res

            if graph.has_circle(new_path):
                continue

            frontiers.append(new_path)
            expanded = max(expanded, len(frontiers))

    return res
