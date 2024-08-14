from dataclasses import dataclass

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


@dataclass
class Secrets:
    token: str = '6871227651:AAERMJQEN4c8LZkRvD0arP9P37zSHQ7vmTs'

bot = Bot(token=Secrets.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
