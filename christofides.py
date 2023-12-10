import networkx as nx
import time
from memory_profiler import memory_usage

def Christofides(graph):

    app_solution, execution_time = Christofides_(graph)

    mem_usage = memory_usage((Christofides_, (graph,)))
    max_memory_usage = max(mem_usage)

    return app_solution, execution_time, max_memory_usage

def pareamento_minimo(grafo, arvore_minima):
    nao_pares = [v for v, grau in nx.degree(arvore_minima) if grau % 2 == 1]
    pareando = nx.min_weight_matching(nx.subgraph(grafo, nao_pares))
    return pareando

def grafo_multigrafo(grafo, arvore_minima, pareamento):
    multigrafo = nx.MultiGraph(arvore_minima)
    for v1, v2 in pareamento:
        multigrafo.add_edge(v1, v2, weight=grafo[v1][v2]['weight'])
    return multigrafo

def menor_caminho(grafo):
    menor_caminho = [x[0] for x in nx.eulerian_circuit(grafo, 1)]
    return list(dict.fromkeys(menor_caminho)) + [menor_caminho[0]]

def Christofides_(grafo):
    start_time = time.time()
    arvore_minima = nx.minimum_spanning_tree(grafo)
    pareamento = pareamento_minimo(grafo, arvore_minima)
    multigrafo = grafo_multigrafo(grafo, arvore_minima, pareamento)
    caminho = menor_caminho(multigrafo)
    
    peso_solucao = 0
    for i in range(len(caminho) - 1):
        peso_solucao += grafo[caminho[i]][caminho[i + 1]]['weight']
    execution_time = time.time() - start_time

    return peso_solucao, execution_time