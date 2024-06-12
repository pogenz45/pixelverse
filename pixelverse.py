import sys
from urllib.parse import unquote
from curl_cffi.requests import AsyncSession
import asyncio
from loguru import logger
import random


logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<g>{time:HH:mm:ss:SSS}</g> | <c>{level}</c> | <level>{message}</level>",
)


class Onchain:
    def __init__(self, init_data):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Referer": "https://api-clicker.pixelverse.xyz/",
            "Origin": "https://api-clicker.pixelverse.xyz/",
            "initdata": f"{init_data}",
        }
        self.http = AsyncSession(
            timeout=30,
            headers=self.headers,
        )

        self.energy = 0

    async def claim_coin(self,index):
        try:
            res_account = await self.http.get(
                "https://api-clicker.pixelverse.xyz/api/users",
                headers=self.headers,
            )
            logger.info(f"Response: {res_account.json()}")
            res = await self.http.post(
                "https://api-clicker.pixelverse.xyz/api/mining/claim",
                headers=self.headers,
            )
            logger.info(f"Response: {res.json()}")
            logger.info(f"Check account {index}")
            return res.json()
        except Exception as e:
            logger.error(f"Error: {e}")

    async def claim_daily(self):
        try:
            res = await self.http.post(
                "https://api-clicker.pixelverse.xyz/api/daily-rewards/claim",
                headers=self.headers,
            )
            logger.info(f"Response: {res.json()}")
            return boost
        except Exception as e:
            logger.error(f"Error: {e}")

    async def click(self):
        while True:
            try:
                await self.claim_coin()
                #await asyncio.sleep(28800)
                continue
            except Exception as e:
                await asyncio.sleep(2)
                logger.info("Click error")
                continue


async def main():
    data_list = []
    with open('initdata.txt', 'r') as file:
        data_list = file.readlines()

    while True:
        try:
            for index,data in enumerate(data_list):
                onchain = Onchain(data)
                await onchain.claim_coin(index)
            await asyncio.sleep(3600)
            continue
        except Exception as e:
            await asyncio.sleep(2)
            logger.info("Click error")
            continue


if __name__ == "__main__":
    asyncio.run(main())
