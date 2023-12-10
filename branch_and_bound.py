import networkx as nx
import time

import numpy as np

def find_two_min_edges(weights):
    min1, min2 = np.inf, np.inf
    for weight in weights:
        if weight < min1:
            min1, min2 = weight, min1
        elif weight < min2:
            min2 = weight
    return min1, min2

def initial_bound(graph):
    bound = 0
    edge_bounds = np.zeros((graph.number_of_nodes(), 2), dtype=object)

    for i in range(1, graph.number_of_nodes() + 1):
        min1, min2 = find_two_min_edges([graph[i][j]['weight'] for j in graph[i]])
        edge_bounds[i - 1] = [min1, min2]
        bound += min1 + min2

    return bound / 2, edge_bounds

def update_bound(graph, solution, edge_bounds, bound):
    changed_edges = np.zeros(graph.number_of_nodes(), dtype=int)
    new_edges = np.array(edge_bounds)
    edge_weight = graph[solution[-2]][solution[-1]]['weight']
    total = bound * 2

    for node in solution[-2:]:
        node_index = node - 1
        if new_edges[node_index][0] != edge_weight:
            total -= new_edges[node_index][changed_edges[node_index]]
            total += edge_weight
            changed_edges[node_index] += 1

    return total / 2, new_edges

def branch_and_bound_tsp(graph):
    start_time = time.time()
    initial_bound_value, initial_edge_bounds = initial_bound(graph)
    root = (initial_bound_value, initial_edge_bounds, 0, [1])
    stack = [root]
    optimal_solution = np.inf
    node_count = 0

    while stack:
        current_node = stack.pop()
        node_count += 1
        level = len(current_node[3])

        if level > graph.number_of_nodes():
            if optimal_solution > current_node[2]:
                optimal_solution = current_node[2]
        else:
            if current_node[0] < optimal_solution:
                if level < graph.number_of_nodes() - 2:
                    for k in range(1, graph.number_of_nodes() + 1):
                        if k in current_node[3]:
                            continue
                        edge_weight = graph[current_node[3][-1]][k]['weight']
                        new_bound, new_edges = update_bound(graph, current_node[3] + [k], current_node[1], current_node[0])
                        if new_bound < optimal_solution:
                            new_node = (new_bound, new_edges, current_node[2] + edge_weight, current_node[3] + [k])
                            stack.append(new_node)
                else:
                    for k in range(1, graph.number_of_nodes() + 1):
                        if k in current_node[3]:
                            continue
                        last_node = next(i for i in range(1, graph.number_of_nodes() + 1) if i not in current_node[3] + [k] and k != i)
                        edge_weight = graph[current_node[3][-1]][k]['weight']
                        next_edge_weight = graph[k][last_node]['weight']
                        last_edge_weight = graph[last_node][1]['weight']
                        cost = current_node[2] + edge_weight + next_edge_weight + last_edge_weight
                        if cost < optimal_solution:
                            new_node = (cost, [], cost, current_node[3] + [k, last_node, 1])
                            stack.append(new_node)
    execution_time = time.time() - start_time

    return optimal_solution, execution_time, 0
