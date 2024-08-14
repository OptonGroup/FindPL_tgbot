import time
import json
import logging
from datetime import datetime
from fake_headers import Headers
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from dblogic.database import database


class AvitoParserClass(object):
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--autoplay-policy=no-user-gesture-required")
        options.experimental_options["prefs"] = {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.mixed_script': 2,
            'profile.managed_default_content_settings.media_stream': 2,
            'profile.managed_default_content_settings.stylesheets': 2
        }

        self.browser = uc.Chrome(options=options, headless=True)
        self.browser.execute_cdp_cmd(
            'Network.setBlockedURLs', {'urls': [
                '*.js',
                '*.css',
                '*.png',
            ]})
        self.browser.execute_cdp_cmd('Network.enable', {})
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
        })

        
    def parse_by_town(self, town='moskva'):
        town_id = {
            'moskva': '637640',
            'sankt-peterburg': '653240',
            'krasnodar': '633540',
            'ekaterinburg': '654070',
        }

        time.sleep(1.7)
        url = f'https://www.avito.ru/web/1/js/items?_=&categoryId=24&locationId={town_id[town]}&cd=0&s=104&p=1&params%5B201%5D=1060&params%5B504%5D%5B0%5D=5256&verticalCategoryId=1&rootCategoryId=4&localPriority=1&disabledFilters%5Bids%5D%5B0%5D=byTitle&disabledFilters%5Bslugs%5D%5B0%5D=bt'
        self.browser.get(url)
        content = json.loads(BeautifulSoup(self.browser.page_source, 'html.parser').find('pre').text)
        try:
            ads = content['catalog']['items'][::-1]
        except:
            logging.error(f'Error Parsing: town={town}, server_ans={content}')
            return []

        new_ads = []
        for ad in ads:
            try:
                ad_id = ad['id']
                if not database.is_ad_in_database(ad_id=ad_id):
                    database.add_ad(ad_id=ad_id, town=town)
                    new_ads.append(
                        f'''{ad['title']}\n📆 {datetime.utcfromtimestamp(ad['sortTimeStamp']//1000).strftime('%Y-%m-%d %H:%M:%S')}\n💵 {ad['priceDetailed']['fullString']}\n\nhttps://www.avito.ru/{ad['id']}\n🏠 {ad['coords']['address_user']}'''
                    )
            except:
                pass
        return new_ads
    
if __name__ == '__main__':
    parser = AvitoParserClass()
    print(len(parser.parse_by_town(town='moskva')))