import time
from dataclasses import dataclass
from .container import Container, Queue, DistinctHeap
from .graph import Graph


@dataclass
class Result:
    algorithms: str = None
    start: int = None
    end: int = None
    path: list = None
    cost: float = None
    expanded_nodes: int = None
    time: float = None
    prune: bool = False

    @property
    def data(self):
        columns_to_attrs = {'algorithms': 'algorithms',
                            'start': 'start',
                            'end': 'end',
                            'total distance': 'cost',
                            'time cost(seconds)': 'time',
                            'memo cost(number of nodes)': 'expanded_nodes',
                            'path': 'path'}
        data = {column: getattr(self, attr)
                for column, attr in columns_to_attrs.items()}
        return data


# decorator
def timer(func):
    def wrapper(*args, **kwargs) -> Result:
        # profiling start time
        start = time.time()
        # get result
        res: Result = func(*args, **kwargs)
        # profiling end time
        end = time.time()
        time_cost = end - start

        # complete the Result object
        res.time = time_cost
        res.algorithms = func.__name__
        res.start = kwargs.get('start', None) or args[1]
        res.end = kwargs.get('end', None) or args[2]
        return res

    wrapper.__name__ = func.__name__
    return wrapper
