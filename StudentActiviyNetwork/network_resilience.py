import pandas as pd
import networkx as nx
from itertools import combinations
import os

# -----------------------------
# 1. Load data
# -----------------------------
students = pd.read_csv("Data/students.csv")
participation = pd.read_csv("Data/participation.csv")

# -----------------------------
# 2. Create full student graph
# -----------------------------
G = nx.Graph()

# Add students
for _, student in students.iterrows():
    G.add_node(
        student["student_id"],
        department=student["department"],
        year=student["year"]
    )

# Create student connections
for activity, group in participation.groupby("activity_id"):

    student_list = group["student_id"].tolist()

    for student1, student2 in combinations(student_list, 2):

        if G.has_edge(student1, student2):
            G[student1][student2]["weight"] += 1
        else:
            G.add_edge(student1, student2, weight=1)

# -----------------------------
# 3. Create analysis network
# -----------------------------
analysis_graph = nx.Graph()

analysis_graph.add_nodes_from(G.nodes(data=True))

for student1, student2, data in G.edges(data=True):

    if data["weight"] >= 3:
        analysis_graph.add_edge(
            student1,
            student2,
            weight=data["weight"],
            distance=1 / data["weight"]
        )

# -----------------------------
# 4. Function to analyze network
# -----------------------------
def analyze_network(graph, name):

    number_of_nodes = graph.number_of_nodes()
    number_of_edges = graph.number_of_edges()

    average_degree = (
        sum(dict(graph.degree()).values())
        / number_of_nodes
    )

    components = list(nx.connected_components(graph))

    number_of_components = len(components)

    largest_component = max(
        len(component)
        for component in components
    )

    return {
        "scenario": name,
        "students": number_of_nodes,
        "connections": number_of_edges,
        "average_degree": round(average_degree, 2),
        "connected_components": number_of_components,
        "largest_component": largest_component
    }


# -----------------------------
# 5. Analyze original network
# -----------------------------
results = []

results.append(
    analyze_network(
        analysis_graph,
        "Original Network"
    )
)

# -----------------------------
# 6. Remove highest-degree student
# -----------------------------
degree = dict(analysis_graph.degree())

highest_degree_student = max(
    degree,
    key=degree.get
)

degree_graph = analysis_graph.copy()

degree_graph.remove_node(
    highest_degree_student
)

results.append(
    analyze_network(
        degree_graph,
        f"After removing {highest_degree_student} (highest degree)"
    )
)

# -----------------------------
# 7. Calculate betweenness
# -----------------------------
betweenness = nx.betweenness_centrality(
    analysis_graph,
    weight="distance"
)

highest_bridge_student = max(
    betweenness,
    key=betweenness.get
)

bridge_graph = analysis_graph.copy()

bridge_graph.remove_node(
    highest_bridge_student
)

results.append(
    analyze_network(
        bridge_graph,
        f"After removing {highest_bridge_student} (highest betweenness)"
    )
)

# -----------------------------
# 8. Display results
# -----------------------------
results_df = pd.DataFrame(results)

print("\nNETWORK RESILIENCE ANALYSIS")
print("===========================")

print(
    results_df.to_string(index=False)
)

print("\nMost connected student removed:")
print(highest_degree_student)

print("\nStrongest bridge student removed:")
print(highest_bridge_student)

# -----------------------------
# 9. Save results
# -----------------------------
os.makedirs("results", exist_ok=True)

results_df.to_csv(
    "results/network_resilience.csv",
    index=False
)

print("\nResults saved to:")
print("results/network_resilience.csv")