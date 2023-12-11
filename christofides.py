import networkx as nx
import time
from memory_profiler import memory_usage

def Christofides(graph):
    app_solution, execution_time = Christofides_algorithm(graph)

    mem_usage = memory_usage((Christofides_algorithm, (graph,)))
    max_memory_usage = max(mem_usage)

    return app_solution, execution_time, max_memory_usage

def Christofides_algorithm(graph):
    start_time = time.time()

    non_pairs = [v for v, degree in nx.degree(nx.minimum_spanning_tree(graph)) if degree % 2 == 1]
    matching = nx.min_weight_matching(nx.subgraph(graph, non_pairs))
    new_graph = nx.MultiGraph(nx.minimum_spanning_tree(graph))

    for v1, v2 in matching:
        new_graph.add_edge(v1, v2, weight=graph[v1][v2]['weight'])

    path = [x[0] for x in nx.eulerian_circuit(new_graph, 1)]
    path = list(dict.fromkeys(path)) + [path[0]]

    solution_weight = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
    
    execution_time = time.time() - start_time

    return solution_weight, execution_time
