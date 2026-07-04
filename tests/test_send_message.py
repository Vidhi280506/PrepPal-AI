import asyncio

from adk_agents.service import PrepPalService


async def main():
    service = PrepPalService()

    await service.initialize()

    print("\n=== Tracker Test ===")
    response = await service.send_message("Show my progress")
    print(response)

    print("\n=== Coach Test ===")
    response = await service.send_message("Give me an Arrays problem")
    print(response)

    await service.shutdown()


asyncio.run(main())