import asyncio

from adk_agents.service import PrepPalService


async def main():
    service = PrepPalService()

    await service.initialize()

    result = await service.get_review_queue()

    print(result)

    await service.shutdown()


if __name__ == "__main__":
    asyncio.run(main())