import asyncio
import json
import logging
from datetime import datetime
from fake_headers import Headers
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

from dblogic.database import database





class AvitoParserClass(object):
    def __init__(self):
        pass

        
    async def parse_by_town(self, town='moskva'):
        town_id = {
            'moskva': '637640',
            'sankt-peterburg': '653240',
            'krasnodar': '633540',
            'ekaterinburg': '654070',
        }

        await asyncio.sleep(3)
        cookies = {'srv_id': 'ky8IHMGa6NmDFEsL.wNkOEXnND-eQ06uLPep3CFu_TQzmS7Ozcn7VJrAP2ncAoyLQ1HBzYwgznnkuvdU=.NdGnePR4VP056auotSTBV8FCHtl7A6KgiMwFvOYYJS4=.web','u': '2y2zaljg.qdyhbw.1cnnie6lxux00','_ga': 'GA1.1.1016894630.1695132607','tmr_lvid': '97cb1a03300cd7fc824f4e570ccae42e','tmr_lvidTS': '1695132607248','adrcid': 'AkfJ3ieE1dAbtGhT6_MvU1Q','_ym_uid': '1695132608524473015','uxs_uid': '3d50e7c0-56f6-11ee-8626-a96b50812051','__zzatw-avito': 'MDA0dBA=Fz2+aQ==','__zzatw-avito': 'MDA0dBA=Fz2+aQ==','buyer_laas_location': '637640','gsscw-avito': 'Mmspa2zYgQX7zmTkCym7/LLmgq0xeeXYS9HhVDWlniWJJA5JbF1EgHg/mS4JZt+drZV9Zri4qH78j43MgL5SF48maqpsxnmOKvK6sWfTK+3rWMbV0FWvyJQchQ10gdJMwIJ/bnyYC2FZwZ289U+dOESy0WrKKzymfHuuDl9VgkfMrf5ycQZ4W8yWY9cq5GmqkJgNdxt9ojnqrfx3cELRGENBAaCLLXpF5VM+Vba1hzQ8ORS0faNRegPPEi+bqA==','gsscw-avito': 'Mmspa2zYgQX7zmTkCym7/LLmgq0xeeXYS9HhVDWlniWJJA5JbF1EgHg/mS4JZt+drZV9Zri4qH78j43MgL5SF48maqpsxnmOKvK6sWfTK+3rWMbV0FWvyJQchQ10gdJMwIJ/bnyYC2FZwZ289U+dOESy0WrKKzymfHuuDl9VgkfMrf5ycQZ4W8yWY9cq5GmqkJgNdxt9ojnqrfx3cELRGENBAaCLLXpF5VM+Vba1hzQ8ORS0faNRegPPEi+bqA==','cfidsw-avito': '+6r9v4tVzM0+qMOCQU7R8wePQjzhIhnfqUyE5sp+C7P1apcwlG7Qmnyts2iHyEABC4nitEr9wwia4sVgZFa/Y8pWAyGSNRA0dpJy9PeILuPSw5q4dQ1aUYXcgg9EdT9R2bhWDrUnjra6KC+IcE2eVU+THuFLgmU3r+xnuys=','cfidsw-avito': '+6r9v4tVzM0+qMOCQU7R8wePQjzhIhnfqUyE5sp+C7P1apcwlG7Qmnyts2iHyEABC4nitEr9wwia4sVgZFa/Y8pWAyGSNRA0dpJy9PeILuPSw5q4dQ1aUYXcgg9EdT9R2bhWDrUnjra6KC+IcE2eVU+THuFLgmU3r+xnuys=','cfidsw-avito': '+6r9v4tVzM0+qMOCQU7R8wePQjzhIhnfqUyE5sp+C7P1apcwlG7Qmnyts2iHyEABC4nitEr9wwia4sVgZFa/Y8pWAyGSNRA0dpJy9PeILuPSw5q4dQ1aUYXcgg9EdT9R2bhWDrUnjra6KC+IcE2eVU+THuFLgmU3r+xnuys=','_ga_WW6Q1STJ8M': 'GS1.1.1707244345.1.0.1707244365.0.0.0','_ga_ZJDLBTV49B': 'GS1.1.1707244345.1.0.1707244365.0.0.0','fgsscw-avito': 'wQ1R51f81d3efd998b5497bfea2ffede333f050f','fgsscw-avito': 'wQ1R51f81d3efd998b5497bfea2ffede333f050f','_ym_d': '1723120788','_gcl_au': '1.1.673711584.1723120788','adrcid': 'AkfJ3ieE1dAbtGhT6_MvU1Q','ma_prevFp_3485699018': '2081412741|851155102|423588996|888000370|2219907560|2766682514|3530670207|888000370|1068634537|3180462103|1068634537|1305082283|2530088751|3579944471|4191350549|3579944471|888000370|1068634537|3539069274|888000370|621576841|3530670207|3579944471|1068634537|1967389372|668684770|3579944471|2800598003|490591024|888000370|1144773868|3708322660|718548439|3308070491','__ai_fp_uuid': 'bd12a2940fcfd0f5%3A1','yandex_monthly_cookie': 'true','__upin': '8Qs7sG9JBUofB1SIpo0VQg','_buzz_fpc': 'JTdCJTIydmFsdWUlMjIlM0ElN0IlMjJ1ZnAlMjIlM0ElMjJlYzU3YTU3M2Q1NjUzZDJmZDhmYTcwOTUyMzUxN2ZmZiUyMiUyQyUyMmJyb3dzZXJWZXJzaW9uJTIyJTNBJTIyMTI3LjAlMjIlMkMlMjJ0c0NyZWF0ZWQlMjIlM0ExNzIzMTIwNzg5MzM2JTdEJTJDJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyRnJpJTJDJTIwMDglMjBBdWclMjAyMDI1JTIwMTIlM0EzOSUzQTUyJTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlN0Q=','_buzz_aidata': 'JTdCJTIydmFsdWUlMjIlM0ElN0IlMjJ1ZnAlMjIlM0ElMjI4UXM3c0c5SkJVb2ZCMVNJcG8wVlFnJTIyJTJDJTIyYnJvd3NlclZlcnNpb24lMjIlM0ElMjIxMjcuMCUyMiUyQyUyMnRzQ3JlYXRlZCUyMiUzQTE3MjMxMjA3OTE0MjclN0QlMkMlMjJwYXRoJTIyJTNBJTIyJTJGJTIyJTJDJTIyZG9tYWluJTIyJTNBJTIyLnd3dy5hdml0by5ydSUyMiUyQyUyMmV4cGlyZXMlMjIlM0ElMjJGcmklMkMlMjAwOCUyMEF1ZyUyMDIwMjUlMjAxMiUzQTM5JTNBNTIlMjBHTVQlMjIlMkMlMjJTYW1lU2l0ZSUyMiUzQSUyMkxheCUyMiU3RA==','gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN','f': '5.32e32548b6f3e9784b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36da6d7377b87edb337e7721a3e5d3cdbb46b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8cad08e7e7eb412c8fa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112f12b79bbb67ac37d46b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264ede992ad2cc54b8aa846b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c03d3f0af72d633b5db6aace19274a12602c730c0109b9fbbc683850773e71095a0001bc166cffee90e28148569569b79cdb19ffe50c1c7de71e7cb57bbcb8e0f0df103df0c26013a0df103df0c26013aafbc9dcfc006bed9f8885e43e993384b7a8d408558788c3c3de19da9ed218fe23de19da9ed218fe200d3eb918501f61078a492ecab7d2b7f','v': '1723664307','ft': '"1DFZ0TyTSj/pAEQl43ZXLWrg0DzUOfE3IvJhVFdZvlQHiLUhY1GzSPeLjkrfzISWvS3CM6b0Ax+TgAv04yjztZTgoiVYbmpoP9dGm0rfEfnlRrZ8p46Yb4L1vTxIaH51RmSE6TsLeXKt+oaB2Kk7+Mz9f8z1AlJV5JRA9guB2hUTLvjW/EgRl6cMmERYVXLW"','dfp_group': '9','abp': '0','_ym_isad': '2','_ym_visorc': 'b','domain_sid': 'ce7UrJ-afHn-Z_Eb1OSAs%3A1723664310960','adrdel': '1723664311646','adrdel': '1723664311646','tmr_detect': '0%7C1723664313524','buyer_location_id': f'{town_id[town]}','luri': 'ekaterinburg','sx': 'H4sIAAAAAAAC%2F1TMUZLyIAwA4Lvw7AMhNIHeBkiY%2Bv%2FUaitV1%2Bndd%2FbBmd0LfG%2FjCEiDclKMCIjJpZCohuIVbCpgxrfZzWgy0Lnnf1Dmac%2BPx%2FLyAYZXglxYpBdzMmpGYIfsiF04ToaIqAhTjRQH8hSVs2IUHmwpLPEjt0Ux3bYn3f02tTl%2FzWvcG7Zys77J9Zc8WLY%2FckaEHKuvygDiNXjrbbKUmKyroh9Z8n7fZJ8y9rZS%2F%2F%2B8bOG89bpeliv7%2FldGPI7vAAAA%2F%2F%2FTRAuVDwEAAA%3D%3D','_ga_M29JC28873': 'GS1.1.1723664310.7.0.1723664334.36.0.0',}
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7','cache-control': 'max-age=1', 'priority': 'u=0, i','sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',}
        params = {'_': '','categoryId': '24','locationId': f'{town_id[town]}','user': '1','cd': '0','s': '104','p': '1','params[201]': '1060','params[504][0]': '5256','verticalCategoryId': '1','rootCategoryId': '4','localPriority': '1','disabledFilters[ids][0]': 'byTitle','disabledFilters[slugs][0]': 'bt',}

        try:
            response = requests.get('https://www.avito.ru/web/1/js/items', params=params, cookies=cookies, headers=headers)
            content = response.json()
        except:
            logging.error(f'Error Parsing: town={town}')
            return []
            
        try:
            ads = content['catalog']['items'][::-1]
        except:
            logging.error(f'Error Parsing: town={town}, server_ans={content}')
            return []

        new_ads = []
        for ad in ads:
            try:
                ad_id = ad['id']
            except:
                continue
            
            if not database.is_ad_in_database(ad_id=ad_id):
                database.add_ad(ad_id=ad_id, town=town)
                new_ads.append(
                    f'''{ad['title']}\n📆 {datetime.utcfromtimestamp(ad['sortTimeStamp']//1000).strftime('%Y-%m-%d %H:%M:%S')}\n💵 {ad['priceDetailed']['fullString']}\n\nhttps://www.avito.ru/{ad['id']}\n🏠 {ad['coords']['address_user']}'''
                )
           
        return new_ads
    
if __name__ == '__main__':
    parser = AvitoParserClass()
    print(len(parser.parse_by_town(town='moskva')))
