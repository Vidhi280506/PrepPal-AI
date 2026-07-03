"""
PrepPal AI - Coach Agent

This module configures the Google ADK Coach Agent.
The Coach Agent teaches DSA concepts, recommends problems,
provides progressive hints, and records practice attempts
through the MCP Server.
"""

import asyncio
import json
import logging
from typing import Any, Optional

from google.adk.agents import LlmAgent

from adk_agents.config import MODEL_NAME
from adk_agents.prompts import COACH_AGENT_PROMPT

logger = logging.getLogger(__name__)


def create_coach_agent(mcp_session: Optional[Any] = None) -> LlmAgent:
    """
    Creates the PrepPal AI Coach Agent.

    Parameters
    ----------
    mcp_session:
        Connected MCP client session.

    Returns
    -------
    LlmAgent
    """

    logger.info("Initializing PrepPal Coach Agent.")

    async def get_problem(
        topic: str = "",
        difficulty: str = ""
    ) -> str:
        """
        Fetch a practice problem from the MCP server.
        """

        logger.info(
            "Calling MCP get_problem (topic=%s, difficulty=%s)",
            topic,
            difficulty,
        )

        if mcp_session is None:
            logger.error("MCP session not configured.")

            return json.dumps({
                "error": "MCP session not configured."
            })

        arguments = {}

        if topic:
            arguments["topic"] = topic

        if difficulty:
            arguments["difficulty"] = difficulty

        try:

            result = await mcp_session.call_tool(
               "get_problem",
                arguments=arguments
            )

            if getattr(result, "content", None):
                return result.content[0].text

            return json.dumps({
                "error": "Empty response from MCP server."
            })

        except Exception as e:

            logger.exception("Failed to fetch problem from MCP.")

            return json.dumps({
                "error": str(e)
            })

    async def submit_attempt(
        problem_id: int,
        solved: bool,
        time_spent_minutes: int,
    ) -> str:
        """
        Submit a solved attempt to the MCP server.
        """

        logger.info(
            "Submitting attempt for problem %s",
            problem_id,
        )

        if mcp_session is None:
            logger.error("MCP session not configured.")

            return json.dumps({
                "error": "MCP session not configured."
            })

        try:

            result = await mcp_session.call_tool(
                "submit_attempt",
                arguments={
                "problem_id": problem_id,
                "solved": solved,
                "time_spent_minutes": time_spent_minutes,
                },
            )

            if getattr(result, "content", None):
                return result.content[0].text

            return json.dumps({
                "error": "Empty response from MCP server."
            })

        except Exception as e:

            logger.exception("Failed to submit attempt.")

            return json.dumps({
                "error": str(e)
            })

    coach_agent = LlmAgent(
        name="PrepPalCoachAgent",
        model=MODEL_NAME,
        description=(
            "Expert DSA coach that teaches algorithms, recommends "
            "practice questions, provides progressive hints, and "
            "evaluates submissions using MCP tools."
        ),
        instruction=COACH_AGENT_PROMPT,
        tools=[
            get_problem,
            submit_attempt,
        ],
    )

    logger.info("Coach Agent initialized successfully.")

    return coach_agent