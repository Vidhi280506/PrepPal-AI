import asyncio

from adk_agents.service import PrepPalService


async def main():
    service = PrepPalService()

    await service.initialize()

    print("Runner Created!")
    print(service.runner)

    await service.shutdown()


asyncio.run(main())