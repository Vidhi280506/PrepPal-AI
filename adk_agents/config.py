"""
Configuration for PrepPal AI ADK Agents.
"""

import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LOG_LEVEL = "INFO"

MAX_RETRIES = 3
REQUEST_TIMEOUT = 30