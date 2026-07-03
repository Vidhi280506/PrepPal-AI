"""
PrepPal AI Service Layer.

This module initializes and manages the Google ADK Runner,
MCP connection, and agent lifecycle.

The Streamlit frontend will interact with this service instead
of directly interacting with ADK or MCP.
"""
import os
import sys
import asyncio
import logging
from typing import Optional

# MCP imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Google ADK imports
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

logger = logging.getLogger(__name__)

class PrepPalService:
    """
    Service responsible for managing the lifecycle of the
    Google ADK Runner, MCP connection, and PrepPal agents.
    """

    def __init__(self):
        logger.info("Initializing PrepPalService...")

        # MCP resources
        self.server_params: Optional[StdioServerParameters] = None
        self.stdio_context = None
        self.session_context = None
        self.mcp_session: Optional[ClientSession] = None

        self.read_stream = None
        self.write_stream = None

        # ADK resources
        self.session_service: Optional[InMemorySessionService] = None
        self.adk_session = None

        # Default session information
        self.app_name = "PrepPal"
        self.user_id = "user_1"
        self.session_id = "session_1"

        self.runner: Optional[Runner] = None

        # Agents
        self.root_agent = None
        self.coach_agent = None
        self.tracker_agent = None

        logger.info("PrepPalService object created.")
    
    async def initialize(self):
        """
        Initialize the MCP connection and prepare the ADK runtime.
        """

        logger.info("Initializing PrepPal AI Service...")

    
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "mcp_server.server",
            ],
            env=os.environ.copy(),
        )

        logger.info("MCP server parameters created successfully.")

        logger.info("Starting MCP stdio transport...")

        self.stdio_context = stdio_client(self.server_params)
        logger.info("Opening stdio connection to MCP server...")

        self.read_stream, self.write_stream = await self.stdio_context.__aenter__()

        logger.info("Creating MCP client session...")

        self.session_context = ClientSession(
            self.read_stream,
            self.write_stream,
        )

        self.mcp_session = await self.session_context.__aenter__()

        logger.info("Initializing MCP session...")

        await self.mcp_session.initialize()
    
        self.initialize_agents()
        logger.info("Creating ADK InMemorySessionService...")

        self.session_service = InMemorySessionService()

        logger.info("Creating ADK session...")

        self.adk_session = self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id,
        )
        logger.info("Creating Google ADK Runner...")

        self.runner = Runner(
            app_name=self.app_name,
            agent=self.root_agent,
            session_service=self.session_service,
        )

        logger.info("Runner created successfully.")

        logger.info("ADK session created successfully.")

        logger.info("MCP session initialized successfully.")

        logger.info("Successfully connected to MCP server.")

        logger.info("MCP stdio context created.")

    async def shutdown(self):
        """
        Gracefully close all async resources.
        """

        logger.info("Shutting down PrepPalService...")

        if self.session_context is not None:
            await self.session_context.__aexit__(None, None, None)

        if self.stdio_context is not None:
            await self.stdio_context.__aexit__(None, None, None)

        logger.info("PrepPalService shut down successfully.")
    
    async def test_connection(self):
        """
        Test the MCP connection by calling get_progress.
        """

        result = await self.mcp_session.call_tool(
            "get_progress",
            arguments={}
        )

        return result
    
    async def send_message(self, message: str) -> str:
        """
        Send a user message through the ADK Runner and return the final
        assistant response.
        """

        if self.runner is None:
            raise RuntimeError("Runner has not been initialized.")

        user_message = types.Content(
            role="user",
            parts=[
                types.Part(text=message)
            ]
        )

        final_response = ""

        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=self.session_id,
            new_message=user_message,
        ):
            # Ignore events without content
            if event.content is None:
                continue

            # Extract text from model responses
            for part in event.content.parts:
                if getattr(part, "text", None):
                    final_response = part.text

        return final_response
    
    def initialize_agents(self):
        """
        Create the Coach, Tracker, and Root agents.
        """

        from adk_agents.coach_agent import create_coach_agent
        from adk_agents.tracker_agent import create_tracker_agent
        from adk_agents.root_agent import create_root_agent

        logger.info("Creating Coach Agent...")

        self.coach_agent = create_coach_agent(
            mcp_session=self.mcp_session
        )

        logger.info("Creating Tracker Agent...")

        self.tracker_agent = create_tracker_agent(
            mcp_session=self.mcp_session
        )

        logger.info("Creating Root Agent...")

        self.root_agent = create_root_agent(
            sub_agents=[
                self.coach_agent,
                self.tracker_agent,
            ]
        )

        logger.info("All agents initialized successfully.")