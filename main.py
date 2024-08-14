import asyncio
import logging
import sys

from dblogic.database import database
from aparserlogic.avitoparser import AvitoParser
from tg_bot import start_bot
from botlogic import functions


async def run_parser():
    while True:
        await asyncio.sleep(10)
        for town in ['moskva', 'sankt-peterburg', 'krasnodar', 'ekaterinburg']:
            new_ads = AvitoParser.parse_by_town(town=town)
            logging.info(f'Get {len(new_ads)} new ads from {town}')
            # await functions.send_ads(ads=new_ads, town=town)


def main():
    loop = asyncio.get_event_loop()
    
    task1 = loop.create_task(run_parser())
    task2 = loop.create_task(start_bot())
    loop.run_until_complete(task1)
    loop.run_until_complete(task2)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=open('./info.log', 'w'),
        format="[%(asctime)s] %(levelname)s %(message)s"
    )
    
    main()
    
    