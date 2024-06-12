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
    async def up_level(self,account_index):
        try:
            logger.info(f"Account {account_index}")
            res_account = await self.http.get(
                "https://api-clicker.pixelverse.xyz/api/users",
                headers=self.headers,
            )
            coin = res_account.json()["clicksCount"]
            logger.info(f"Coin: {coin}")
            res_pet = await self.http.get(
                "https://api-clicker.pixelverse.xyz/api/pets",
                headers=self.headers,
            )
            #buy pet

            #up level pet
            list_pet = res_pet.json()["data"]
            while True:
                count = 0
                for index,data in enumerate(list_pet):
                    level_price = list_pet[index]["userPet"]["levelUpPrice"]
                    level_pet = list_pet[index]["userPet"]["level"]
                    pet_id = list_pet[index]["userPet"]["id"]
                    if level_price < coin:
                        res_up_level = await self.http.post(
                            f"https://api-clicker.pixelverse.xyz/api/pets/user-pets/{pet_id}/level-up",
                            headers=self.headers,
                        )
                        level_pet = level_pet + 1
                        logger.info(f"Upload pet {index} level success")
                        coin = coin - level_price
                    else:
                        count += 1
                if count == len(list_pet):
                    break
                else:
                    continue
        except Exception as e:
            logger.error(f"Error: {e}")



async def main():
    data_list = []
    with open('initdata.txt', 'r') as file:
        data_list = file.readlines()
    for index,data in enumerate(data_list):
        onchain = Onchain(data)
        await onchain.up_level(index)

    '''while True:
        try:

            await asyncio.sleep(3600)
            continue
        except Exception as e:
            await asyncio.sleep(2)
            logger.info("Click error")
            continue'''


if __name__ == "__main__":
    asyncio.run(main())
