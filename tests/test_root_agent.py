from adk_agents.root_agent import create_root_agent
from adk_agents.coach_agent import create_coach_agent
from adk_agents.tracker_agent import create_tracker_agent

coach = create_coach_agent()
tracker = create_tracker_agent()

root = create_root_agent(
    sub_agents=[
        coach,
        tracker
    ]
)

print("✅ Root Agent created successfully!")
print(f"Name: {root.name}")
print(f"Number of sub-agents: {len(root.sub_agents)}")

for agent in root.sub_agents:
    print(f"- {agent.name}")