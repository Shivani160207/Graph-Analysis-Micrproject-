import pandas as pd
import networkx as nx
from itertools import combinations
import community as community_louvain
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

for _, student in students.iterrows():
    G.add_node(
        student["student_id"],
        department=student["department"],
        year=student["year"]
    )

# Group students by activity
for activity, group in participation.groupby("activity_id"):

    student_list = group["student_id"].tolist()

    for student1, student2 in combinations(student_list, 2):

        if G.has_edge(student1, student2):
            G[student1][student2]["weight"] += 1
        else:
            G.add_edge(student1, student2, weight=1)

# -----------------------------
# 3. Create analysis graph
# -----------------------------
analysis_graph = nx.Graph()

analysis_graph.add_nodes_from(G.nodes(data=True))

for student1, student2, data in G.edges(data=True):

    if data["weight"] >= 3:
        analysis_graph.add_edge(
            student1,
            student2,
            weight=data["weight"]
        )

# -----------------------------
# 4. Community detection
# -----------------------------
communities = community_louvain.best_partition(
    analysis_graph,
    weight="weight",
    random_state=42
)

# -----------------------------
# 5. Add community to students
# -----------------------------
community_results = []

for student, community_id in communities.items():

    community_results.append({
        "student_id": student,
        "department": analysis_graph.nodes[student]["department"],
        "year": analysis_graph.nodes[student]["year"],
        "community": community_id
    })

community_df = pd.DataFrame(community_results)

# -----------------------------
# 6. Save results
# -----------------------------
os.makedirs("results", exist_ok=True)

community_df.to_csv(
    "results/communities.csv",
    index=False
)

# -----------------------------
# 7. Display results
# -----------------------------
print("\nCOMMUNITY DETECTION")
print("-------------------")

number_of_communities = community_df["community"].nunique()

print("Number of communities:", number_of_communities)

print("\nCOMMUNITY SIZES")
print("----------------")

sizes = community_df["community"].value_counts().sort_index()

for community_id, size in sizes.items():
    print(
        "Community",
        community_id,
        ":",
        size,
        "students"
    )

print("\nSTUDENT COMMUNITY ASSIGNMENTS")
print("--------------------------------")

print(
    community_df
    .sort_values(["community", "student_id"])
    .head(20)
    .to_string(index=False)
)

print("\nResults saved to:")
print("results/communities.csv")