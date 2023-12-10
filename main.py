import tsplib95
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from twice_around import TwiceAroundtheTree
from christofides import Christofides
from branch_and_bound import branch_and_bound_tsp
from memory_profiler import memory_usage

def load_file(file_name):
    tsp = f"{file_name}.tsp"
    opt = f"{file_name}.opt.tour"

    graph = tsplib95.load(tsp).get_graph()
    vertices = len(graph.nodes)

    with open(opt, 'r') as f:
        lines = f.readlines()
        opt_graph = [int(line.strip()) for line in lines if line.strip().isdigit()]
    if "teste" in file_name:
        optimal_solution = 0
    else:    
        optimal_solution = 0
        for i in range(len(opt_graph) - 1):
            optimal_solution += graph[opt_graph[i]][opt_graph[i + 1]]['weight']
        optimal_solution += graph[opt_graph[-1]][opt_graph[0]]['weight']
    return graph, vertices, optimal_solution

def find_files_with_extensions(directory):
    tsp_files = []
    files = os.listdir(directory)
    for file in files:
        if file.endswith('.tsp') and f"{os.path.splitext(file)[0]}.opt.tour" in files:
            tsp_files.append(os.path.splitext(file)[0])
    return tsp_files

directory = "graphs"
tsp_files = find_files_with_extensions(directory)
results = []

for file_name in tsp_files:
    try:
        graph, vertices, optimal_solution = load_file(f"{directory}/{file_name}")
        twice_around = (None, None, None)
        christofides = (None, None, None)
        branch_and = (None, None, None)

        if vertices <= 3000:
            twice_around = TwiceAroundtheTree(graph)

        if vertices <= 700:
            christofides = Christofides(graph)

        if vertices <= 15:
            branch_and = branch_and_bound_tsp(graph)
        
        twice_around_proportion = None
        christofides_proportion = None
        branch_proportion = None

        if optimal_solution != 0:
            twice_around_proportion = twice_around[0] / optimal_solution if twice_around[0] is not None else None
            christofides_proportion = christofides[0] / optimal_solution if christofides[0] is not None else None

        else:
            twice_around_proportion = 0
            christofides_proportion = 0

        results.append({
            'File': file_name,
            'Cities': vertices,
            'Optimal Solution': optimal_solution,
            'Twice Around the Tree Solution': twice_around[0],
            'Christofides Solution': christofides[0],
            'Branch-and-bound Solution': branch_and[0],
            'Twice Around Time': twice_around[1],
            'Christofides Time': christofides[1],
            'Branch-and-bound Time': branch_and[1],
            'Twice Around Memory': twice_around[2],
            'Christofides Memory': christofides[2],
            'Branch-and-bound Memory': branch_and[2],
            'Twice Around Proportion': twice_around_proportion,
            'Christofides Proportion': christofides_proportion
        })

        print(f"Done Processing {file_name}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        continue

results_df = pd.DataFrame(results)

plt.figure(figsize=(10, 6))

valid_twice_around = results_df[results_df['Twice Around Time'] != None]
valid_christofides = results_df[results_df['Christofides Time'] != None]
valid_branch = results_df[results_df['Branch-and-bound Time'] != None]

plt.scatter(valid_twice_around['Cities'], valid_twice_around['Twice Around Time'], label='Twice Around the Tree')
plt.scatter(valid_christofides['Cities'], valid_christofides['Christofides Time'], label='Christofides')
plt.scatter(valid_branch['Cities'], valid_branch['Branch-and-bound Time'], label='Branch-and-bound')

plt.xlabel('Number of Cities')
plt.ylabel('Time Taken (seconds)')
plt.title('Number of Cities vs Time Taken for Different Algorithms')
plt.legend()
plt.tight_layout()

output_file_name = 'cities_vs_time.png'
plt.savefig(output_file_name)
plt.show()

plt.figure(figsize=(10, 6))

valid_twice_around = results_df[results_df['Twice Around Memory'] != None]
valid_christofides = results_df[results_df['Christofides Memory'] != None]

plt.scatter(valid_twice_around['Cities'], valid_twice_around['Twice Around Memory'], label='Twice Around the Tree')
plt.scatter(valid_christofides['Cities'], valid_christofides['Christofides Memory'], label='Christofides')

plt.xlabel('Number of Cities')
plt.ylabel('Memory Taken (MB)')
plt.title('Number of Cities vs Memory Taken for Different Algorithms')
plt.legend()
plt.tight_layout()

output_file_name = 'cities_vs_memory.png'
plt.savefig(output_file_name)

plt.figure(figsize=(12, 8))

filtered_results_df = results_df[results_df['Twice Around Proportion'] != 0]

indices = range(len(filtered_results_df))

bar_width = 0.35

plt.bar(indices, filtered_results_df['Twice Around Proportion'], width=bar_width, label='Twice Around the Tree')
plt.bar([i + bar_width for i in indices], filtered_results_df['Christofides Proportion'], width=bar_width, label='Christofides')

plt.xlabel('Files')
plt.ylabel('Proportional Solution')
plt.title('Comparison of Proportional Solutions to the Optimal Solution by Each Algorithm')
plt.xticks([i + bar_width / 2 for i in indices], filtered_results_df['File'], rotation=45, ha='right')
plt.legend()
plt.tight_layout()

try:
    plt.ylim(1, max(filtered_results_df[['Twice Around Proportion', 'Christofides Proportion']].max(axis=1)) + 0.1)
except:
    pass



output_file_name = 'solutions_two_algorithms.png'
plt.savefig(output_file_name)

plt.show()

results_df_filled = results_df.fillna("NA")
results_df.to_csv('results.csv', index=False)

