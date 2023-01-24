import asyncio

from loguru import logger

from loader import client


async def test_client():
    x, y = await client.coordinates("Detroit")
    print(x, y)
    coordinates = await client.address(f"{x}", f"{y}")
    logger.info(coordinates)


async def main():
    await test_client()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
