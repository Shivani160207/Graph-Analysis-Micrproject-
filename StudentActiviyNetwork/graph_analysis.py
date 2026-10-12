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

# Group students by activity
for activity, group in participation.groupby("activity_id"):

    student_list = group["student_id"].tolist()

    # Create student pairs
    for student1, student2 in combinations(student_list, 2):

        if G.has_edge(student1, student2):
            G[student1][student2]["weight"] += 1
        else:
            G.add_edge(student1, student2, weight=1)

# -----------------------------
# 3. Create analysis graph
# -----------------------------
# Only keep connections where
# students share at least 3 activities

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
# 4. Calculate graph metrics
# -----------------------------

degree = dict(analysis_graph.degree())

degree_centrality = nx.degree_centrality(analysis_graph)

betweenness = nx.betweenness_centrality(
    analysis_graph,
    weight="distance"
)

closeness = nx.closeness_centrality(
    analysis_graph,
    distance="distance"
)

# -----------------------------
# 5. Create results table
# -----------------------------

results = []

for student in analysis_graph.nodes():

    results.append({
        "student_id": student,
        "department": analysis_graph.nodes[student]["department"],
        "year": analysis_graph.nodes[student]["year"],
        "degree": degree[student],
        "degree_centrality": round(degree_centrality[student], 4),
        "betweenness_centrality": round(betweenness[student], 4),
        "closeness_centrality": round(closeness[student], 4)
    })

results_df = pd.DataFrame(results)

# Sort by degree
results_df = results_df.sort_values(
    "degree",
    ascending=False
)

# -----------------------------
# 6. Create results folder
# -----------------------------

os.makedirs("results", exist_ok=True)

# Save CSV
results_df.to_csv(
    "results/student_metrics.csv",
    index=False
)

# -----------------------------
# 7. Display results
# -----------------------------

print("\nGRAPH ANALYTICS")
print("----------------")

print("Students:", analysis_graph.number_of_nodes())
print("Connections:", analysis_graph.number_of_edges())

print("\nTOP 10 CONNECTED STUDENTS")
print("--------------------------")

print(
    results_df[
        ["student_id", "degree", "degree_centrality"]
    ].head(10).to_string(index=False)
)

print("\nTOP 10 BRIDGE STUDENTS")
print("----------------------")

bridge_students = results_df.sort_values(
    "betweenness_centrality",
    ascending=False
)

print(
    bridge_students[
        ["student_id", "betweenness_centrality"]
    ].head(10).to_string(index=False)
)

# -----------------------------
# 8. Find isolated students
# -----------------------------

isolated = list(
    nx.isolates(analysis_graph)
)

print("\nISOLATED STUDENTS")
print("-----------------")

if isolated:
    print(isolated)
else:
    print("No completely isolated students.")

print("\nResults saved to:")
print("results/student_metrics.csv")