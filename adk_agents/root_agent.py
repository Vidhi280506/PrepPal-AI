"""
PrepPal AI - Root Agent Orchestrator
This module configures the Google ADK Root Agent, responsible for routing 
user intents to the appropriate specialized sub-agents.
"""

import logging
from typing import List, Optional

# Official Google ADK SDK imports
from google.adk.agents import LlmAgent, Agent
from adk_agents.config import MODEL_NAME
from adk_agents.prompts import ROOT_AGENT_PROMPT

# Configure module-level logger
logger = logging.getLogger(__name__)

def create_root_agent(sub_agents: Optional[List[Agent]] = None) -> LlmAgent:
    """
    Creates and configures the PrepPal AI Root Agent using the Google ADK SDK.
    
    The Root Agent acts as the primary orchestrator. It does not answer
    domain-specific questions directly. Instead, it analyzes the user's 
    intent and leverages ADK's native delegation to route the task to 
    the appropriate specialized sub-agent:
    - Coach Agent: For practicing, answering questions, and learning.
    - Tracker Agent: For viewing progress, dashboards, and review queues.
    
    Args:
        sub_agents (List[Agent], optional): The specialized agents (e.g., Coach, Tracker) 
            that this root agent can delegate tasks to. Defaults to None for safe initialization.
            
    Returns:
        LlmAgent: The configured ADK Root Agent instance.
    """
    logger.info("Initializing the PrepPal AI Root Agent.")
    
    # Fallback to an empty list if no sub-agents are provided yet (Milestone constraint)
    agents_to_register = sub_agents if sub_agents is not None else []

    # Define the Root Orchestrator
    root_agent = LlmAgent(
        name="PrepPalRootAgent",
        model=MODEL_NAME,
        instruction=ROOT_AGENT_PROMPT,
        description=(
            "The main orchestrator for PrepPal AI. "
            "Routes user requests to specialized Coach or Tracker agents based on intent."
        ),
        # In Google ADK, passing sub-agents as tools allows the core LLM 
        # to read their descriptions and invoke them dynamically.
        sub_agents=agents_to_register
    )
    
    logger.info(f"Root Agent '{root_agent.name}' created with {len(agents_to_register)} sub-agents ready for delegation.")
    
    return root_agent