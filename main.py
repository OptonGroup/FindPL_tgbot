import asyncio
import logging
import sys

from dblogic.database import database
from aparserlogic.avitoparser import AvitoParser
from botlogic.tg_bot import start_bot
from botlogic.functions import functions


async def run_parser():
    num_of_iter = 0
    while True:
        for town in ['moskva', 'sankt-peterburg', 'novosibirsk', 'ekaterinburg', 'kazan', 'nizhniy_novgorod', 'krasnoyarsk', 'chelyabinsk', 'samara', 'ufa', 'rostov-na-donu', 'krasnodar']:
            new_ads = await AvitoParser.parse_by_town(town=town)
            logging.info(f'Get {len(new_ads)} new ads from {town}')
            if num_of_iter:
                try:
                    await functions.send_ads(ads=new_ads, town=town)
                except:
                    pass
        if num_of_iter % 100 == 0:
            database.delete_ads_with_time_more_12hours()
            await functions.send_alarm_active()
        num_of_iter += 1
        await asyncio.sleep(180)

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
    
    