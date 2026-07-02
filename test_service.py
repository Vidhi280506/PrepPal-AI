import asyncio

from adk_agents.service import PrepPalService


async def main():
    service = PrepPalService()

    await service.initialize()

    print("Session Created!")
    print(service.adk_session)

    await service.shutdown()


asyncio.run(main())