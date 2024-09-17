from graphviz import Digraph

# Enhanced Use Case Diagram
enhanced_use_case = Digraph('Enhanced Use Case Diagram', filename='enhanced_use_case_diagram', format='png')
enhanced_use_case.attr(rankdir='TB', size='10')

# Actor
enhanced_use_case.node('User', shape='actor', label='User')

# Use Cases
enhanced_use_case.node('Manage_Habit_Tracker_and_Activities_Planner', shape='ellipse', label='Manage Habit Tracker and Activities Planner')
enhanced_use_case.node('Create_Habit_Task', shape='ellipse', label='Create Habit/Task')
enhanced_use_case.node('Edit_Habit_Task', shape='ellipse', label='Edit Habit/Task')
enhanced_use_case.node('Delete_Habit_Task', shape='ellipse', label='Delete Habit/Task')
enhanced_use_case.node('View_Habits_Tasks', shape='ellipse', label='View Habits/Tasks')
enhanced_use_case.node('Track_Progress', shape='ellipse', label='Track Progress')

# Relationships
enhanced_use_case.edge('User', 'Manage_Habit_Tracker_and_Activities_Planner')
enhanced_use_case.edge('Manage_Habit_Tracker_and_Activities_Planner', 'Create_Habit_Task')
enhanced_use_case.edge('Manage_Habit_Tracker_and_Activities_Planner', 'Edit_Habit_Task')
enhanced_use_case.edge('Manage_Habit_Tracker_and_Activities_Planner', 'Delete_Habit_Task')
enhanced_use_case.edge('Manage_Habit_Tracker_and_Activities_Planner', 'View_Habits_Tasks')
enhanced_use_case.edge('Manage_Habit_Tracker_and_Activities_Planner', 'Track_Progress')

# Render enhanced use case diagram
enhanced_use_case_path = enhanced_use_case.render('/mnt/data/enhanced_use_case_diagram')
enhanced_use_case_path
