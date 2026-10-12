import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
students = pd.read_csv("Data/students.csv")
activities = pd.read_csv("Data/activities.csv")
participation = pd.read_csv("Data/participation.csv")

# Create graph
G = nx.Graph()

# Add student nodes
for _, student in students.iterrows():
    G.add_node(
        student["student_id"],
        type="student",
        department=student["department"],
        year=student["year"]
    )

# Add activity nodes
for _, activity in activities.iterrows():
    G.add_node(
        activity["activity_id"],
        type="activity",
        name=activity["activity_name"],
        activity_type=activity["activity_type"]
    )

# Add participation edges
for _, row in participation.iterrows():
    G.add_edge(row["student_id"], row["activity_id"])

# Display graph information
print("GRAPH CREATED SUCCESSFULLY")
print("---------------------------")
print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())

print("Student nodes:", len(students))
print("Activity nodes:", len(activities))

plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G, seed=42)

student_nodes = [
    node for node, data in G.nodes(data=True)
    if data["type"] == "student"
]

activity_nodes = [
    node for node, data in G.nodes(data=True)
    if data["type"] == "activity"
]

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=student_nodes,
    node_size=40
)

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=activity_nodes,
    node_size=150
)

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.2
)

plt.title("Student–Activity Network")
plt.axis("off")
plt.show()