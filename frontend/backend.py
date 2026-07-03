import os
import sys
import asyncio
import json

DEV_MODE = True

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from adk_agents.service import PrepPalService


_service = None
_loop = None


def _get_loop():
    """
    Returns a reusable event loop.
    """
    global _loop

    if _loop is None:
        _loop = asyncio.new_event_loop()

    return _loop


def _get_service():
    """
    Initializes PrepPalService only once and reuses it.
    """
    global _service

    loop = _get_loop()

    asyncio.set_event_loop(loop)

    if _service is None:
        _service = PrepPalService()
        loop.run_until_complete(_service.initialize())

    return _service, loop


def ask_preppal(message: str) -> str:
    """
    Sends a message to PrepPal AI and returns the response.
    """

    if DEV_MODE:

        msg = message.lower()

        if "progress" in msg:
            return """
## 📈 Progress Summary

Problems Solved: **42**

Accuracy: **78%**

Weak Topics:
- Graphs
- Dynamic Programming

Today's Recommendation:
Practice 3 Graph problems.
"""

        elif "array" in msg:
            return """
## 📚 Arrays Practice

### Two Sum

Difficulty: Easy

Hint:
Use a HashMap to store previously seen values.
"""

        elif "graph" in msg:
            return """
## 📚 Graph Practice

### Number of Islands

Difficulty: Medium

Hint:
DFS or BFS traversal.
"""

        elif "dynamic" in msg or "dp" in msg:
            return """
## 📚 Dynamic Programming

### Climbing Stairs

Difficulty: Easy

Hint:
Think Fibonacci.
"""

        else:
            return f"""
## 🤖 PrepPal (Development Mode)

You asked:

> {message}

This is a mock response.

Gemini was NOT called.
"""

    service, loop = _get_service()

    return loop.run_until_complete(
        service.send_message(message)
    )


def get_progress():
    """
    Returns the user's progress dashboard data.
    """

    service, loop = _get_service()

    result = loop.run_until_complete(
        service.get_progress()
    )

    text = result.content[0].text

    return json.loads(text)


def get_review_queue():
    """
    Returns the user's spaced repetition review queue.
    """

    service, loop = _get_service()

    result = loop.run_until_complete(
        service.get_review_queue()
    )

    text = result.content[0].text

    return json.loads(text)