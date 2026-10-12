import pandas as pd
import networkx as nx
from itertools import combinations

# Load data
students = pd.read_csv("Data/students.csv")
participation = pd.read_csv("Data/participation.csv")

# Create student graph
G = nx.Graph()

# Add all students as nodes
for _, student in students.iterrows():
    G.add_node(
        student["student_id"],
        department=student["department"],
        year=student["year"]
    )

# Group students by activity
activity_groups = participation.groupby("activity_id")

# Connect students who share an activity
for activity, group in activity_groups:
    student_list = group["student_id"].tolist()

    for student1, student2 in combinations(student_list, 2):

        if G.has_edge(student1, student2):
            G[student1][student2]["weight"] += 1
        else:
            G.add_edge(student1, student2, weight=1)

# Display information
print("STUDENT–STUDENT NETWORK")
print("-----------------------")
print("Number of students:", G.number_of_nodes())
print("Number of connections:", G.number_of_edges())

# Average degree
average_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()

print("Average degree:", round(average_degree, 2))

# Strongest connections
strongest = sorted(
    G.edges(data=True),
    key=lambda x: x[2]["weight"],
    reverse=True
)

print("\nTop 10 strongest student connections:")

for student1, student2, data in strongest[:10]:
    print(
        student1,
        "<->",
        student2,
        " shared activities:",
        data["weight"]
    )
    # Create analysis graph using only strong connections
# Students must share at least 3 activities
analysis_graph = nx.Graph()

# Add all students
analysis_graph.add_nodes_from(G.nodes(data=True))

# Add only strong connections
for student1, student2, data in G.edges(data=True):
    if data["weight"] >= 3:
        analysis_graph.add_edge(
            student1,
            student2,
            weight=data["weight"]
        )

print("\nANALYSIS NETWORK")
print("----------------")
print("Students:", analysis_graph.number_of_nodes())
print("Connections:", analysis_graph.number_of_edges())

average_degree = (
    sum(dict(analysis_graph.degree()).values())
    / analysis_graph.number_of_nodes()
)

print("Average degree:", round(average_degree, 2))