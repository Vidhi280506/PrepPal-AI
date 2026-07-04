import asyncio

from adk_agents.service import PrepPalService
from google.genai import types


async def main():
    service = PrepPalService()
    await service.initialize()

    message = types.Content(
        role="user",
        parts=[
            types.Part(text="Give me an easy Arrays problem")
        ]
    )

    async for event in service.runner.run_async(
        user_id=service.user_id,
        session_id=service.session_id,
        new_message=message,
    ):
        print("=" * 60)
        print("AUTHOR:", event.author)
        print("CONTENT:", event.content)
        print("OUTPUT:", event.output)
        print("TURN COMPLETE:", event.turn_complete)

    await service.shutdown()


asyncio.run(main())