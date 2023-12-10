import networkx as nx
import time
from memory_profiler import memory_usage

def TwiceAroundtheTree(graph):

    mem_usage = memory_usage((TwiceAroundtheTree_, (graph,)))
    max_memory_usage = max(mem_usage)

    app_solution, execution_time = TwiceAroundtheTree_(graph)

    return app_solution, execution_time, max_memory_usage

def TwiceAroundtheTree_(graph):
    start_time = time.time()

    min_spanning = nx.minimum_spanning_tree(graph)
    path = list(nx.dfs_preorder_nodes(min_spanning, 1))
    path.append(path[0])

    app_solution = 0
    for i in range(len(path) - 1):
        app_solution += graph[path[i]][path[i + 1]]['weight']

    execution_time = time.time() - start_time
    return app_solution, execution_time



