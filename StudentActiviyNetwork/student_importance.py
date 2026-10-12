import pandas as pd

# Load student metrics and community data
metrics = pd.read_csv("results/student_metrics.csv")
communities = pd.read_csv("results/communities.csv")

# Combine the two datasets
data = metrics.merge(
    communities[["student_id", "community"]],
    on="student_id"
)

# -----------------------------
# TOP CONNECTED STUDENTS
# -----------------------------

print("\nTOP 10 HIGHLY CONNECTED STUDENTS")
print("----------------------------------")

top_degree = data.sort_values(
    "degree",
    ascending=False
).head(10)

print(
    top_degree[
        ["student_id", "department", "degree", "community"]
    ].to_string(index=False)
)

# -----------------------------
# TOP BRIDGE STUDENTS
# -----------------------------

print("\nTOP 10 BRIDGE STUDENTS")
print("-----------------------")

top_betweenness = data.sort_values(
    "betweenness_centrality",
    ascending=False
).head(10)

print(
    top_betweenness[
        ["student_id", "department",
         "betweenness_centrality", "community"]
    ].to_string(index=False)
)

# -----------------------------
# TOP STUDENTS BY CLOSENESS
# -----------------------------

print("\nTOP 10 STUDENTS BY CLOSENESS")
print("-----------------------------")

top_closeness = data.sort_values(
    "closeness_centrality",
    ascending=False
).head(10)

print(
    top_closeness[
        ["student_id", "department",
         "closeness_centrality", "community"]
    ].to_string(index=False)
)

# -----------------------------
# LOW-CONNECTED STUDENTS
# -----------------------------

print("\nLOW-CONNECTED STUDENTS")
print("----------------------")

low_degree = data.sort_values(
    "degree",
    ascending=True
).head(10)

print(
    low_degree[
        ["student_id", "department",
         "degree", "community"]
    ].to_string(index=False)
)

# -----------------------------
# Save results
# -----------------------------

top_degree.to_csv(
    "results/top_connected_students.csv",
    index=False
)

top_betweenness.to_csv(
    "results/top_bridge_students.csv",
    index=False
)

low_degree.to_csv(
    "results/low_connected_students.csv",
    index=False
)

print("\nResults saved successfully!")