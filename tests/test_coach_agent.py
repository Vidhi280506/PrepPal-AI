from adk_agents.coach_agent import create_coach_agent

# We don't have a real MCP client yet.
coach = create_coach_agent()

print("✅ Coach Agent created successfully!")
print(f"Name: {coach.name}")
print(f"Description: {coach.description}")