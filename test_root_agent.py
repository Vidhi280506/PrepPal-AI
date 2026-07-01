from adk_agents.root_agent import create_root_agent

agent = create_root_agent()

print("✅ Root Agent created successfully!")
print(f"Name: {agent.name}")
print(f"Description: {agent.description}")