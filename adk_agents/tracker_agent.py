"""
PrepPal AI - Tracker Agent
This module configures the Google ADK Tracker Agent, responsible for monitoring 
and explaining student analytics, performance metrics, and upcoming spaced 
repetition requirements. It communicates with the backend exclusively via 
the Model Context Protocol (MCP) server.
"""

import logging
import asyncio
import json
from typing import Optional, Any

# Official Google ADK SDK imports
from google.adk.agents import LlmAgent

# Configuration and Prompts imports
from adk_agents.config import MODEL_NAME
from adk_agents.prompts import TRACKER_AGENT_PROMPT

# Configure module-level logger
logger = logging.getLogger(__name__)

def create_tracker_agent(mcp_session: Optional[Any] = None) -> LlmAgent:
    """
    Creates and configures the PrepPal AI Tracker Agent.
    
    The Tracker Agent specializes entirely in student metrics, learning dashboards, 
    and spaced repetition logistics. It analyzes performance strengths or gaps, provides 
    insight into upcoming reviews, and motivates learners without ever teaching raw 
    algorithms or providing practice problem material directly.
    
    Args:
        mcp_session (Optional[Any]): An active, connected MCP client session used 
            to call the remote tracking tools. Defaults to None.
            
    Returns:
        LlmAgent: The configured ADK Tracker Agent instance.
    """
    logger.info("Initializing the PrepPal AI Tracker Agent.")

    def get_progress() -> str:
        """
        Retrieves user dashboard metrics including total problems solved, 
        overall accuracy, mastered topics, and identified weak domains.
        
        Returns:
            str: A JSON string containing the progress analytics or an error message.
        """
        logger.info("Tracker Agent invoking get_progress tool via MCP.")
        
        if not mcp_session:
            logger.error("MCP session is not available in Tracker Agent.")
            return json.dumps({"error": "MCP session not configured. Cannot fetch progress metrics."})

        try:
            # Safely wrap the async MCP call for the synchronous ADK framework execution
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                mcp_session.call_tool("get_progress", arguments={})
            )
            
            if not result or not getattr(result, "content", None):
                logger.warning("MCP get_progress returned an empty or malformed response.")
                return json.dumps({"progress": {}, "message": "No progress data found."})
                
            return result.content[0].text
            
        except Exception as e:
            logger.exception(f"Failed to fetch progress metrics via MCP: {e}")
            return json.dumps({"error": f"Failed to communicate with MCP server: {str(e)}"})

    def get_review_queue() -> str:
        """
        Retrieves the list of topics and problems that have become due for 
        revision based on the SM-2 spaced repetition schedules.
        
        Returns:
            str: A JSON string containing the due review objects or an error message.
        """
        logger.info("Tracker Agent invoking get_review_queue tool via MCP.")
        
        if not mcp_session:
            logger.error("MCP session is not available in Tracker Agent.")
            return json.dumps({"error": "MCP session not configured. Cannot fetch review queue."})

        try:
            # Safely wrap the async MCP call for the synchronous ADK framework execution
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                mcp_session.call_tool("get_review_queue", arguments={})
            )
            
            if not result or not getattr(result, "content", None):
                logger.warning("MCP get_review_queue returned an empty or malformed response.")
                return json.dumps({"due_reviews": [], "message": "No reviews due at this time."})
                
            return result.content[0].text
            
        except Exception as e:
            logger.error(f"Failed to fetch review queue via MCP: {e}")
            return json.dumps({"error": f"Failed to communicate with MCP server: {str(e)}"})

    # Initialize the Tracker Agent as an isolated LlmAgent
    tracker_agent = LlmAgent(
        name="PrepPalTrackerAgent",
        model=MODEL_NAME,
        instruction=TRACKER_AGENT_PROMPT,
        description=(
            "An analytics and progress-tracking companion for PrepPal AI. "
            "Responsible for breaking down dashboard statistics, accuracy profiles, "
            "weak topics, and explaining upcoming spaced repetition queues. "
            "It is completely restricted from teaching coding syntax, explaining algorithms, "
            "or creating new practice problems."
        ),
        tools=[get_progress, get_review_queue]
    )
    
    logger.info(f"Tracker Agent '{tracker_agent.name}' successfully initialized with tracking tools linked.")
    
    return tracker_agent