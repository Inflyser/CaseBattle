import aiohttp
import asyncio

async def test_api():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://api.telegram.org") as resp:
                print("Status:", resp.status)
                print("Text:", await resp.text())
        except Exception as e:
            print("Ошибка подключения:", e)

asyncio.run(test_api())