import pandas as pd

# -----------------------------
# 1. Load data
# -----------------------------
students = pd.read_csv("Data/students.csv")
activities = pd.read_csv("Data/activities.csv")
participation = pd.read_csv("Data/participation.csv")
communities = pd.read_csv("results/communities.csv")
metrics = pd.read_csv("results/student_metrics.csv")

# -----------------------------
# 2. Merge community information
# -----------------------------
student_data = communities.merge(
    metrics,
    on=["student_id", "department", "year"]
)

# -----------------------------
# 3. Community profiling
# -----------------------------

print("\nCOMMUNITY PROFILING")
print("===================")

community_ids = sorted(student_data["community"].unique())

for community_id in community_ids:

    group = student_data[
        student_data["community"] == community_id
    ]

    print(f"\nCOMMUNITY {community_id}")
    print("-------------------")

    # Number of students
    print("Students:", len(group))

    # Most common department
    common_department = group["department"].mode()[0]
    print("Most common department:", common_department)

    # Average degree
    average_degree = group["degree"].mean()
    print("Average degree:", round(average_degree, 2))

    # Most central student
    top_student = group.sort_values(
        "degree",
        ascending=False
    ).iloc[0]

    print(
        "Most connected student:",
        top_student["student_id"]
    )

    # Activities of students in this community
    community_students = group["student_id"].tolist()

    community_participation = participation[
        participation["student_id"].isin(community_students)
    ]

    activity_counts = (
        community_participation["activity_id"]
        .value_counts()
    )

    if len(activity_counts) > 0:

        top_activity_id = activity_counts.index[0]

        activity_name = activities.loc[
            activities["activity_id"] == top_activity_id,
            "activity_name"
        ].iloc[0]

        print(
            "Most common activity:",
            activity_name
        )

# -----------------------------
# 4. Save community summary
# -----------------------------

summary = []

for community_id in community_ids:

    group = student_data[
        student_data["community"] == community_id
    ]

    common_department = group["department"].mode()[0]

    top_student = group.sort_values(
        "degree",
        ascending=False
    ).iloc[0]

    community_students = group["student_id"].tolist()

    community_participation = participation[
        participation["student_id"].isin(community_students)
    ]

    activity_counts = (
        community_participation["activity_id"]
        .value_counts()
    )

    top_activity_id = activity_counts.index[0]

    activity_name = activities.loc[
        activities["activity_id"] == top_activity_id,
        "activity_name"
    ].iloc[0]

    summary.append({
        "community": community_id,
        "student_count": len(group),
        "most_common_department": common_department,
        "average_degree": round(group["degree"].mean(), 2),
        "top_student": top_student["student_id"],
        "most_common_activity": activity_name
    })

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    "results/community_summary.csv",
    index=False
)

print("\n\nCOMMUNITY SUMMARY")
print("=================")
print(summary_df.to_string(index=False))

print("\nSaved to:")
print("results/community_summary.csv")