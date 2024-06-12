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
    def __init__(self, init_data, proxy=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Referer": "https://api-clicker.pixelverse.xyz/",
            "Origin": "https://api-clicker.pixelverse.xyz/",
            "initdata": f"{init_data}",
        }
        #self.proxy=proxy
        self.http = AsyncSession(
            timeout=30,
            headers=self.headers,
        )

        self.energy = 0

    async def claim_answer(self):
        try:
            res_account = await self.http.get(
                "https://api-clicker.pixelverse.xyz/api/users",
                headers=self.headers,
            )
            logger.info(f"Response: {res_account.json()}")
            json_data = {
                "7c3a95c6-75a3-4c62-a20e-896a21132060": 2,
                "8074e9c5-f6c2-4012-bfa2-bcc98ceb5175": 0,
                "571523ae-872d-49f0-aa71-53d4a41cd810": 1,
                "f097634a-c8e8-4de9-b707-575d20c5fd88": 3
            }
            res = await self.http.post(
                "https://api-clicker.pixelverse.xyz/api/cypher-games/82c0bae5-59f3-4a07-97e4-bbbff4ead39f/answer",
                json=json_data,
                headers=self.headers,
            )
            logger.info(f"Response: {res.json()}")
        except Exception as e:
            logger.error(f"Error: {e}")


async def main():
    data_list = []
    with open('initdata.txt', 'r') as file:
        data_list = file.readlines()
    proxy_list = []
    with open('proxy_list.txt', 'r') as file:
        proxy_list = file.readlines()
    for index,data in enumerate(data_list):
        onchain = Onchain(data.strip(),proxy_list[index])
        await onchain.claim_answer()

    '''while True:
        try:
            for index,data in enumerate(data_list):
                onchain = Onchain(data)
                await onchain.claim_answer()
            await asyncio.sleep(3600)
            continue
        except Exception as e:
            await asyncio.sleep(2)
            logger.info("Click error")
            continue'''


if __name__ == "__main__":
    asyncio.run(main())
