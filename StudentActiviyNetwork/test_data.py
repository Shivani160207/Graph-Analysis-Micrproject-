import pandas as pd

students = pd.read_csv("Data/students.csv")
activities = pd.read_csv("Data/activities.csv")
participation = pd.read_csv("Data/participation.csv")

print("STUDENTS")
print(students.head())

print("\nACTIVITIES")
print(activities.head())

print("\nPARTICIPATION")
print(participation.head())

print("\n--- DATASET INFORMATION ---")
print("Number of students:", len(students))
print("Number of activities:", len(activities))
print("Number of participation records:", len(participation))

used_activities = participation["activity_id"].unique()

unused = activities[~activities["activity_id"].isin(used_activities)]

print("\nActivities with no participants:")
print(unused)