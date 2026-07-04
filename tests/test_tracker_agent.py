from adk_agents.tracker_agent import create_tracker_agent

tracker = create_tracker_agent()

print("✅ Tracker Agent created successfully!")
print(f"Name: {tracker.name}")
print(f"Description: {tracker.description}")